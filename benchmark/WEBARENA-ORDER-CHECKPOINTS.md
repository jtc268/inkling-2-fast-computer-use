# Frozen order checkpoints

Each row is a fresh pair in Brave. A speedup requires two native WebArena-Verified passes on matched fixtures. The full-task clock includes model generation and browser actions. Both arms use greedy decoding and the same 512-token limit.

| Checkpoint | Task | Hardware | Baseline | Ran first | Baseline time | Edited time | Speedup |
|---|---:|---|---|---|---:|---:|---:|
| Windows command-stop | 188 | RTX 5090 | Upstream stock | Edited | 5.45s · fail | 3.16s · pass | Excluded · broken fixture link |
| Windows command-stop | 188 | RTX 5090 | Upstream stock | Baseline | 6.86s · pass | 2.65s · pass | 2.59× |
| Windows command-stop | 188 | RTX 5090 | Upstream stock | Edited | 6.47s · pass | 3.12s · pass | 2.07× |
| Pending click + stop | 189 | M5 Max MacBook Pro | Upstream stock | Edited | 24.01s · pass | 5.12s · pass | 4.69× |
| Pending click + stop | 189 | M5 Max MacBook Pro | Upstream stock | Baseline | 23.86s · pass | 4.16s · pass | 5.74× |
| Pending click + stop | 188 | M5 Max MacBook Pro | Upstream stock | Edited | 27.98s · pass | 5.16s · pass | 5.42× |
| Pending click + stop | 188 | M5 Max MacBook Pro | Upstream stock | Baseline | 28.35s · pass | 5.33s · pass | 5.32× |

The pending click + stop edit was developed on 189. Its other tasks use frozen weights. The Windows command-stop edit was developed on 188 and has a different shard.

14 native grades replayed. The original mismatched Windows fixture remains in the table and contributes no speedup.

[Exact pending-order rows](../evidence/webarena-pending-repair/pending-native-stop/) · [Windows command-stop rows](WEBARENA-ORDER-BOUNDARY.md) · [Grades and recording hashes](../evidence/webarena-order-checkpoints/).
