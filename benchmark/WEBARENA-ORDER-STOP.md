# End generation after a completed browser command

On WebArena 96 the published browser-search checkpoint issued the intended click within five tokens on three decisions, then started another message and generated to the 512-token limit. We changed the output row for the end-of-sampling token. On the three recorded states, ordinary greedy decoding produced the same click and stopped at six tokens.

The change affects 2,288 BF16 values in one row relative to the published search release. The standalone checkpoint differs from upstream Inkling 2 Mini in 4 output rows. The browser, keyboard, cursor, prompt, reasoning setting and token limit match within every pair.

| Task | Baseline checkpoint | First model | Baseline | Stop-row edit | Speedup |
|---|---|---|---:|---:|---:|
| 96 · Latest order | Search release | Stop-row edit | 46.71 s · pass | 6.89 s · pass | 6.78× |
| 96 · Latest order | Search release | Search release | 33.09 s · pass | 7.52 s · pass | 4.40× |

All rows above ran on an M5 Max MacBook Pro. In the separate upstream-stock comparison on the order lookup, stock failed after 65.12 seconds and the search release passed in 50.32 seconds. The order speedup above uses the previously passing search release as its baseline. Task 96 was used to develop the stop-row edit.

4 native grades replayed. [Search baseline weights](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/9a38b0bfc3f703da81ee3bca2e99da929c4623ad) · [Upstream-stock order trial](WEBARENA-CROSS-TASK.md) · [Exact replacement rows, byte audit and grade archive](../evidence/webarena-order-stop/)

```sh
python benchmark/replay_search.py evidence/webarena-order-stop/native-grades.zip
python benchmark/verify_row_payload.py /path/to/Inkling-2-Mini evidence/webarena-order-stop/rows.npz evidence/webarena-order-stop/weight-audit.json
```
