# Search after one more click-row edit

The frozen parent repeated a fill on Windows after the search field already contained the exact query. We changed 2,273 BF16 values in the C output row. Every pair below uses the same prompt, greedy decoding, browser controls and typing delay on both arms. Each time covers the full task.

Task 278 was used to develop this edit. The other IDs are earlier controls from the same shopping template. The Mac and Windows trials used Brave, fresh fixtures, native WebArena grades and greedy decoding. Windows field-selection methods have separate results. The Mac and CUDA runs used the same audited weights.

CUDA scored the repeated fill above a click on two recorded decision states. We used those score differences and Mac activation vectors to modify the click output row. Relative to upstream, four output rows contain 9,188 changed BF16 values. Relative to the previous checkpoint, 2,273 values changed in row 34.

| Device | Task | Run | Field selection | Stock | Edited | Speedup |
|---|---:|---:|---|---|---|---:|
| M5 Max MacBook Pro | 278 | r1 | keyboard | 18.84 s · pass | 7.61 s · pass | 2.47× |
| M5 Max MacBook Pro | 278 | r2 | keyboard | 20.14 s · pass | 6.58 s · pass | 3.06× |
| M5 Max MacBook Pro | 274 | r1 | keyboard | 14.64 s · pass | 5.63 s · pass | 2.60× |
| M5 Max MacBook Pro | 274 | r2 | keyboard | 14.30 s · pass | 5.42 s · pass | 2.64× |
| M5 Max MacBook Pro | 276 | r1 | keyboard | 13.64 s · pass | 6.19 s · pass | 2.20× |
| M5 Max MacBook Pro | 276 | r2 | keyboard | 13.13 s · pass | 5.49 s · pass | 2.39× |
| M5 Max MacBook Pro | 277 | r1 | keyboard | 16.39 s · pass | 5.86 s · pass | 2.80× |
| M5 Max MacBook Pro | 277 | r2 | keyboard | 16.68 s · pass | 6.60 s · pass | 2.53× |
| M5 Max MacBook Pro | 275 | r1 | keyboard | 20.43 s · pass | 4.96 s · pass | 4.12× |
| M5 Max MacBook Pro | 275 | r2 | keyboard | 18.25 s · pass | 5.14 s · pass | 3.55× |
| RTX 5090 | 278 | r1 | select-text | 7.30 s · pass | 6.04 s · pass | 1.21× |
| RTX 5090 | 278 | r1 | keyboard | 6.49 s · pass | 7.74 s · fail | — |
| RTX 5090 | 278 | r2-same-device | select-text | 6.61 s · pass | 5.97 s · pass | 1.11× |
| RTX 5090 | 278 | r2-same-device | keyboard | 7.22 s · pass | 7.31 s · fail | — |

28 native grades reproduced from saved network traces.

The first portable Windows pair was 1.21× faster. The edited model failed the first Windows keyboard-shortcut run. Failed attempts have no time-to-success ratio.

[Previous shopping results](WEBARENA-QUERY-TRANSFER.md) · [Windows input control](WINDOWS-FIELD-CONTROL.md) · [All native grade receipts and output rows](../evidence/webarena-click-row/)

```sh
python benchmark/replay_search.py evidence/webarena-click-row/click-row-grades.zip
python benchmark/verify_row_payload.py /path/to/original evidence/webarena-click-row/rows.npz evidence/webarena-click-row/weight-audit.json
```

[First decision, total model generation and browser time](BROWSER-TIME-COMPONENTS.md).
