"""Run stock and a pinned edited Inkling checkpoint on the same WebArena task in both orders."""

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

import webarena_ten as bench
from huggingface_hub import snapshot_download

PROFILES = Path(__file__).with_name("browser_checkpoints.json")


def model_directory(profile, supplied):
    directory = supplied or Path(
        snapshot_download(
            profile["repo"],
            revision=profile["revision"],
            allow_patterns=[
                "model*.safetensors",
                "mtp.safetensors",
                "model.safetensors.index.json",
                "config.json",
                "generation_config.json",
                "hf_quant_config.json",
                "processor_config.json",
                "tokenizer.json",
                "tokenizer_config.json",
                "special_tokens_map.json",
                "chat_template.jinja",
                "tiktoken/*",
            ],
        )
    )
    index = json.loads((directory / "model.safetensors.index.json").read_text())
    shard = directory / index["weight_map"]["model.llm.unembed.weight"]
    with shard.open("rb") as f:
        actual = hashlib.file_digest(f, "sha256").hexdigest()
    if actual != profile["shard_sha256"]:
        raise ValueError(
            f"Expected {profile['shard_sha256']}, got {actual} in {shard}."
        )
    return directory.resolve()


def main():
    catalog = json.loads(PROFILES.read_text())
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkpoint", choices=sorted(set(catalog) - {"stock"}), default="mac-headline"
    )
    parser.add_argument(
        "--id", type=int, default=190, help="Official WebArena task number"
    )
    parser.add_argument("--engine", choices=("mlx", "rtx"), default="mlx")
    parser.add_argument("--out", required=True, type=Path, help="New output directory")
    parser.add_argument(
        "--original", type=Path, help="Existing upstream model directory"
    )
    parser.add_argument("--edited", type=Path, help="Existing edited model directory")
    parser.add_argument(
        "--brave",
        default=os.environ.get("BRAVE_PATH")
        or shutil.which("brave-browser")
        or shutil.which("brave")
        or bench.BRAVE,
    )
    parser.add_argument(
        "--gpu",
        default="0",
        help="NVIDIA device index or UUID for the local Docker runtime",
    )
    parser.add_argument(
        "--cdp", help="Existing Brave CDP URL, for an RTX browser on a separate machine"
    )
    args = parser.parse_args()
    if args.out.exists():
        parser.error("Choose a new output directory to keep previous runs.")
    if args.engine == "mlx" and (
        sys.platform != "darwin" or platform.machine() != "arm64" or args.cdp
    ):
        parser.error(
            "The MLX comparison runs on an Apple silicon Mac with a local Brave browser."
        )
    if not args.cdp and not Path(args.brave).is_file():
        parser.error("Install Brave or set --brave to its executable.")
    subprocess.run(
        ["docker", "info", "--format", "{{.ServerVersion}}"],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    grader = bench.WebArenaVerified(
        config=bench.WebArenaVerifiedConfig(
            environments={name: {"urls": [url]} for name, url in bench.URL.items()}
        )
    )
    sites = [s.value for s in grader.get_task(args.id).sites]
    if len(sites) != 1 or sites[0] not in bench.FIXTURE_IMAGES:
        parser.error("Choose a single-site task with a supported public fixture.")
    base = model_directory(catalog["stock"], args.original)
    edit = model_directory(catalog[args.checkpoint], args.edited)
    if args.engine == "mlx":
        subprocess.run(
            [
                sys.executable,
                str(Path(__file__).with_name("run_search_mac.py")),
                str(base),
                str(edit),
                "--id",
                str(args.id),
                "--out",
                str(args.out),
                "--repeats",
                "2",
                "--edited-first",
                "--field-selection",
                "keyboard",
                "--brave",
                args.brave,
            ],
            check=True,
        )
    else:
        from sglang_browser import run_pairs

        run_pairs(
            args,
            grader,
            sites[0],
            {"original": base, "edited": edit},
            {
                "original": catalog["stock"]["shard_sha256"],
                "edited": catalog[args.checkpoint]["shard_sha256"],
            },
        )
    result = json.loads((args.out / "pairs.json").read_text())
    for pair in result["pairs"]:
        ratio = pair["ratio"]
        timing = f"{ratio:.2f}×" if ratio is not None else "no joint pass"
        print(
            f"Run {pair['repeat']}, {pair['order'][0]} first: stock {pair['original_s']:.2f}s (score {pair['original_score']:g}), "
            f"edit {pair['edited_s']:.2f}s (score {pair['edited_score']:g}), {timing}"
        )


if __name__ == "__main__":
    main()
