# Sony headphone names and prices

WebArena 279 is the first shopping task in catalog order after the five search-navigation tasks. It asks for product names and the minimum and maximum prices. The click-row checkpoint was frozen before either model attempted the task.

Both models ran in Brave on the M5 Max MacBook Pro with the same browser controls, system prompt, greedy sampling and 512-token limit per decision. Each episode began on a fresh fixture. The native WebArena-Verified evaluator graded the final response and network trace.

| Run order | Stock | Click-row edit | Speedup |
|---|---:|---:|---:|
| Edited first | fail · 58.91 s | fail · 8.50 s | — |

A time-to-success speedup requires two passing grades.

[Frozen weights and five shopping controls](WEBARENA-CLICK-ROW.md) · [Protocol, grades and network evidence](../evidence/webarena-shopping-transfer/)

```sh
python benchmark/replay_search.py evidence/webarena-shopping-transfer/grade-replay.zip
```

## Development follow-up

We then used the observed failure to change the output weights for scrolling and ending a response. The new checkpoint scrolled to the products in a fresh browser and returned 4 names and a price range in 11.01 seconds. The native evaluator rejected the answer. Task 279 became a development case for this edit.

[Development receipt and network trace](../evidence/webarena-shopping-transfer/retrieval-development-replay.zip) · [Development checkpoint and elapsed time](../evidence/webarena-shopping-transfer/scroll-development.json)
