"""Check whether two edited checkpoints received identical messages at every browser decision."""
import argparse
import json
from pathlib import Path
from zipfile import ZipFile


def compare(archive_path, pairs_path, previous, current, device, tasks):
    pairs = json.loads(pairs_path.read_text())["pairs"]
    with ZipFile(archive_path) as archive:
        timing = {}
        for name in archive.namelist():
            if name.startswith("timing/"):
                record = json.loads(archive.read(name))
                timing[record["receipt_sha256"]] = record

    comparisons = []
    for task in tasks:
        for first in ("edited", "original"):
            episodes = []
            for checkpoint in (previous, current):
                matches = [p for p in pairs if p["checkpoint"] == checkpoint and p["task"] == task
                           and p["device"] == device and p["order"][0] == first and p["comparable"]]
                if len(matches) != 1:
                    raise ValueError(f"Expected one comparable {checkpoint} run on task {task}, {first} first.")
                episodes.append(timing[matches[0]["edited"]["receipt_sha256"]])
            before, after = episodes
            if before["shard_sha256"] == after["shard_sha256"] or min(before["score"], after["score"]) != 1:
                raise ValueError(f"Task {task} needs two distinct passing checkpoints.")
            counts = []
            for step, (a, b) in enumerate(zip(before["steps"], after["steps"], strict=True), 1):
                if a["message_sha256"] != b["message_sha256"] or a["action"] != b["action"]:
                    raise ValueError(f"Task {task}, {first} first, decision {step} has different input or action.")
                counts.append((a["generated"], b["generated"]))
            comparisons.append((task, first, counts))
    return comparisons


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("pairs", type=Path)
    parser.add_argument("previous")
    parser.add_argument("current")
    parser.add_argument("--device", required=True)
    parser.add_argument("--tasks", nargs="+", type=int, required=True)
    args = parser.parse_args()
    for task, first, counts in compare(args.archive, args.pairs, args.previous, args.current, args.device, args.tasks):
        print(f"WebArena {task}, {first} first. {len(counts)} matching decisions. Generated tokens per decision {counts}.")
