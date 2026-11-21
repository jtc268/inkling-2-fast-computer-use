"""Run one matched BrowserGym case using the published MLX inference driver."""
import argparse
import json
import os
from pathlib import Path

import gym as benchmark


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=benchmark.TASKS, default="use-autocomplete")
    parser.add_argument("--seed", type=int, default=103)
    parser.add_argument("--output", type=Path, default=Path("headline-run"))
    args = parser.parse_args()
    # Each call gets fresh results. Preserve earlier evidence if the directory exists.
    args.output.mkdir(parents=True, exist_ok=False)
    results = {}
    for arm in ("edited", "original"):
        worker = benchmark.inference_proc(os.environ["INKLING_" + arm.upper()])
        try:
            benchmark.evaluate(args.task, args.seed, arm, worker, args.output)
        finally:
            worker.stdin.close()
            worker.wait()
        receipt = args.output / f"{args.task}-{args.seed}-{arm}.json"
        results[arm] = json.loads(receipt.read_text())
    baseline, candidate = results["original"], results["edited"]
    if baseline["goal"] != candidate["goal"]:
        raise ValueError("The two runs received different goals")
    if baseline.get("reward", 0) > 0 and candidate.get("reward", 0) > 0:
        a, b = baseline["elapsed_s"], candidate["elapsed_s"]
        print(f"Both passed. Original {a:.2f}s, edited {b:.2f}s, {a/b:.2f}×, {a-b:.2f}s saved.")
    else:
        print(f"Passes: original {baseline['success']}, edited {candidate['success']}.")


if __name__ == "__main__":
    main()
