# Total cost of the latest pending order

WebArena 189 ran in Brave on M5 Max MacBook Pro. Both models used the same keyboard controls, cursor, prompt, greedy decoder and 512-token decision limit. Each episode started with a fresh shopping fixture.

Task 189 uses the same template as the canceled-order lookup. The prompt asks for the latest pending order. Its ID and released weight hash were fixed before the run.

| First model | Stock Inkling 2 Mini | Stop-row edit | Time-to-success speedup |
|---|---:|---:|---:|
| Stop-row edit | pass · 23.50 s | pass · 31.90 s | 0.74× |
| Stock | pass · 33.85 s | pass · 33.24 s | 1.02× |

Run 1. Stock issued 4 commands and the edit issued 5. Model generation took 21.18 seconds for stock and 30.01 seconds for the edit.
Run 2. Stock issued 5 commands and the edit issued 6. Model generation took 31.14 seconds for stock and 30.95 seconds for the edit.

4 recorded native grades reproduced. A speedup requires two passing grades.

[Exact weights](WEBARENA-ORDER-STOP.md) · [Grade receipts and recorded network traces](../evidence/webarena-pending-order/native-grades.zip)
