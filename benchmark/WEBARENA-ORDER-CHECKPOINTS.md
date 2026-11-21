# Frozen order checkpoints

Each row is a fresh pair in Brave. A speedup requires two native WebArena-Verified passes on matched fixtures. The full-task clock includes model generation and browser actions. Both arms receive visible page text and numbered controls, use the same cursor timing, and decode greedily with a 512-token limit. Both set the chat template to `reasoning_effort="none"`. The model can still emit thinking tokens at that setting.

| Checkpoint | Hardware | Baseline | Task IDs | Baseline passes | Edited passes | IDs at ≥2× in both orders |
|---|---|---|---|---:|---:|---|
| Cross-device order stop | M5 Max MacBook Pro | Upstream stock | 189, 190 | 4/4 | 4/4 | 189, 190 |
| Cross-device order stop | RTX 5090 | Upstream stock | 190 | 2/2 | 0/2 | — |
| Completed-order stop | M5 Max MacBook Pro | Published search weights | 96 | 2/2 | 2/2 | 96 |
| Completed-order stop | M5 Max MacBook Pro | Upstream stock | 188, 189, 190, 191, 274 | 8/10 | 8/10 | 188, 189, 190, 274 |
| Completed-order stop | RTX 5090 | Upstream stock | 190 | 2/2 | 2/2 | — |
| Windows command-stop | M5 Max MacBook Pro | Upstream stock | 188, 274 | 4/4 | 4/4 | 188 |
| Windows command-stop | RTX 5090 | Upstream stock | 188 | 2/2 | 2/2 | 188 |
| Pending click + stop | M5 Max MacBook Pro | Published search weights | 96 | 2/2 | 2/2 | 96 |
| Pending click + stop | M5 Max MacBook Pro | Upstream stock | 62, 188, 189, 190, 274, 275, 276 | 12/14 | 12/14 | 188, 189, 190, 274, 275 |
| Pending click + stop | RTX 5090 | Upstream stock | 188, 189 | 4/4 | 4/4 | 189 |

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
| Cross-device order stop | 190 | RTX 5090 | Upstream stock | Edited | 9.33s · pass | 3.29s · fail | — |
| Cross-device order stop | 190 | RTX 5090 | Upstream stock | Baseline | 12.41s · pass | 3.19s · fail | — |
| Cross-device order stop | 189 | M5 Max MacBook Pro | Upstream stock | Edited | 33.13s · pass | 5.25s · pass | 6.31× |
| Cross-device order stop | 189 | M5 Max MacBook Pro | Upstream stock | Baseline | 34.83s · pass | 5.74s · pass | 6.07× |
| Cross-device order stop | 190 | M5 Max MacBook Pro | Upstream stock | Edited | 45.89s · pass | 5.13s · pass | 8.95× |
| Cross-device order stop | 190 | M5 Max MacBook Pro | Upstream stock | Baseline | 44.67s · pass | 5.58s · pass | 8.00× |
| Completed-order stop | 188 | M5 Max MacBook Pro | Upstream stock | Edited | 45.75s · pass | 6.44s · pass | 7.10× |
| Completed-order stop | 188 | M5 Max MacBook Pro | Upstream stock | Baseline | 29.18s · pass | 4.84s · pass | 6.02× |
| Completed-order stop | 189 | M5 Max MacBook Pro | Upstream stock | Edited | 33.17s · pass | 5.30s · pass | 6.25× |
| Completed-order stop | 189 | M5 Max MacBook Pro | Upstream stock | Baseline | 24.86s · pass | 5.87s · pass | 4.24× |
| Completed-order stop | 274 | M5 Max MacBook Pro | Upstream stock | Edited | 15.15s · pass | 7.10s · pass | 2.13× |
| Completed-order stop | 274 | M5 Max MacBook Pro | Upstream stock | Baseline | 14.35s · pass | 5.39s · pass | 2.66× |
| Completed-order stop | 96 | M5 Max MacBook Pro | Published search weights | Edited | 47.03s · pass | 6.95s · pass | 6.77× |
| Completed-order stop | 96 | M5 Max MacBook Pro | Published search weights | Baseline | 44.63s · pass | 7.58s · pass | 5.89× |
| Completed-order stop | 191 | M5 Max MacBook Pro | Upstream stock | Edited | 72.89s · fail | 19.84s · grader error | — |
| Completed-order stop | 191 | M5 Max MacBook Pro | Upstream stock | Baseline | 82.11s · fail | 21.12s · grader error | — |

The pending click + stop edit was developed on 189. Its other tasks use frozen weights. The Windows command-stop edit was developed on 188 and has a different shard. The pending click + stop runs on Windows and Mac use the same shard. The completed-order stop edit was developed on 190 after recording the frozen checkpoint on that task. Tasks 191 and 192 were selected in numerical order as the remaining statuses in that same template. [Selection recorded before inference](../evidence/webarena-order-holdouts/selection.json). On task 191 the official evaluator reports an error for a non-null retrieved answer. That episode earns zero credit. An independent browser inspection covered all four order-history pages. Of 37 orders, 25 were complete, nine canceled and three pending. The fixture contained zero processing orders. Pairs that overlapped the November 21 fixture connection outage were set aside. Reported replacement pairs started after connectivity returned.

94 native grades replayed. The original mismatched Windows fixture remains in the table and contributes no speedup.

[Exact pending-order rows](../evidence/webarena-pending-repair/pending-native-stop/) · [Windows command-stop rows](WEBARENA-ORDER-BOUNDARY.md) · [Grades and recording hashes](../evidence/webarena-order-checkpoints/).

[Download the standalone pending-order checkpoint](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/9f6b8d4dbd3ec39171e38bf528735be4d0b14e66).

[Download the standalone completed-order checkpoint](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/cd27dd36403a165685abd5bf202c326ec9590b20).

[Download the Mac order-lookup trial](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/686faa4d1748f0120008ec007dc97677678e1643). It failed both RTX 5090 runs on task 190.

On the first frozen 190 run, the first complete account click appeared at generated token 5. The model continued until the 512-token limit. The browser received one command for that decision. [Decoder replay](../evidence/webarena-order-checkpoints/190-decoder.json).
The follow-up edit changes 2,261 BF16 values in output row 200006, which ends generation. On the saved initial page, ordinary greedy decoding emitted the same account click in 6 tokens instead of 512. The edit preserved the expected commands on all 24 recorded replay states. The table gives fresh end-to-end browser timings. [Exact rows, decoder replays and byte audit](../evidence/webarena-order-checkpoints/complete-stop/).

On the fastest M5 Max pair, both runs issued the same browser commands and returned the same total. Model inference fell from 42.99 to 2.93 seconds. It accounted for 40.06 of the 40.15 seconds saved. Generated tokens fell from 1,555 to 28. Cursor timing was identical.

The cross-device stop edit reached order history on RTX 5090, then ended navigation in one run and returned an older total of $762.18 in the other. Stock returned the latest completed total of $65.32 twice. Both edited terminal decisions reproduced on the original page observations and action histories. [Terminal-decision replays](../evidence/webarena-order-checkpoints/complete-cross/terminal-replay.json).

On M5 Max, those same weights passed twice. In the 8.95× pair, both runs issued the same clicks. Inference fell from 43.03 to 2.84 seconds and accounted for 40.19 of the 40.76 seconds saved.
