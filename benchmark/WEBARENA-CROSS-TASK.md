# How the frozen checkpoints perform on other browser tasks

The forum checkpoint that submitted WebArena 630 on the Mac was tested on earlier shopping wins. The browser-search checkpoint that passed all five search cases was tested on WebArena 96, which asks for the status and arrival date of the latest order. Neither checkpoint changed between its development task and these checks.

Every run used a fresh fixture and Brave on the M5 Max MacBook Pro. Stock and edited weights used the same prompt, greedy decoder, step limit, keyboard controls and cursor movement.

| Checkpoint | Task | First model | Stock | Edited | Speedup |
|---|---|---|---:|---:|---:|
| Forum submission | 275 · Xbox search | Edited | 18.80 s · pass | 4.69 s · pass | 4.01× |
| Forum submission | 275 · Xbox search | Stock | 18.05 s · pass | 5.19 s · pass | 3.48× |
| Browser search | 96 · Latest order | Edited | 65.12 s · fail | 50.32 s · pass | — |

6 grades reproduced from the saved native responses and network traces.

[Forum submission](WEBARENA-FORUM-CONTROLS.md) · [Five search cases and Windows repeat](WEBARENA-NATIVE-CLICK.md) · [Checkpoint hashes and grade archive](../evidence/webarena-cross-task/)

```sh
python benchmark/replay_search.py evidence/webarena-cross-task/native-grades.zip
```
