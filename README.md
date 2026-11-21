# Inkling 2 Mini Fast Browser Use

**8.95× faster on WebArena’s completed-order lookup.**

In the fastest run on an M5 Max MacBook Pro, stock found the correct total in 45.89 seconds. The edited model took 5.13 seconds.

We used weight-space programming to edit four rows in Inkling 2 Mini’s output layer. The model made the same clicks without generating a thinking trace.

[Watch the demo](https://jtc268.github.io/inkling-2-fast-computer-use/) · [Download the tested weights](https://huggingface.co/husky8/Inkling-2-Mini-Fast-Browser-Use/tree/686faa4d1748f0120008ec007dc97677678e1643) · [Reproduce the run](benchmark/REPRODUCE-BROWSER.md) · [Results and weight audit](benchmark/WEBARENA-ORDER-CHECKPOINTS.md)

## BrowserGym accuracy

The default two-row checkpoint passed 6 of 20 MiniWoB++ cases. Stock passed 11. [Task scores](benchmark/BROWSERGYM.md) · [Receipts](evidence/browsergym-receipts.zip)

## Run the form-and-cart demo

If your agent already supports Inkling 2 Mini, use `husky8/Inkling-2-Mini-Fast-Browser-Use` as its model ID. The agent supplies the browser view and executes the commands. The channel edit lives in the checkpoint.

To download the full model with the Hugging Face CLI:

```sh
hf download husky8/Inkling-2-Mini-Fast-Browser-Use --revision d4562716ff6d8d0281bf09814a1df0db570f6be3 --local-dir inkling-browser
```

To run the recorded workflow on Apple silicon with Brave and [uv](https://docs.astral.sh/uv/), clone this repository and run:

```sh
git clone https://github.com/jtc268/inkling-2-fast-computer-use.git
cd inkling-2-fast-computer-use
uv run --python 3.12 playwright install ffmpeg
uv run --python 3.12 python benchmark/run.py
```

The runner downloads the edited model on first use. If you already downloaded it, set `INKLING_EDITED` to that directory. A successful run prints the commands and saves a recording and checked receipt in `runs/`. Use `--mode test --arm both` for all six pairs. This loads both checkpoints and needs more memory than a single run.

To verify the downloaded weights against the upstream shard, run `python benchmark/verify_weights.py /path/to/original /path/to/edited`. The verifier compares every byte and both published SHA-256 digests.

Base model by Thinking Machines Lab. [Original model](https://huggingface.co/thinkingmachines/Inkling-2-Mini) · [Apache 2.0](LICENSE) · [Cursor motion by Cua](benchmark/CUA-LICENSE.txt)
