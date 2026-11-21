# Windows search after a native click-row edit

The previous edit repeatedly filled the green-tea search box on Windows. Both keyboard trials failed. The next edit changed 2,264 BF16 values in the click output row relative to that parent. The system prompt, greedy decoding, token cap, field controls and mouse motion matched across each stock and edited pair.

We recovered the native CUDA output vectors from token score differences, accounting for the model’s final logit softcap. We checked recovery on 480 unused output tokens and the separate click and fill tokens. A direct output-row edit raised click above fill on the two captured repeated-fill states. The recorded Mac shopping controls contributed protected output positions.

| Device | Task | Run | Field selection | Stock | Edited | Speedup |
|---|---:|---|---|---:|---:|---:|
| M5 Max MacBook Pro | 278 | r1 | keyboard | 19.19 s · pass | 6.01 s · pass | 3.19× |
| M5 Max MacBook Pro | 278 | r2 | keyboard | 19.34 s · pass | 5.99 s · pass | 3.23× |
| M5 Max MacBook Pro | 274 | r1 | keyboard | 14.60 s · pass | 5.38 s · pass | 2.72× |
| M5 Max MacBook Pro | 274 | r2 | keyboard | 14.98 s · pass | 5.79 s · pass | 2.59× |
| M5 Max MacBook Pro | 276 | r1 | keyboard | 13.50 s · pass | 5.32 s · pass | 2.54× |
| M5 Max MacBook Pro | 276 | r2 | keyboard | 13.71 s · pass | 5.49 s · pass | 2.50× |
| M5 Max MacBook Pro | 277 | r1 | keyboard | 17.71 s · pass | 6.42 s · pass | 2.76× |
| M5 Max MacBook Pro | 277 | r2 | keyboard | 19.77 s · pass | 6.44 s · pass | 3.07× |
| M5 Max MacBook Pro | 275 | r1 | keyboard | 18.45 s · pass | 5.01 s · pass | 3.69× |
| M5 Max MacBook Pro | 275 | r2 | keyboard | 18.47 s · pass | 4.73 s · pass | 3.90× |
| RTX 5090 | 278 | r1 | keyboard | 6.58 s · pass | 5.08 s · pass | 1.29× |
| RTX 5090 | 278 | r2 | keyboard | 6.82 s · pass | 4.14 s · pass | 1.65× |
| RTX 5090 | 278 | r1 | select-text | 6.84 s · pass | 4.36 s · pass | 1.57× |
| RTX 5090 | 278 | r2 | select-text | 7.94 s · pass | 4.17 s · pass | 1.90× |

28 native grades replayed from the saved network evidence. Task 278 was used for development. The other Mac IDs are earlier search controls.

[Earlier Windows failures](WEBARENA-CLICK-ROW.md) · [Native grades, weight audit and reconstruction rows](../evidence/webarena-cuda-click/)

```sh
python benchmark/replay_search.py evidence/webarena-cuda-click/native-grades.zip
python benchmark/verify_row_payload.py /path/to/original evidence/webarena-cuda-click/rows.npz evidence/webarena-cuda-click/weight-audit.json
```

[Download the tested standalone checkpoint](https://huggingface.co/husky8/Inkling-2-Mini-Fast-Browser-Use/tree/9a38b0bfc3f703da81ee3bca2e99da929c4623ad).
