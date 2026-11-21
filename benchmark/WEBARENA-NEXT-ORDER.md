# Total cost of the latest canceled order

WebArena 188 ran in Brave on M5 Max MacBook Pro. Both models used the same keyboard controls, cursor, prompt, greedy decoder and 512-token decision limit. Each episode started with a fresh shopping fixture.

We selected the first unseen shopping-only order lookup after task 96 with a native response evaluator. The task and weight hash were recorded before the first run.

| First model | Stock Inkling 2 Mini | Stop-row edit | Time-to-success speedup |
|---|---:|---:|---:|
| Stop-row edit | pass · 27.83 s | pass · 5.22 s | 5.34× |
| Stock | pass · 27.64 s | pass · 6.07 s | 4.56× |

Run 1. Both issued the same browser commands. Model generation took 25.51 seconds for stock and 2.86 seconds for the edit.
Run 2. Stock issued 4 commands and the edit issued 5. Model generation took 25.39 seconds for stock and 3.76 seconds for the edit.

4 recorded native grades reproduced. A speedup requires two passing grades.

[Exact weights](WEBARENA-ORDER-STOP.md) · [Grade receipts and recorded network traces](../evidence/webarena-next-order/native-grades.zip)
