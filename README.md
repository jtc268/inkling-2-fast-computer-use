# Inkling 2 Fast Browser Use

## Browser-use highlights

[Watch every task in order](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4) · [All 41 chapter times and outcomes](benchmark/ORDERED-BROWSER-VIDEO.md)

Standalone downloads · [Completed-order weights](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/cd27dd36403a165685abd5bf202c326ec9590b20) · [Pending-order weights](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/9f6b8d4dbd3ec39171e38bf528735be4d0b14e66) · [Mac order-lookup trial](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/686faa4d1748f0120008ec007dc97677678e1643) · [Paired grades](benchmark/WEBARENA-ORDER-CHECKPOINTS.md)

**8.95× on the completed-order lookup.** On M5 Max MacBook Pro stock took 45.89 seconds and the cross-device order stop took 5.13 seconds. Both passed again in the opposite order at 8.00×. This task was used to develop the edit. [Fastest paired run](benchmark/WEBARENA-ORDER-CHECKPOINTS.md).

**6.78× on WebArena’s latest-order lookup.** The published search weights took 46.71 seconds and the new stop-row edit took 6.89 seconds on M5 Max. Both passed. Upstream stock failed this task on Mac. [Exact weights and paired runs](benchmark/WEBARENA-ORDER-STOP.md)

**5.18× on one autocomplete case.** Six verified Selenium form submissions measured 2.81× on the repeat. Across the original 20 MiniWoB++ cases, the original passed 11 and the two-row edit passed 6. [Timings, pass counts and real-time films](benchmark/HEADLINERS.md)

Two rows in Inkling 2 Mini’s output layer score the tokens that start a thinking trace or an answer. We swapped them to see whether the model would issue browser commands sooner. It did on a form-and-cart task in Brave.

**[Watch the real-time comparison](https://jtc268.github.io/inkling-2-fast-computer-use/) · [Download the full checkpoint](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use)**

| Six paired runs on a MacBook Pro | Original | Edited |
| --- | ---: | ---: |
| Median time to verified cart | 20.34 s | 7.93 s |
| Median generated thinking tokens per task | 185.5 | 0 |
| Correct form, product and quantity | 6/6 | 6/6 |

[Extended video, 37 seconds](https://jtc268.github.io/inkling-2-fast-computer-use/browser-and-gym.mp4) · The checkout comparison continues into fresh live excerpts from all five BrowserGym environments. Each excerpt plays at 1× and displays its full episode outcome.

The model received numbered control labels as text. It filled two fields, submitted the form, set the quantity and added the item to the cart. The harness opened the product page, followed “View Cart” and checked the receipt. Both checkpoints chose identical commands. Prompts, greedy decoding, reasoning effort (already set to `none`), typing speed and cursor timing were identical. The timer includes inference and browser execution after warmup. The video is a fresh 1× recording of case 03 (16.96 s original, 7.15 s edited). We enlarged both viewports to 1200 × 720 and preserved the dress photo’s aspect ratio in both browsers.

## Replication and WebArena search

34 WebArena IDs have native grades, and 32 have grades for stock and at least one edit. [All pairs for the downloadable checkpoint](benchmark/WEBARENA-FROZEN-CHECKPOINT.md). [New product lookup](benchmark/WEBARENA-PRODUCT-LOOKUP.md). [Shopping search, paired grades and the byte audit](benchmark/WEBARENA-QUERY-TRANSFER.md)

On the fresh MacBook Pro form-and-cart run, the original finished 4/6 and all three edits finished 6/6. On the four common successes, the first release took 6.96 s versus 16.62 s original (2.39×). The four-row edit took 7.04 s (2.36×). On the same filmed case on RTX 5090, the two edits measured 1.03× and 1.18×. [All runs](benchmark/FORM-CART-RECHECK.md) · [Fresh form-to-cart video](https://jtc268.github.io/inkling-2-fast-computer-use/form-cart-recheck.mp4)

On WebArena 274, the four-row edit and original both passed each paired RTX 5090 run, at 1.52×, 1.54× and 1.55× wall-clock speedups. On WebArena 431, all four attempts failed. On 630, both originals passed and both edits failed. The checkpoint swaps the two output-channel rows and adjusts the click and stop rows. [Search experiments](benchmark/WEBARENA-SEARCH.md) · [Watch at 1×](https://jtc268.github.io/inkling-2-fast-computer-use/webarena-search-fast.mp4) · [Download these weights](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/fa1ef63d66ec9d489dc185cd0a8ca5452a28bfe9)

## Ten WebArena tasks on RTX 5090

The original passed 8/30 attempts. The edit passed 5/30. Both earned full credit in 3 matched pairs. This checkpoint changes the click and end-of-generation output rows. [All ten tasks and replay instructions](benchmark/WEBARENA-10.md) · [1× video](https://jtc268.github.io/inkling-2-fast-computer-use/webarena-ten.mp4) · [Standalone weights](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/2c522e2d40dab1e9193e9cb121e1f8e9c222c6c9)

## What changed

Rows 200004 and 200008 in `model.llm.unembed.weight` exchanged places. Those rows score the tokens that open the answer and thinking channels. Only 4,596 BF16 values changed. All other bytes in the 19.53 GB shard matched. [Weight audit](evidence/weight-audit.json)

In the filmed run, the original generated 95 thinking tokens for the form and 100 for the cart. The edit generated zero and went straight to the same commands. On one loaded model, restoring the two rows reproduced the original form response token for token. [Replay](evidence/same-process-replay.json) · [All twelve timed runs](evidence/results.json) · [Raw recordings](https://github.com/jtc268/inkling-2-fast-computer-use/releases/download/v1.0/raw-runs.zip)

There is also a prompt-only shortcut. On the development case, the original took 16.82 s with the shared prompt and 7.57 s with its answer channel prefilled. The edited checkpoint took 6.94 s with the shared prompt. The six main pairs are variants of the same two pages. Accuracy on harder tasks, screenshot loops and other browsers remains unmeasured. [Prompt control](evidence/dev-original-prefill.json)

## BrowserGym accuracy

The original passed 11/20 cases and the edit passed 6/20. Both passed 5. The original alone passed 6, the edit alone passed 1, and both failed 8. Across the 5 joint successes, median completion time was 19.86 s original and 3.84 s edited. Four matched seeds per environment.

| MiniWoB++ task | Original | Edited |
| --- | ---: | ---: |
| Email inbox | 3/4 | 3/4 |
| Autocomplete | 2/4 | 3/4 |
| Social feed | 3/4 | 0/4 |
| Date picker | 3/4 | 0/4 |
| Flight booking | 0/4 | 0/4 |

The model read a fresh text description of the DOM after each action. BrowserGym graded the outcome. Each case allowed 16 decisions. [Run details](benchmark/BROWSERGYM.md) · [Scores](evidence/browsergym-summary.json) · [All 40 receipts](evidence/browsergym-receipts.zip)

## Try it

If your agent already supports Inkling 2 Mini, use `husky8/Inkling-2-Fast-Computer-Use` as its model ID. The agent supplies the browser view and executes the commands. The channel edit lives in the checkpoint.

To download the full model with the Hugging Face CLI:

```sh
hf download husky8/Inkling-2-Fast-Computer-Use --local-dir inkling-browser
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
