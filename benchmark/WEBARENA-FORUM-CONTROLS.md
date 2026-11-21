# WebArena 630 forum submission

Each trial starts on a fresh forum. Stock and the named edit use the same browser controls, prompt, greedy decoding and 512-token limit per decision. The native evaluator checks the requested submission. A time-to-success ratio requires both runs to pass.

| Device | Edit | Run | Stock | Edited | Speedup |
|---|---|---|---:|---:|---:|
| M5 Max MacBook Pro | Select-transfer | r1 | fail · 88.91 s | fail · 9.42 s | — |
| RTX 5090 | Select-transfer | r1 | pass · 23.37 s | fail · 19.71 s | — |
| M5 Max MacBook Pro | Forum-channel | r1 | fail · 94.04 s | fail · 12.36 s | — |
| M5 Max MacBook Pro | Submit-margin | r1 | fail · 78.20 s | fail · 13.41 s | — |
| M5 Max MacBook Pro | Cached-submit | r1 | fail · 95.01 s | pass · 20.95 s | — |

On the recorded Mac failure, the select-transfer edit stopped with the forum field empty. The forum-channel edit changed only the answer and reasoning output rows relative to that checkpoint. It selected the requested forum in a fresh run, then stopped without submitting the post.

For the submit-margin experiment, a scripted development trace established that scrolling, clicking the visible submit button and observing the posted page completed the task. Only the model-driven fresh runs appear in the table.

The scroll command and the completion command share their first token. The model continued that token into a completion command while the submit button was still below the viewport. We adjusted four structural output rows using activations from the normal token-by-token decoding path. The fresh runs in the table used the resulting checkpoint directly.

10 native grades reproduced from the recorded responses and network traces. [Grade archive](../evidence/webarena-forum-controls/native-grades.zip) · [Weights and paired results](../evidence/webarena-forum-controls/native-results.json)

```sh
python benchmark/replay_search.py evidence/webarena-forum-controls/native-grades.zip
```
