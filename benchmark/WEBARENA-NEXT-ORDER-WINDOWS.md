# Total cost of the latest canceled order on Windows

WebArena 188 ran in Brave on RTX 5090. Both models used the same keyboard controls, cursor, prompt, greedy decoder and 512-token decision limit. Each episode started with a fresh shopping fixture.

The private inference server loaded each checkpoint before the timed episode. Its version readback matched the tested weight hash. Both models used the same cache reset and warm-up.

| First model | Stock Inkling 2 Mini | Stop-row edit | Time-to-success speedup |
|---|---:|---:|---:|
| Stop-row edit | pass · 6.46 s | pass · 6.31 s | 1.02× |
| Stock | pass · 10.43 s | pass · 11.04 s | 0.94× |

4 recorded native grades reproduced. A speedup requires two passing grades.

[Exact weights](WEBARENA-ORDER-STOP.md) · [Grade receipts and recorded network traces](../evidence/webarena-next-order-windows/native-grades.zip)
