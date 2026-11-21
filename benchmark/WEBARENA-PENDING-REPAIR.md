# Pending order on Mac

WebArena 189 asks for the total of the latest pending order. Each timed run uses the normal browser agent in Brave on the M5 Max MacBook Pro. Every pair compares a weight edit with upstream stock on the same starting page, prompt, controls, cursor and decoder.

The published checkpoint was frozen before task selection. The later edits used this task during development. They are separate checkpoints.

| Weight edit | First model | Stock | Edited | Time-to-success speedup |
|---|---|---:|---:|---:|
| Published stop-row weights | Edited | pass · 23.50s | pass · 31.90s | 0.74× |
| Published stop-row weights | Stock | pass · 33.85s | pass · 33.24s | 1.02× |
| Pending click edit | Edited | pass · 23.84s | pass · 18.25s | 1.31× |
| Pending click edit | Stock | pass · 32.46s | pass · 19.68s | 1.65× |
| Pending click + stop edit | Edited | pass · 24.01s | pass · 5.12s | 4.69× |
| Pending click + stop edit | Stock | pass · 23.86s | pass · 4.16s | 5.74× |

In both published-checkpoint runs the browser rejected two bare control numbers, each generated at the 512-token limit. The pending click edit changes the click-verb output row relative to the Windows command-boundary candidate. The numerical control and order value still come from the model. The pending click + stop checkpoint changes the sampling-stop row relative to that Mac click edit.

12 recorded native grades reproduced. [Grade receipts, timings and exact replacement rows](../evidence/webarena-pending-repair/) · [Frozen model results](WEBARENA-FROZEN-CHECKPOINT.md) · [Task selection](WEBARENA-PENDING-ORDER.md).
