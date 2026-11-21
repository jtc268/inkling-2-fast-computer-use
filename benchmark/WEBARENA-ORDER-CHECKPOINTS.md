# Frozen order checkpoints

Each row is a fresh pair in Brave. A speedup requires two native WebArena-Verified passes on matched fixtures. The full-task clock includes model generation and browser actions. Both arms receive visible page text and numbered controls, use the same cursor timing, and decode greedily with a 512-token limit. Both set the chat template to `reasoning_effort="none"`. The model can still emit thinking tokens at that setting.

| Checkpoint | Hardware | Baseline | Task IDs | Baseline passes | Edited passes | IDs at ≥2× in both orders |
|---|---|---|---|---:|---:|---|
| Completed-order stop | M5 Max MacBook Pro | Upstream stock | 189, 190 | 4/4 | 4/4 | 189, 190 |
| Completed-order stop | RTX 5090 | Upstream stock | 190 | 2/2 | 2/2 | — |
| Windows command-stop | M5 Max MacBook Pro | Upstream stock | 188, 274 | 4/4 | 4/4 | 188 |
| Windows command-stop | RTX 5090 | Upstream stock | 188 | 2/2 | 2/2 | 188 |
| Pending click + stop | M5 Max MacBook Pro | Published search weights | 96 | 2/2 | 2/2 | 96 |
| Pending click + stop | M5 Max MacBook Pro | Upstream stock | 188, 189, 190, 274, 275, 276 | 12/12 | 12/12 | 188, 189, 190, 274, 275 |
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
| Completed-order stop | 190 | M5 Max MacBook Pro | Upstream stock | Edited | 45.34s · pass | 5.19s · pass | 8.73× |
| Completed-order stop | 190 | M5 Max MacBook Pro | Upstream stock | Baseline | 46.59s · pass | 6.01s · pass | 7.75× |
| Completed-order stop | 190 | RTX 5090 | Upstream stock | Edited | 7.22s · pass | 9.29s · pass | 0.78× |
| Completed-order stop | 190 | RTX 5090 | Upstream stock | Baseline | 12.15s · pass | 8.93s · pass | 1.36× |
| Completed-order stop | 189 | M5 Max MacBook Pro | Upstream stock | Edited | 33.17s · pass | 5.30s · pass | 6.25× |
| Completed-order stop | 189 | M5 Max MacBook Pro | Upstream stock | Baseline | 24.86s · pass | 5.87s · pass | 4.24× |

The pending click + stop edit was developed on 189. Its other tasks use frozen weights. The Windows command-stop edit was developed on 188 and has a different shard. The pending click + stop runs on Windows and Mac use the same shard. The completed-order stop edit was developed on 190 after recording the frozen checkpoint on that task.

62 native grades replayed. The original mismatched Windows fixture remains in the table and contributes no speedup.

[Exact pending-order rows](../evidence/webarena-pending-repair/pending-native-stop/) · [Windows command-stop rows](WEBARENA-ORDER-BOUNDARY.md) · [Grades and recording hashes](../evidence/webarena-order-checkpoints/).

[Download the standalone pending-order checkpoint](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/9f6b8d4dbd3ec39171e38bf528735be4d0b14e66).

On the first frozen 190 run, the first complete account click appeared at generated token 5. The model continued until the 512-token limit. The browser received one command for that decision. [Decoder replay](../evidence/webarena-order-checkpoints/190-decoder.json).
The follow-up edit changes 2,261 BF16 values in output row 200006, which ends generation. On the saved initial page, ordinary greedy decoding emitted the same account click in 6 tokens instead of 512. The edit preserved the expected commands on all 24 recorded replay states. The table gives fresh end-to-end browser timings. [Exact rows, decoder replays and byte audit](../evidence/webarena-order-checkpoints/complete-stop/).
