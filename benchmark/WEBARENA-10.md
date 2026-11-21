# Inkling 2 Mini on ten WebArena tasks

The original passed 8/30 attempts. The edit passed 5/30. Both earned full credit in 3 matched pairs. Each task ran three times per checkpoint on the same physical RTX 5090. A third 5090 repeated all ten with the original and passed 2/10.

**Search for a USB Wi-Fi adapter (WebArena 274).** The recorded pair took 4.75 s original and 4.71 s edited. Grader scores were 1 and 1. [Watch at 1×](https://jtc268.github.io/inkling-2-fast-computer-use/webarena-ten.mp4) · [Download this checkpoint](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/2c522e2d40dab1e9193e9cb121e1f8e9c222c6c9)

**Save a product to a wishlist (WebArena 516).** The edit completed 1/3 runs and the original completed 0/3. In this recording the edit completed in 3.06 s and the original failed. An unsuccessful attempt has no completion-time ratio. [Watch the completion difference at 1×](https://jtc268.github.io/inkling-2-fast-computer-use/webarena-ten-completion.mp4)

In the filmed wishlist run, the original actually sent five add-to-wishlist requests and reached the decision limit without a final answer. The edit sent one and returned the required success response. This shows a difference in finishing the task cleanly.

| ID | Task | Original passes | Edited passes | Joint passes | Original time | Edited time | Original / edited |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 96 | Track the latest order | 1/3 | 0/3 | 0/3 | — | — | — |
| 269 | Filter shoes under $25 | 0/3 | 0/3 | 0/3 | — | — | — |
| 274 | Search for a USB Wi-Fi adapter | 3/3 | 3/3 | 3/3 | 4.74 s | 4.71 s | 1.00× |
| 313 | Find customer service | 0/3 | 0/3 | 0/3 | — | — | — |
| 431 | Add the lowest-unit-price item to the cart | 0/3 | 0/3 | 0/3 | — | — | — |
| 516 | Save a product to a wishlist | 0/3 | 1/3 | 0/3 | — | — | — |
| 399 | Edit a forum profile | 1/3 | 1/3 | 0/3 | — | — | — |
| 404 | Upvote the newest book post | 0/3 | 0/3 | 0/3 | — | — | — |
| 595 | Follow the space forum | 0/3 | 0/3 | 0/3 | — | — | — |
| 630 | Ask for headphone recommendations | 3/3 | 0/3 | 0/3 | — | — | — |

Times are medians over paired full-credit completions. A ratio above 1 means the edit finished sooner. A dash means there was no pair of successful completions. The individual scores and wall times below include failures.

## What changed

A closed-form weight edit changed 4,547 BF16 values in two rows of the language-model output matrix. Row 34 scores the token `C`, which begins a click in this browser driver. Row 200006 scores the native end-of-generation token. The calculation used synthetic browser observations and preserved the upstream rows for thinking and answering. On four calibration examples the original produced two valid target actions and the edit produced four. On five separate synthetic examples each produced four. [Byte audit](../evidence/webarena-ten/weight-audit.json) · [Calibration and separate checks](../evidence/webarena-ten/synthetic-checks.json)

## Run conditions

Ten consumer tasks were selected from previously explored WebArena cases and frozen before the weights were edited. The ten span the shopping and forum environments. Each episode reset the pinned fixture, opened a fresh Brave context and recorded a network trace. Inkling received visible text, numbered controls and tab titles. The prompt, `none` reasoning effort, greedy decoder, 512-token ceiling, 12-decision limit, 360 ms cursor glide and 25 ms typing delay were identical. Timing started after model warmup and page load, included all model decisions and browser actions, and ended before grading. Only an official score of 1 counts as a pass.

The paired cards loaded each checkpoint in the same SGLang image with 8,192 context. Opposite cards started with opposite checkpoints, and arm order reversed in the second repetition. First-step text observations were byte-identical in 29/30 pairs. The third card used an existing upstream server with a larger context limit and contributed only independent scores. Three repetitions probe repeatability on the same fixed initial tasks. They do not estimate population accuracy.

A temporary loss of the Linux fixture connection interrupted the USB4 lane. Its second and third rounds used the same pinned site images hosted on the Mac. Every timing pair used the same fixture host for both arms. One additional, unpaired original run on task 269 scored 0 before the interruption. Its [receipt](../evidence/webarena-ten/infrastructure.zip) is preserved separately.

The video uses complete browser viewports at 1×. We selected the task with the most paired successes, then the greatest ratio of median completion times. The filmed repetition had the closest ratio to that task’s median-time ratio. The clock freezes at each receipt’s measured finish.

## Individual scores and seconds

Each cell contains the official score followed by wall time.

| ID | Run | Original | Edited |
| ---: | ---: | ---: | ---: |
| 96 | 1 | 1 · 11.65 s | 0 · 17.00 s |
| 96 | 2 | 0 · 17.77 s | 0 · 11.47 s |
| 96 | 3 | 0 · 12.32 s | 0 · 16.27 s |
| 269 | 1 | 0 · 31.29 s | 0 · 27.34 s |
| 269 | 2 | 0 · 22.44 s | 0 · 27.31 s |
| 269 | 3 | 0 · 31.03 s | 0 · 26.28 s |
| 274 | 1 | 1 · 4.71 s | 1 · 4.77 s |
| 274 | 2 | 1 · 4.74 s | 1 · 4.70 s |
| 274 | 3 | 1 · 4.75 s | 1 · 4.71 s |
| 313 | 1 | 0 · 15.73 s | 0 · 17.03 s |
| 313 | 2 | 0 · 16.97 s | 0 · 17.22 s |
| 313 | 3 | 0 · 15.74 s | 0 · 20.90 s |
| 431 | 1 | 0 · 29.62 s | 0 · 18.25 s |
| 431 | 2 | 0 · 14.22 s | 0 · 18.70 s |
| 431 | 3 | 0 · 17.03 s | 0 · 18.53 s |
| 516 | 1 | 0 · 24.60 s | 1 · 3.06 s |
| 516 | 2 | 0 · 31.24 s | 0 · 20.77 s |
| 516 | 3 | 0 · 24.51 s | 0 · 27.68 s |
| 399 | 1 | 0 · 5.17 s | 0 · 5.20 s |
| 399 | 2 | 0 · 5.17 s | 1 · 9.34 s |
| 399 | 3 | 1 · 8.88 s | 0 · 5.26 s |
| 404 | 1 | 0 · 29.58 s | 0 · 27.15 s |
| 404 | 2 | 0 · 29.71 s | 0 · 26.84 s |
| 404 | 3 | 0 · 29.57 s | 0 · 26.89 s |
| 595 | 1 | 0 · 24.93 s | 0 · 24.44 s |
| 595 | 2 | 0 · 24.96 s | 0 · 24.19 s |
| 595 | 3 | 0 · 31.41 s | 0 · 24.29 s |
| 630 | 1 | 1 · 26.77 s | 0 · 10.26 s |
| 630 | 2 | 1 · 19.52 s | 0 · 10.34 s |
| 630 | 3 | 1 · 19.30 s | 0 · 12.60 s |

## Replay the grades

From the repository root, use a Python environment with `webarena-verified==1.2.3`. The archive retains the model actions, final answers, raw HAR hashes and filtered network events. The offline grader reproduced all 70 live grades.

```sh
python benchmark/replay_ten.py evidence/webarena-ten/receipts.zip
```

[All scores](../evidence/webarena-ten/results.json) · [Replay archive](../evidence/webarena-ten/receipts.zip) · [Frozen task IDs](../evidence/webarena-ten-panel.json) · [Exact prompt and limits](../evidence/webarena-ten/protocol.json) · [Video evidence](../evidence/webarena-ten/video.json)

To repeat the browser run, use the pinned fixtures and environment documented in [WebArena setup](WEBARENA.md). Serve the original checkpoint, then the candidate on the same device. Run the following command for each checkpoint with the corresponding model ID and arm. `--ids` is optional.

```sh
python benchmark/run_webarena_ten.py --endpoint http://127.0.0.1:30000 \
  --model-id "$SERVED_MODEL" --arm "$ARM" --gpu-uuid "$GPU_UUID" \
  --tokenizer "$CHECKPOINT" --out runs/ten
```
