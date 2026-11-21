# Restore the click verb on the Windows order lookup

WebArena 188 ran in Brave on RTX 5090. Both models used the same keyboard controls, cursor, prompt, greedy decoder and 512-token decision limit. Each episode started with a fresh shopping fixture.

The private inference server loaded each checkpoint before the timed episode. Its version readback matched the tested weight hash. Both models used the same cache reset and warm-up.

The previous stop-row weights started by emitting a bare control number. Its first decision used all 512 tokens in both Windows run orders. On the recorded first decisions, a click-verb continuation produced the intended account click in 11 tokens. We changed 2,283 BF16 values in the click output row. The graded runs below use the normal decoder.

| First model | Stock Inkling 2 Mini | Order click edit | Time-to-success speedup |
|---|---:|---:|---:|
| Order click edit | pass · 9.63 s | fail · 6.73 s | — |

The edit opened My Account in 6 tokens. It reached My Orders and stopped without returning the total. The native evaluator scored that episode zero.


2 recorded native grades reproduced. A speedup requires two passing grades.

[Earlier Windows order trial](WEBARENA-NEXT-ORDER-WINDOWS.md) · [Exact replacement rows and grade archive](../evidence/webarena-order-start/)


~~~sh
python benchmark/replay_search.py evidence/webarena-order-start/native-grades.zip
python benchmark/verify_row_payload.py /path/to/Inkling-2-Mini evidence/webarena-order-start/rows.npz evidence/webarena-order-start/weight-audit.json
~~~
