# Inkling 2 Mini Fast Browser Use

**8.95× faster on WebArena’s completed-order lookup.**

WebArena task 190 asks for the total of the most recent completed order. In the fastest paired run on an M5 Max MacBook Pro, both models made the same clicks, returned $65.32 and earned full credit.

| WebArena 190 · Completed-order lookup | Original Inkling 2 Mini | Edited Inkling 2 Mini |
|---|---:|---:|
| Total task time | 45.89 s | 5.13 s |
| Model inference time | 43.03 s | 2.84 s |
| Generated tokens | 1,555 | 28 |
| Thinking tokens | 1,509 | 0 |

**Weight-space programming.** We edited four rows in Inkling 2 Mini’s output matrix, `model.llm.unembed.weight`, without additional training. We swapped the rows for answer text (`200004`) and thinking (`200008`), then adjusted the rows for the click command `C` (`34`) and end of generation (`200006`). A byte comparison found 9,192 changed BF16 values across those four rows. [Weight audit](https://github.com/jtc268/inkling-2-fast-computer-use/blob/main/evidence/webarena-order-checkpoints/complete-cross/weight-audit.json)

**Method.** Both checkpoints ran in MLX and read visible text and numbered controls in Brave. We reset the storefront, warmed each model and used the same prompt, greedy decoding, reasoning effort (`none`) and cursor timing. Total time includes inference and browser actions. We developed the edit on this task and tested both run orders.

[Watch the demo](https://jtc268.github.io/inkling-2-fast-computer-use/) · [Download the tested weights](https://huggingface.co/husky8/Inkling-2-Mini-Fast-Browser-Use/tree/686faa4d1748f0120008ec007dc97677678e1643) · [Reproduce the run](benchmark/REPRODUCE-BROWSER.md) · [Paired runs and grades](benchmark/WEBARENA-ORDER-CHECKPOINTS.md)

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
