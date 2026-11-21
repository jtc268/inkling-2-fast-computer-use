# Repeating a shopping search after a weight edit

The previous checkpoint failed its first unseen green-tea search. It filled the field 11 times and never submitted it. We used that trace to revise the click and end-of-generation output rows. The original thinking and answer marker swap is also present. We kept prompts, decoding, the action parser, mouse animation and typing speed fixed. The model read rendered page text and controls in Brave.

We adjusted the two rows directly using saved model states and ten synthetic search queries. The edit raised the score for a click after a filled field and the native stop token after a complete command. We constrained changes on saved decisions from three prior searches. There was no gradient training. Other prompts can still select different tokens.

| Device | WebArena task | Role | Run | Stock | Edited | Stock time ÷ edited time |
|---|---|---|---:|---:|---:|---:|
| M5 Max MacBook Pro | 278 · Green tea bags | used to develop this edit | 1 | 20.26 s · pass | 6.02 s · pass | 3.36× |
| M5 Max MacBook Pro | 278 · Green tea bags | used to develop this edit | 2 | 20.29 s · pass | 6.53 s · pass | 3.11× |
| M5 Max MacBook Pro | 274 · USB Wi-Fi adapter | earlier control | 1 | 14.46 s · pass | 5.07 s · pass | 2.85× |
| M5 Max MacBook Pro | 274 · USB Wi-Fi adapter | earlier control | 2 | 14.53 s · pass | 5.25 s · pass | 2.77× |
| M5 Max MacBook Pro | 276 · Switch accessories | earlier control | 1 | 14.10 s · pass | 6.12 s · pass | 2.30× |
| M5 Max MacBook Pro | 276 · Switch accessories | earlier control | 2 | 13.49 s · pass | 5.73 s · pass | 2.36× |
| M5 Max MacBook Pro | 277 · iPhone 13 batteries | protected earlier win | 1 | 17.64 s · pass | 6.47 s · pass | 2.73× |
| M5 Max MacBook Pro | 277 · iPhone 13 batteries | protected earlier win | 2 | 17.69 s · pass | 6.14 s · pass | 2.88× |
| M5 Max MacBook Pro | 630 · Ask for headphone recommendations | earlier forum control, different interface | 1 | 89.24 s · fail | 0.96 s · fail | — |
| M5 Max MacBook Pro | 275 · Xbox | first unseen search | 1 | 17.98 s · pass | 4.71 s · pass | 3.81× |
| M5 Max MacBook Pro | 275 · Xbox | first unseen search | 2 | 17.78 s · pass | 5.67 s · pass | 3.14× |
| RTX 5090 | 278 · Green tea bags | used to develop this edit | 1 | 6.92 s · pass | 11.51 s · fail | — |
| RTX 5090 | 276 · Switch accessories | earlier control | 1 | 5.32 s · pass | 3.70 s · pass | 1.44× |

## Where the time went

The browser clock covers observation, model inference and action execution. The columns below split the first take on each device into inference and everything else. Token counts cover all decisions, including invalid commands.

| Device | Task | Generated tokens, stock → edit | Decisions, stock → edit | Inference seconds, stock → edit | Other seconds, stock → edit |
|---|---:|---:|---:|---:|---:|
| M5 Max MacBook Pro | 278 | 498 → 26 | 5 → 3 | 16.35 → 2.86 | 3.91 → 3.16 |
| M5 Max MacBook Pro | 274 | 377 → 24 | 3 → 3 | 12.11 → 2.76 | 2.35 → 2.30 |
| M5 Max MacBook Pro | 276 | 312 → 23 | 3 → 3 | 10.77 → 3.27 | 3.32 → 2.86 |
| M5 Max MacBook Pro | 277 | 413 → 26 | 4 → 3 | 14.54 → 3.46 | 3.10 → 3.01 |
| M5 Max MacBook Pro | 630 | 3202 → 7 | 12 → 1 | 86.75 → 0.96 | 2.49 → 0.00 |
| M5 Max MacBook Pro | 275 | 491 → 22 | 5 → 3 | 15.80 → 2.55 | 2.18 → 2.16 |
| RTX 5090 | 278 | 387 → 82 | 4 → 8 | 3.38 → 2.10 | 3.54 → 9.41 |
| RTX 5090 | 276 | 294 → 22 | 3 → 3 | 2.34 → 0.64 | 2.98 → 3.06 |

On the RTX Switch-accessories run, stock spent 2.98 s outside inference. If that time stayed fixed and generation took zero seconds, the maximum time ratio on that stock run would be 1.78×. A different action sequence can change the time spent in the browser.

On the RTX green-tea task, both arms used the same Windows Brave harness. The edit requested the same fill several times. In a separate input-field check, the shortcut sent by Playwright on the Mac left a collapsed selection in the Windows field. Retyping inserted duplicate text. Explicit Ctrl+A and Playwright’s field selection both replaced it correctly. The recorded failure includes both effects. [Windows input-field check](../evidence/webarena-query-transfer/windows-field-control.json)

With the CUDA checkpoint and the filled green-tea screen fixed, the history spelling `F7` produced `F7 green tea bag for weight loss` twice. The spelling `F 7` produced `F7 green tea bag for weight loss` twice. Only the ASCII space changed. These are single-decision probes. [Recorded counterfactuals](../evidence/webarena-query-transfer/cuda-probe-results.json)

The native grader reproduced all 26 outcomes. Stock passed 12/13 and the edit passed 11/13. Only paired passes have a speed ratio.

Green tea was used to develop this revision. Its earlier unseen failure remains in the previous report. The search tasks share the same WebArena template. The forum control exercises a different site when the shopping regressions pass.

The checkpoint changes 9,184 BF16 values in output rows 34, 200004, 200006 and 200008. The complete shard SHA-256 is `9f54b7bc5c2d2408f19d79cc3bcce1fd456c96bcdf1f4e25bfcb6d3c608dc47e`.

[Earlier checkpoint and its unseen failure](WEBARENA-SEARCH-COMMAND.md) · [All timings](../evidence/webarena-query-transfer/results.json) · [Replayable receipts](../evidence/webarena-query-transfer/receipts.zip) · [Full browser recordings](../evidence/webarena-query-transfer/recordings.zip) · [Byte audit](../evidence/webarena-query-transfer/weight-audit.json)

```sh
python benchmark/replay_search.py evidence/webarena-query-transfer/receipts.zip
```

On M5 Max, both models passed 10/10 matched runs across 5 shopping queries that share WebArena template 212. Passing pairs ran 2.30–3.81× as fast.

Xbox was the final ungraded task ID in the five-query shopping template. Its task ID and frozen checkpoint were recorded before the first attempt. Only Xbox was a first-exposure test for this revision.

On the Mac forum post, stock scored 0 and the edit scored 0. The edited model declared navigation complete from the home page. It did not create a post.

For a fresh local browser timing, install the Inkling-compatible MLX runtime, WebArena-Verified 1.2.3, Docker and Brave. The runner selects the official shopping or forum fixture for the requested task and reverses the checkpoint order on the second pair.

```sh
python benchmark/run_search_mac.py ORIGINAL EDITED --id 278 --repeats 2 --field-selection keyboard --out green-tea
python benchmark/run_search_mac.py ORIGINAL EDITED --id 630 --repeats 2 --field-selection keyboard --out forum-post
```

These commands reproduce the recorded selection method. The runner defaults to portable field selection for fresh experiments.

[Download the standalone weights](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/ba75284970e339d5cb957a206b3d4be6ce8d5f7d).

The four published BF16 rows and stock weights reproduce the complete edited shard hash. To check it locally, run

```sh
python benchmark/verify_row_payload.py ORIGINAL evidence/webarena-query-transfer/rows.npz evidence/webarena-query-transfer/weight-audit.json
```
