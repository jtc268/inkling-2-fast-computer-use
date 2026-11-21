"""Independently audit a BF16 output-row edit across a complete Inkling checkpoint."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import tempfile


TENSOR = "model.llm.unembed.weight"
INDEX = "model.safetensors.index.json"
BLOCK = 8 * 1024 * 1024
REQUIRED = {
    INDEX, "config.json", "generation_config.json", "hf_quant_config.json",
    "processor_config.json", "special_tokens_map.json", "tokenizer.json",
    "tokenizer_config.json", "chat_template.jinja", "tiktoken/tokenizer.model",
    "mtp.safetensors",
}


def checkpoint_files(directory):
    """Compare all regular assets, apart from documentation and repository metadata."""
    files = set()
    for path in directory.rglob("*"):
        rel = path.relative_to(directory)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if path.is_symlink() and not path.exists():
            raise ValueError(f"Broken link in checkpoint: {rel}")
        if path.is_symlink() and path.is_dir():
            raise ValueError(f"Directory symlink cannot be audited recursively: {rel}")
        if path.is_file() and path.suffix.lower() != ".md" and path.name not in {"LICENSE", "NOTICE"}:
            files.add(rel.as_posix())
    missing = REQUIRED - files
    if missing:
        raise ValueError(f"Required inference files missing: {sorted(missing)}")
    return files


def file_state(stream):
    st = os.fstat(stream.fileno())
    return st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns


def safe_shard_name(directory):
    index = json.loads((directory / INDEX).read_bytes())
    name = index["weight_map"][TENSOR]
    if not isinstance(name, str) or Path(name).name != name or not name.endswith(".safetensors"):
        raise ValueError("Invalid output tensor shard in index")
    return name


def tensor_layout(stream, file_size):
    raw_size = stream.read(8)
    if len(raw_size) != 8:
        raise ValueError("Truncated safetensors prefix")
    header_bytes, = struct.unpack("<Q", raw_size)
    if not 2 <= header_bytes <= min(file_size - 8, 100_000_000):
        raise ValueError("Invalid safetensors header length")
    header = stream.read(header_bytes)
    metadata = json.loads(header)
    tensor = metadata[TENSOR]
    shape = tensor["shape"]
    if tensor["dtype"] != "BF16" or len(shape) != 2 or not all(type(n) is int and n > 0 for n in shape):
        raise ValueError("Expected a two-dimensional BF16 output tensor")
    data_start = 8 + header_bytes
    start, end = tensor["data_offsets"]
    row_bytes = 2 * shape[1]
    if not (0 <= start < end <= file_size - data_start and end - start == row_bytes * shape[0]):
        raise ValueError("Invalid output tensor bounds")
    for name, other in metadata.items():
        if name not in (TENSOR, "__metadata__"):
            left, right = other["data_offsets"]
            if left < right and max(start, left) < min(end, right):
                raise ValueError(f"Output tensor overlaps tensor {name}")
    return shape, row_bytes, data_start + start, raw_size + header


def equal_until(before, after, stop, h_base, h_candidate, label):
    while before.tell() < stop:
        size = min(BLOCK, stop - before.tell())
        left, right = before.read(size), after.read(size)
        if len(left) != size or len(right) != size:
            raise ValueError(f"Unexpected EOF in {label}")
        if left != right:
            mismatch = next(i for i, (a, b) in enumerate(zip(left, right)) if a != b)
            raise ValueError(f"Unapproved byte difference in {label} at offset {before.tell() - size + mismatch}")
        h_base.update(left)
        h_candidate.update(right)


def diff_row(row, offset, before, after):
    changed_values = sum(a != b for a, b in zip(struct.iter_unpack("<H", before), struct.iter_unpack("<H", after)))
    if not changed_values:
        raise ValueError(f"Declared row {row} is identical to the base")
    ranges = []
    for i, (a, b) in enumerate(zip(before, after)):
        if a != b:
            position = offset + i
            if ranges and position == ranges[-1][1]:
                ranges[-1][1] += 1
            else:
                ranges.append([position, position + 1])
    return {
        "row": row, "shard_offset": offset,
        "changed_bf16_values": changed_values,
        "changed_bytes": sum(hi - lo for lo, hi in ranges),
        "base_sha256": hashlib.sha256(before).hexdigest(),
        "candidate_sha256": hashlib.sha256(after).hexdigest(),
        "changed_byte_ranges": ranges,
    }


def audit_shard(base_path, candidate_path, rows):
    with base_path.open("rb") as before, candidate_path.open("rb") as after:
        orig_base, orig_candidate = file_state(before), file_state(after)
        if orig_base[:2] == orig_candidate[:2]:
            raise ValueError("The main shards have the same inode")
        size = orig_base[2]
        if orig_candidate[2] != size:
            raise ValueError("Main shard sizes differ")
        shape, row_bytes, start, header = tensor_layout(before, size)
        if after.read(len(header)) != header:
            raise ValueError("Main shard tensor metadata differs")
        h_base, h_candidate = hashlib.sha256(header), hashlib.sha256(header)
        row_diffs = []
        for row in rows:
            if not 0 <= row < shape[0]:
                raise ValueError(f"Row index outside output tensor: {row}")
            offset = start + row * row_bytes
            equal_until(before, after, offset, h_base, h_candidate, base_path.name)
            left, right = before.read(row_bytes), after.read(row_bytes)
            if len(left) != row_bytes or len(right) != row_bytes:
                raise ValueError("Truncated edited row")
            row_diffs.append(diff_row(row, offset, left, right))
            h_base.update(left)
            h_candidate.update(right)
        equal_until(before, after, size, h_base, h_candidate, base_path.name)
        if (orig_base, orig_candidate) != (file_state(before), file_state(after)):
            raise ValueError("A main shard changed while auditing")
    return {
        "shard": base_path.name, "shard_bytes": size,
        "base_sha256": h_base.hexdigest(), "candidate_sha256": h_candidate.hexdigest(),
        "tensor": TENSOR, "dtype": "BF16", "shape": shape, "rows": rows, "row_bytes": row_bytes,
        "changed_bf16_values": sum(r["changed_bf16_values"] for r in row_diffs),
        "changed_bytes": sum(r["changed_bytes"] for r in row_diffs),
        "row_diffs": row_diffs, "byte_range_format": "Absolute shard offsets, inclusive start and exclusive end",
        "tensor_header_sha256": hashlib.sha256(header).hexdigest(),
        "tensor_metadata_identical": True, "all_bytes_outside_declared_rows_identical": True,
        "main_shards_have_distinct_inodes": True,
    }


def audit(base, candidate, rows):
    if not rows or len(rows) != len(set(rows)):
        raise ValueError("Provide a nonempty set of distinct row IDs")
    files, other = checkpoint_files(base), checkpoint_files(candidate)
    if files != other:
        raise ValueError(f"Checkpoint file manifests differ: {sorted(files ^ other)}")
    shard = safe_shard_name(base)
    if shard != safe_shard_name(candidate):
        raise ValueError("The tensor index maps the output tensor to different shards")
    report = audit_shard(base / shard, candidate / shard, sorted(rows))
    auxiliary = {}
    for name in sorted(files - {shard}):
        with (base / name).open("rb") as before, (candidate / name).open("rb") as after:
            old_base, old_candidate = file_state(before), file_state(after)
            if old_base[2] != old_candidate[2]:
                raise ValueError(f"Auxiliary file sizes differ: {name}")
            h_base, h_candidate = hashlib.sha256(), hashlib.sha256()
            equal_until(before, after, old_base[2], h_base, h_candidate, name)
            if (old_base, old_candidate) != (file_state(before), file_state(after)):
                raise ValueError(f"Auxiliary file changed while auditing: {name}")
            auxiliary[name] = {"sha256": h_base.hexdigest(), "bytes": old_base[2]}
    report["auxiliary_files_identical"] = auxiliary
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--rows", type=int, nargs="+", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--expect-base-sha256")
    parser.add_argument("--expect-candidate-sha256")
    args = parser.parse_args()
    out = args.out.resolve()
    if any(out.is_relative_to(directory.resolve()) for directory in (args.base, args.candidate)):
        parser.error("Write the proof outside both model directories")
    try:
        report = audit(args.base, args.candidate, args.rows)
        for arm, expected in (("base", args.expect_base_sha256), ("candidate", args.expect_candidate_sha256)):
            if expected and report[f"{arm}_sha256"] != expected.lower():
                raise ValueError(f"Unexpected {arm} shard digest")
        with tempfile.NamedTemporaryFile(mode="w", dir=out.parent, prefix=".weight-proof-", delete=False) as tmp:
            json.dump(report, tmp, indent=2)
            tmp.write("\n")
        Path(tmp.name).replace(out)
    except (ValueError, KeyError, OSError) as exc:
        parser.exit(1, f"Weight audit failed: {exc}\n")
    print(f"Verified {report['changed_bf16_values']} changed BF16 values in {len(report['rows'])} rows. "
          f"Candidate SHA-256 {report['candidate_sha256']}")


if __name__ == "__main__":
    main()
