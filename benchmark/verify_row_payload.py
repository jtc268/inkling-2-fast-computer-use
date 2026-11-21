"""Reconstruct the edited shard's SHA-256 from stock weights and the published BF16 rows."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from verify_output_rows import BLOCK, TENSOR, file_state, safe_shard_name, tensor_layout


def verify(base, row_file, report):
    name = safe_shard_name(base)
    if report['shard'] != name or report['tensor'] != TENSOR or report['dtype'] != 'BF16':
        raise ValueError('Checkpoint layout and audit refer to different tensors.')
    with (base / name).open('rb') as stream, np.load(row_file, allow_pickle=False) as payload:
        state = file_state(stream)
        shape, row_bytes, start, header = tensor_layout(stream, state[2])
        rows = report['rows']
        if (len(rows) != len(set(rows)) or sorted(payload.files) != sorted(str(r) for r in rows)
                or shape != report['shape'] or row_bytes != report['row_bytes']):
            raise ValueError('Row payload and audit disagree.')
        stock, edited = hashlib.sha256(header), hashlib.sha256(header)

        def copy_unchanged(until):
            while stream.tell() < until:
                block = stream.read(min(BLOCK, until - stream.tell()))
                if not block:
                    raise ValueError('Truncated stock checkpoint.')
                stock.update(block)
                edited.update(block)

        for row in sorted(rows):
            data = payload[str(row)]
            if not 0 <= row < shape[0] or data.dtype != np.dtype('<u2') or data.shape != (shape[1],):
                raise ValueError(f'Invalid packed BF16 row {row}.')
            copy_unchanged(start + row * row_bytes)
            before = stream.read(row_bytes)
            if len(before) != row_bytes:
                raise ValueError(f'Stock row {row} is truncated.')
            stock.update(before)
            edited.update(data.tobytes(order='C'))
        copy_unchanged(state[2])
        if file_state(stream) != state:
            raise ValueError('Stock shard changed during verification.')
        if stock.hexdigest() != report['base_sha256'] or edited.hexdigest() != report['candidate_sha256']:
            raise ValueError('Reconstructed shard hash differs from the audit.')
    return edited.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('base', type=Path, help='Original Inkling 2 Mini model directory')
    parser.add_argument('rows', type=Path)
    parser.add_argument('audit', type=Path)
    args = parser.parse_args()
    audit = json.loads(args.audit.read_text())
    print(f"Reconstructed edited shard from {len(audit['rows'])} rows: {verify(args.base, args.rows, audit)}")


if __name__ == '__main__':
    main()
