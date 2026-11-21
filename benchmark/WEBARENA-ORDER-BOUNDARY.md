# Stop after the correct account click on Windows

WebArena 188 ran in Brave on RTX 5090. Both models used the same keyboard controls, cursor, prompt, greedy decoder and 512-token decision limit. Each episode started with a fresh shopping fixture.

The private inference server loaded each checkpoint before the timed episode. Its version readback matched the tested weight hash. Both models used the same cache reset and warm-up.

The preceding click-row candidate opened My Account, reached My Orders and failed to return the total. Replaying its native decoder exposed completed browser clicks followed by additional output. This checkpoint changes row 200006 (2,288 BF16 values) relative to that candidate. Both models below used ordinary decoding.

| First model | Stock Inkling 2 Mini | Order boundary edit | Time-to-success speedup |
|---|---:|---:|---:|
| Order boundary edit | fail · 5.45 s | pass · 3.16 s | — |
| Stock | pass · 6.86 s | pass · 2.65 s | 2.59× |
| Order boundary edit | pass · 6.47 s | pass · 3.12 s | 2.07× |

The first pair is excluded from speed and model-accuracy comparisons. The recorded storefront HTML sent stock’s My Account click to the unreachable original WebArena host and sent the edited model to the working local fixture. The native grades are retained above. The fixture now verifies the account link before each timed run.


6 recorded native grades reproduced. A speedup requires two passing grades.

[Earlier Windows order trial](WEBARENA-ORDER-START.md) · [Exact replacement rows and grade archive](../evidence/webarena-order-boundary/)


~~~sh
python benchmark/replay_search.py evidence/webarena-order-boundary/native-grades.zip
python benchmark/verify_row_payload.py /path/to/Inkling-2-Mini evidence/webarena-order-boundary/rows.npz evidence/webarena-order-boundary/weight-audit.json
~~~
