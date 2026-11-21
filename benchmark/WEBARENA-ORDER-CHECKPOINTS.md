# Frozen order checkpoints

Each row is a fresh pair in Brave. A speedup requires two native WebArena-Verified passes on matched fixtures. The full-task clock includes model generation and browser actions. Both arms receive visible page text and numbered controls, use the same cursor timing, and decode greedily with a 512-token limit. Both set the chat template to `reasoning_effort="none"`. The model can still emit thinking tokens at that setting.

| Checkpoint | Hardware | Baseline | Task IDs | Baseline passes | Edited passes | IDs at ≥2× in both orders |
|---|---|---|---|---:|---:|---|
| Cross-device order stop | M5 Max MacBook Pro | Published search weights | 96 | 2/2 | 2/2 | 96 |
| Cross-device order stop | M5 Max MacBook Pro | Upstream stock | 188, 189, 190, 274 | 8/8 | 8/8 | 188, 189, 190 |
| Cross-device order stop | RTX 5090 | Upstream stock | 190 | 2/2 | 0/2 | — |
| Completed-order stop | M5 Max MacBook Pro | Published search weights | 96 | 2/2 | 2/2 | 96 |
| Completed-order stop | M5 Max MacBook Pro | Upstream stock | 188, 189, 190, 191, 231, 274, 275, 276, 277, 278, 283 | 16/22 | 18/22 | 188, 189, 190, 274, 275, 276, 277, 278 |
| Completed-order stop | RTX 5090 | Upstream stock | 190, 191, 275 | 4/6 | 4/6 | — |
| Windows command-stop | M5 Max MacBook Pro | Upstream stock | 188, 274 | 4/4 | 4/4 | 188 |
| Windows command-stop | RTX 5090 | Upstream stock | 188 | 2/2 | 2/2 | 188 |
| Order-history routing trial | M5 Max MacBook Pro | Upstream stock | 189, 190 | 3/4 | 4/4 | 190 |
| Order-history routing trial | RTX 5090 | Upstream stock | 188, 189, 190, 191, 275 | 8/10 | 8/10 | 188, 189, 190 |
| Guarded reasoning trial | RTX 5090 | Upstream stock | 190 | 2/2 | 2/2 | — |
| Pending click + stop | M5 Max MacBook Pro | Published search weights | 96 | 2/2 | 2/2 | 96 |
| Pending click + stop | M5 Max MacBook Pro | Upstream stock | 62, 188, 189, 190, 274, 275, 276 | 12/14 | 12/14 | 188, 189, 190, 274, 275 |
| Pending click + stop | RTX 5090 | Upstream stock | 188, 189 | 4/4 | 4/4 | 189 |
| Focused search-field edit | M5 Max MacBook Pro | Upstream stock | 283 | 0/2 | 0/2 | — |
| Search field-state edit | M5 Max MacBook Pro | Upstream stock | 283 | 0/2 | 0/2 | — |
| Search submit stop | RTX 5090 | Upstream stock | 275 | 2/2 | 2/2 | — |

| Checkpoint | Task | Hardware | Baseline | Ran first | Baseline time | Edited time | Speedup |
|---|---:|---|---|---|---:|---:|---:|
| Windows command-stop | 188 | RTX 5090 | Upstream stock | Edited | 5.45s · fail | 3.16s · pass | Excluded · broken fixture link |
| Windows command-stop | 188 | RTX 5090 | Upstream stock | Baseline | 6.86s · pass | 2.65s · pass | 2.59× |
| Windows command-stop | 188 | RTX 5090 | Upstream stock | Edited | 6.47s · pass | 3.12s · pass | 2.07× |
| Windows command-stop | 188 | M5 Max MacBook Pro | Upstream stock | Edited | 27.99s · pass | 5.22s · pass | 5.36× |
| Windows command-stop | 188 | M5 Max MacBook Pro | Upstream stock | Baseline | 29.27s · pass | 7.66s · pass | 3.82× |
| Windows command-stop | 274 | M5 Max MacBook Pro | Upstream stock | Edited | 15.23s · pass | 6.70s · pass | 2.27× |
| Windows command-stop | 274 | M5 Max MacBook Pro | Upstream stock | Baseline | 14.14s · pass | 8.33s · pass | 1.70× |
| Pending click + stop | 189 | M5 Max MacBook Pro | Upstream stock | Edited | 24.01s · pass | 5.12s · pass | 4.69× |
| Pending click + stop | 189 | M5 Max MacBook Pro | Upstream stock | Baseline | 23.86s · pass | 4.16s · pass | 5.74× |
| Pending click + stop | 189 | RTX 5090 | Upstream stock | Edited | 12.52s · pass | 3.59s · pass | 3.49× |
| Pending click + stop | 189 | RTX 5090 | Upstream stock | Baseline | 6.85s · pass | 2.87s · pass | 2.39× |
| Pending click + stop | 188 | M5 Max MacBook Pro | Upstream stock | Edited | 27.98s · pass | 5.16s · pass | 5.42× |
| Pending click + stop | 188 | M5 Max MacBook Pro | Upstream stock | Baseline | 28.35s · pass | 5.33s · pass | 5.32× |
| Pending click + stop | 274 | M5 Max MacBook Pro | Upstream stock | Edited | 16.20s · pass | 6.29s · pass | 2.58× |
| Pending click + stop | 274 | M5 Max MacBook Pro | Upstream stock | Baseline | 15.69s · pass | 7.27s · pass | 2.16× |
| Pending click + stop | 275 | M5 Max MacBook Pro | Upstream stock | Edited | 18.40s · pass | 4.76s · pass | 3.87× |
| Pending click + stop | 275 | M5 Max MacBook Pro | Upstream stock | Baseline | 18.27s · pass | 5.32s · pass | 3.44× |
| Pending click + stop | 276 | M5 Max MacBook Pro | Upstream stock | Edited | 14.04s · pass | 5.99s · pass | 2.34× |
| Pending click + stop | 276 | M5 Max MacBook Pro | Upstream stock | Baseline | 14.03s · pass | 7.86s · pass | 1.79× |
| Pending click + stop | 96 | M5 Max MacBook Pro | Published search weights | Edited | 46.79s · pass | 7.67s · pass | 6.10× |
| Pending click + stop | 96 | M5 Max MacBook Pro | Published search weights | Baseline | 48.27s · pass | 7.35s · pass | 6.57× |
| Pending click + stop | 188 | RTX 5090 | Upstream stock | Edited | 5.76s · pass | 2.96s · pass | 1.94× |
| Pending click + stop | 188 | RTX 5090 | Upstream stock | Baseline | 6.62s · pass | 2.73s · pass | 2.43× |
| Pending click + stop | 190 | M5 Max MacBook Pro | Upstream stock | Edited | 45.50s · pass | 18.33s · pass | 2.48× |
| Pending click + stop | 190 | M5 Max MacBook Pro | Upstream stock | Baseline | 49.00s · pass | 19.75s · pass | 2.48× |
| Pending click + stop | 62 | M5 Max MacBook Pro | Upstream stock | Edited | 75.50s · fail | 0.72s · fail | — |
| Pending click + stop | 62 | M5 Max MacBook Pro | Upstream stock | Baseline | 76.97s · fail | 1.01s · fail | — |
| Completed-order stop | 190 | M5 Max MacBook Pro | Upstream stock | Edited | 45.34s · pass | 5.19s · pass | 8.73× |
| Completed-order stop | 190 | M5 Max MacBook Pro | Upstream stock | Baseline | 46.59s · pass | 6.01s · pass | 7.75× |
| Completed-order stop | 190 | RTX 5090 | Upstream stock | Edited | 7.22s · pass | 9.29s · pass | 0.78× |
| Completed-order stop | 190 | RTX 5090 | Upstream stock | Baseline | 12.15s · pass | 8.93s · pass | 1.36× |
| Completed-order stop | 191 | RTX 5090 | Upstream stock | Edited | 11.73s · fail | 3.01s · grader error | — |
| Completed-order stop | 191 | RTX 5090 | Upstream stock | Baseline | 9.14s · fail | 2.70s · grader error | — |
| Completed-order stop | 275 | RTX 5090 | Upstream stock | Edited | 4.81s · pass | 6.08s · pass | 0.79× |
| Completed-order stop | 275 | RTX 5090 | Upstream stock | Baseline | 5.01s · pass | 6.08s · pass | 0.82× |
| Cross-device order stop | 190 | RTX 5090 | Upstream stock | Edited | 9.33s · pass | 3.29s · fail | — |
| Cross-device order stop | 190 | RTX 5090 | Upstream stock | Baseline | 12.41s · pass | 3.19s · fail | — |
| Guarded reasoning trial | 190 | RTX 5090 | Upstream stock | Edited | 5.72s · pass | 6.79s · pass | 0.84× |
| Guarded reasoning trial | 190 | RTX 5090 | Upstream stock | Baseline | 10.33s · pass | 3.34s · pass | 3.09× |
| Order-history routing trial | 190 | RTX 5090 | Upstream stock | Edited | 9.88s · pass | 4.86s · pass | 2.03× |
| Order-history routing trial | 190 | RTX 5090 | Upstream stock | Baseline | 10.09s · pass | 4.64s · pass | 2.18× |
| Order-history routing trial | 189 | RTX 5090 | Upstream stock | Edited | 6.30s · pass | 2.92s · pass | 2.16× |
| Order-history routing trial | 189 | RTX 5090 | Upstream stock | Baseline | 6.77s · pass | 2.87s · pass | 2.36× |
| Order-history routing trial | 188 | RTX 5090 | Upstream stock | Edited | 6.31s · pass | 2.82s · pass | 2.23× |
| Order-history routing trial | 188 | RTX 5090 | Upstream stock | Baseline | 9.69s · pass | 2.75s · pass | 3.53× |
| Order-history routing trial | 191 | RTX 5090 | Upstream stock | Edited | 8.42s · fail | 4.19s · grader error | — |
| Order-history routing trial | 191 | RTX 5090 | Upstream stock | Baseline | 12.57s · fail | 11.34s · grader error | — |
| Order-history routing trial | 275 | RTX 5090 | Upstream stock | Edited | 5.02s · pass | 6.35s · pass | 0.79× |
| Order-history routing trial | 275 | RTX 5090 | Upstream stock | Baseline | 4.64s · pass | 6.01s · pass | 0.77× |
| Search submit stop | 275 | RTX 5090 | Upstream stock | Edited | 4.78s · pass | 3.29s · pass | 1.45× |
| Search submit stop | 275 | RTX 5090 | Upstream stock | Baseline | 4.75s · pass | 3.00s · pass | 1.58× |
| Order-history routing trial | 189 | M5 Max MacBook Pro | Upstream stock | Edited | 24.47s · pass | 5.35s · pass | 4.57× |
| Order-history routing trial | 189 | M5 Max MacBook Pro | Upstream stock | Baseline | 10.68s · fail | 5.62s · pass | — |
| Order-history routing trial | 190 | M5 Max MacBook Pro | Upstream stock | Edited | 33.89s · pass | 5.24s · pass | 6.46× |
| Order-history routing trial | 190 | M5 Max MacBook Pro | Upstream stock | Baseline | 47.18s · pass | 5.76s · pass | 8.19× |
| Focused search-field edit | 283 | M5 Max MacBook Pro | Upstream stock | Edited | 87.93s · fail | 18.77s · fail | — |
| Focused search-field edit | 283 | M5 Max MacBook Pro | Upstream stock | Baseline | 91.99s · fail | 19.45s · fail | — |
| Search field-state edit | 283 | M5 Max MacBook Pro | Upstream stock | Edited | 83.21s · fail | 35.93s · fail | — |
| Search field-state edit | 283 | M5 Max MacBook Pro | Upstream stock | Baseline | 83.12s · fail | 36.31s · fail | — |
| Cross-device order stop | 188 | M5 Max MacBook Pro | Upstream stock | Edited | 29.22s · pass | 5.69s · pass | 5.14× |
| Cross-device order stop | 188 | M5 Max MacBook Pro | Upstream stock | Baseline | 28.38s · pass | 4.97s · pass | 5.71× |
| Cross-device order stop | 189 | M5 Max MacBook Pro | Upstream stock | Edited | 33.13s · pass | 5.25s · pass | 6.31× |
| Cross-device order stop | 189 | M5 Max MacBook Pro | Upstream stock | Baseline | 34.83s · pass | 5.74s · pass | 6.07× |
| Cross-device order stop | 190 | M5 Max MacBook Pro | Upstream stock | Edited | 45.89s · pass | 5.13s · pass | 8.95× |
| Cross-device order stop | 190 | M5 Max MacBook Pro | Upstream stock | Baseline | 44.67s · pass | 5.58s · pass | 8.00× |
| Cross-device order stop | 274 | M5 Max MacBook Pro | Upstream stock | Edited | 14.46s · pass | 4.65s · pass | 3.11× |
| Cross-device order stop | 274 | M5 Max MacBook Pro | Upstream stock | Baseline | 14.47s · pass | 9.14s · pass | 1.58× |
| Cross-device order stop | 96 | M5 Max MacBook Pro | Published search weights | Edited | 48.34s · pass | 6.91s · pass | 7.00× |
| Cross-device order stop | 96 | M5 Max MacBook Pro | Published search weights | Baseline | 54.03s · pass | 7.76s · pass | 6.96× |
| Completed-order stop | 188 | M5 Max MacBook Pro | Upstream stock | Edited | 45.75s · pass | 6.44s · pass | 7.10× |
| Completed-order stop | 188 | M5 Max MacBook Pro | Upstream stock | Baseline | 29.18s · pass | 4.84s · pass | 6.02× |
| Completed-order stop | 189 | M5 Max MacBook Pro | Upstream stock | Edited | 33.17s · pass | 5.30s · pass | 6.25× |
| Completed-order stop | 189 | M5 Max MacBook Pro | Upstream stock | Baseline | 24.86s · pass | 5.87s · pass | 4.24× |
| Completed-order stop | 231 | M5 Max MacBook Pro | Upstream stock | Edited | 31.38s · fail | 5.12s · pass | — |
| Completed-order stop | 231 | M5 Max MacBook Pro | Upstream stock | Baseline | 35.65s · fail | 7.38s · pass | — |
| Completed-order stop | 274 | M5 Max MacBook Pro | Upstream stock | Edited | 15.15s · pass | 7.10s · pass | 2.13× |
| Completed-order stop | 274 | M5 Max MacBook Pro | Upstream stock | Baseline | 14.35s · pass | 5.39s · pass | 2.66× |
| Completed-order stop | 275 | M5 Max MacBook Pro | Upstream stock | Edited | 18.87s · pass | 7.17s · pass | 2.63× |
| Completed-order stop | 275 | M5 Max MacBook Pro | Upstream stock | Baseline | 20.92s · pass | 5.12s · pass | 4.09× |
| Completed-order stop | 276 | M5 Max MacBook Pro | Upstream stock | Edited | 14.80s · pass | 5.64s · pass | 2.63× |
| Completed-order stop | 276 | M5 Max MacBook Pro | Upstream stock | Baseline | 14.73s · pass | 5.50s · pass | 2.68× |
| Completed-order stop | 277 | M5 Max MacBook Pro | Upstream stock | Edited | 19.38s · pass | 5.88s · pass | 3.30× |
| Completed-order stop | 277 | M5 Max MacBook Pro | Upstream stock | Baseline | 20.64s · pass | 6.60s · pass | 3.13× |
| Completed-order stop | 278 | M5 Max MacBook Pro | Upstream stock | Edited | 19.75s · pass | 6.43s · pass | 3.07× |
| Completed-order stop | 278 | M5 Max MacBook Pro | Upstream stock | Baseline | 24.29s · pass | 6.12s · pass | 3.97× |
| Completed-order stop | 96 | M5 Max MacBook Pro | Published search weights | Edited | 47.03s · pass | 6.95s · pass | 6.77× |
| Completed-order stop | 96 | M5 Max MacBook Pro | Published search weights | Baseline | 44.63s · pass | 7.58s · pass | 5.89× |
| Completed-order stop | 191 | M5 Max MacBook Pro | Upstream stock | Edited | 72.89s · fail | 19.84s · grader error | — |
| Completed-order stop | 191 | M5 Max MacBook Pro | Upstream stock | Baseline | 82.11s · fail | 21.12s · grader error | — |
| Completed-order stop | 283 | M5 Max MacBook Pro | Upstream stock | Edited | 81.34s · fail | 12.87s · fail | — |
| Completed-order stop | 283 | M5 Max MacBook Pro | Upstream stock | Baseline | 81.82s · fail | 12.78s · fail | — |

The pending click + stop edit was developed on 189. Its other tasks use frozen weights. The Windows command-stop edit was developed on 188 and has a different shard. The pending click + stop runs on Windows and Mac use the same shard. The completed-order stop edit was developed on 190 after recording the frozen checkpoint on that task. Tasks 191 and 192 were selected in numerical order as the remaining statuses in that same template. [Selection recorded before inference](../evidence/webarena-order-holdouts/selection.json). The RTX 5090 repeat on 191 followed the Mac misses and used the identical completed-order checkpoint. Task 231 rechecks an earlier order-number failure. Task 298 is the first ID in the order-details navigation template. [Recorded task order and advancement rule](../evidence/webarena-order-holdouts/order-navigation.json). On task 191 the official evaluator reports an error for a non-null retrieved answer. That episode earns zero credit. An independent browser inspection covered all four order-history pages. Of 37 orders, 25 were complete, nine canceled and three pending. The fixture contained zero processing orders. Pairs that overlapped the November 21 fixture connection outage were set aside. Reported replacement pairs started after connectivity returned.

182 native grades replayed. The original mismatched Windows fixture remains in the table and contributes no speedup.

[Exact pending-order rows](../evidence/webarena-pending-repair/pending-native-stop/) · [Windows command-stop rows](WEBARENA-ORDER-BOUNDARY.md) · [Grades and recording hashes](../evidence/webarena-order-checkpoints/).

[Download the standalone pending-order checkpoint](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/9f6b8d4dbd3ec39171e38bf528735be4d0b14e66).

[Download the standalone completed-order checkpoint](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/cd27dd36403a165685abd5bf202c326ec9590b20).

[Download the Mac order-lookup trial](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/686faa4d1748f0120008ec007dc97677678e1643). It failed both RTX 5090 runs on task 190.

On the first frozen 190 run, the first complete account click appeared at generated token 5. The model continued until the 512-token limit. The browser received one command for that decision. [Decoder replay](../evidence/webarena-order-checkpoints/190-decoder.json).
The follow-up edit changes 2,261 BF16 values in output row 200006, which ends generation. On the saved initial page, ordinary greedy decoding emitted the same account click in 6 tokens instead of 512. The edit preserved the expected commands on all 24 recorded replay states. The table gives fresh end-to-end browser timings. [Exact rows, decoder replays and byte audit](../evidence/webarena-order-checkpoints/complete-stop/).

On the fastest M5 Max pair, both runs issued the same browser commands and returned the same total. Model inference fell from 42.99 to 2.93 seconds. It accounted for 40.06 of the 40.15 seconds saved. Generated tokens fell from 1,555 to 28. Cursor timing was identical.

The cross-device stop edit reached order history on RTX 5090, then ended navigation in one run and returned an older total of $762.18 in the other. Stock returned the latest completed total of $65.32 twice. Both edited terminal decisions reproduced on the original page observations and action histories. [Terminal-decision replays](../evidence/webarena-order-checkpoints/complete-cross/terminal-replay.json).

On M5 Max, those same weights passed twice. In the 8.95× pair, both runs issued the same clicks. Inference fell from 43.03 to 2.84 seconds and accounted for 40.19 of the 40.76 seconds saved.

## Five storefront searches

The same frozen checkpoint completed all five WebArena search-result tasks on the M5 Max MacBook Pro. These tasks were regression checks on previously tested searches. Stock and edited weights each passed 10 of 10 runs. The smallest speedup across the ten paired runs was 2.13× and the largest was 4.09×.

| Search | Edit ran first | Stock ran first |
|---|---:|---:|
| USB Wi-Fi (274) | 2.13× | 2.66× |
| Xbox (275) | 2.63× | 4.09× |
| Switch accessories (276) | 2.63× | 2.68× |
| iPhone 13 batteries (277) | 3.30× | 3.13× |
| Green tea bags (278) | 3.07× | 3.97× |

On RTX 5090, the identical Xbox search weights passed twice and took longer than stock both times. Stock took 4.81s and 5.01s. The edit took 6.08s and 6.08s.

The next task (283) required opening a specific Xbox controller product page. Both models missed in both run orders.

[Selection rule for the next shopping navigation task](../evidence/webarena-order-holdouts/shopping-navigation.json).

The guarded reasoning trial changes four output rows relative to the Mac order-lookup checkpoint. These rows choose the assistant role, text, reasoning and end of message. The edit reproduced 30 previous Mac browser commands. It uses the same prompt and decoder at inference.
Both models returned the correct total on RTX 5090 in both orders. With the edit first, stock took 5.72s and the edit took 6.79s. With stock first, the times were 10.33s and 3.34s. The two speed ratios were 0.84× and 3.09×.
[Row changes, regression replays and byte audit](../evidence/webarena-order-checkpoints/order-short-margin/).

## Three order lookups with the same weights

On RTX 5090, stock and the order-history edit each passed all six runs across canceled, pending and completed orders. The same edited shard ran 2.03× to 3.53× faster across those pairs. Task 190 was the development case. Tasks 188 and 189 were earlier wins rechecked with those weights.

| WebArena lookup | RTX 5090, edit first | RTX 5090, stock first | M5 Max, edit first | M5 Max, stock first |
|---|---:|---:|---:|---:|
| Canceled (#188) | 2.23× | 3.53× | Pending | Pending |
| Pending (#189) | 2.16× | 2.36× | 4.57× | Edit passed |
| Completed (#190) | 2.03× | 2.18× | 6.46× | 8.19× |
| Processing (#191) | Neither passed | Neither passed | Pending | Pending |

Each timed run starts on the storefront. It ends when the agent submits its response. The full table above includes the elapsed seconds and the official evaluation status for each arm.

## Xbox search on RTX 5090

The same order-history weights completed the Xbox search in 6.35s and 6.01s. Stock took 5.02s and 4.64s. Both models filled the search field, clicked Search and stopped on the results page. The edit generated 512 and 512 tokens for the click alone. That one decision took 3.29s and 3.29s.

Replaying each recorded browser observation through the same RTX decoder reproduced all six commands. The complete search click appeared at token 6 in the first run and token 6 in the second. The decoder then started another assistant message in both runs. [Token positions and original run hashes](../evidence/webarena-order-checkpoints/order-history-route/xbox-submit-replay.json).

Holding the rest of each recorded run fixed, even removing the entire search-click inference time would yield 1.64× and 1.70× versus stock. Reaching 2× on this task would also require time savings elsewhere.

The order-history routing trial changes 2,280 BF16 values in the end-of-message row relative to the guarded reasoning trial. The parent used 510 reasoning tokens without issuing a command on one recorded order-history page. A conditional replay reached the correct answer after 16 reasoning tokens. The trial in the table uses ordinary greedy generation. [Weight audit and unforced replay checks](../evidence/webarena-order-checkpoints/order-history-route/).

On the RTX 5090 completed order lookup (#190), both models returned the correct total in both run orders. Stock needed 4 decisions and the edit needed 3. Stock generated 1,181 tokens, including 1,137 reasoning tokens. The edit generated 335, including 252 reasoning tokens. The two full-task speedups were 2.03× and 2.18×.

On the RTX 5090 pending order lookup (#189), both models returned the correct total in both run orders. Both issued exactly the same browser commands. Stock generated 620 tokens, including 578 reasoning tokens. The edit generated 30, including 0 reasoning tokens. The two full-task speedups were 2.16× and 2.36×.

## Stopping after the Xbox search click

The trial changed 2,282 BF16 values in the sampling-stop output row relative to the order-history checkpoint. Each test used ordinary greedy decoding with the same 512-token ceiling. [Changed weights and replay checks](../evidence/webarena-order-checkpoints/search-submit-stop/).

| RTX 5090 run | Stock | Previous edit | Stop-row edit | Stop-row vs. stock | Search-click tokens, previous → new |
|---|---:|---:|---:|---:|---:|
| Edited first | 4.78s | 6.35s | 3.29s | 1.45× | 512 → 7 |
| Original first | 4.75s | 6.01s | 3.00s | 1.58× | 512 → 7 |

The previous-edit column comes from its earlier, separately timed runs. Each speed ratio uses stock from the same counterbalanced trial as the stop-row edit.

## Xbox controller product page

Task 283 requires ending on a particular product page. In one recorded stock run the browser opened the correct page, then left it. Stock received zero credit. Replaying the official grader with a successful navigation response scores zero before the product request, one immediately after it, and zero after the later navigation. These trace checks add no model runs. [Trace positions and receipt hash](../evidence/webarena-order-checkpoints/xbox-product-grader-check.json).

Task 283 exposed a repeated click on an empty, focused search field. The search-field edit changes 2,281 BF16 values in the output row for the fill command, relative to the five-search checkpoint. It reproduced 45 earlier browser commands and filled the field on two recorded views during ordinary generation. [Exact rows and full browser grades](../evidence/webarena-order-checkpoints/search-focus-route/).

## Verify the published results

From the repository root, replay the official grades and check the reported speed ratios, token counts and model time against the timestamped browser steps. Each step includes a digest of the page observation.

```sh
python benchmark/replay_search.py evidence/webarena-order-checkpoints/native-grades.zip
python benchmark/verify_browser_timings.py evidence/webarena-order-checkpoints/native-grades.zip evidence/webarena-order-checkpoints/pairs.json
```
