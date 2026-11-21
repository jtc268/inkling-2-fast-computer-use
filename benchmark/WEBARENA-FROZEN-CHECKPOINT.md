# One published checkpoint on WebArena

On the M5 Max MacBook Pro, the same downloadable weights completed 6 WebArena tasks at least twice as fast as upstream Inkling 2 Mini in both run orders. Both models passed each of those comparisons.

This table covers every paired WebArena episode for that checkpoint recorded through this study, including failed attempts. It contains 20 pairs across 9 distinct task IDs. The three remaining shopping-search rechecks were scheduled in ID order. Each advanced only after the previous task produced two passing comparisons at 2× or better.

Each arm used Brave, DOM observations, keyboard field selection, greedy decoding, and a 512-token limit per decision. Times cover the browser episode, including generation and actions. Each pair starts from the same visible page.

**Where the USB search saved time.** Both models filled the field, clicked Search and marked the task complete. Stock generated 377 tokens in 12.28s. The edit generated 24 in 2.38s. The thinking-token counts were 342 and 0. Both ran with the same reasoning setting, browser controls and cursor timing.

**Pending-order slowdown.** Both models returned the correct value. In each edited run the first two decisions reached the 512-token limit and produced a bare control number. The browser rejected both commands. Together those decisions used 27.85s and 28.25s across the two runs.

| WebArena task | Device | Baseline | Repeat | Baseline result | Edited result | Speedup |
|---|---|---|---:|---:|---:|---:|
| 96 · Track the latest order | M5 Max MacBook Pro | Published search weights | 1 | pass · 46.71 s | pass · 6.89 s | 6.78× |
| 96 · Track the latest order | M5 Max MacBook Pro | Published search weights | 2 | pass · 33.09 s | pass · 7.52 s | 4.40× |
| 96 · Track the latest order | RTX 5090 | Upstream stock | 1 | fail · 26.09 s | pass · 12.52 s | — |
| 188 · Find the total of the latest canceled order | M5 Max MacBook Pro | Upstream stock | 1 | pass · 27.83 s | pass · 5.22 s | 5.34× |
| 188 · Find the total of the latest canceled order | M5 Max MacBook Pro | Upstream stock | 2 | pass · 27.64 s | pass · 6.07 s | 4.56× |
| 188 · Find the total of the latest canceled order | RTX 5090 | Upstream stock | 1 | pass · 6.46 s | pass · 6.31 s | 1.02× |
| 188 · Find the total of the latest canceled order | RTX 5090 | Upstream stock | 2 | pass · 10.43 s | pass · 11.04 s | 0.94× |
| 189 · Find the total of the latest pending order | M5 Max MacBook Pro | Upstream stock | 1 | pass · 23.50 s | pass · 31.90 s | 0.74× |
| 189 · Find the total of the latest pending order | M5 Max MacBook Pro | Upstream stock | 2 | pass · 33.85 s | pass · 33.24 s | 1.02× |
| 274 · Search for a USB Wi-Fi adapter | M5 Max MacBook Pro | Upstream stock | 1 | pass · 14.63 s | pass · 4.72 s | 3.10× |
| 274 · Search for a USB Wi-Fi adapter | M5 Max MacBook Pro | Upstream stock | 2 | pass · 14.45 s | pass · 4.92 s | 2.93× |
| 275 · Search for Xbox | M5 Max MacBook Pro | Upstream stock | 1 | pass · 18.69 s | pass · 4.71 s | 3.97× |
| 275 · Search for Xbox | M5 Max MacBook Pro | Upstream stock | 2 | pass · 19.09 s | pass · 4.74 s | 4.03× |
| 276 · Search for Switch accessories | M5 Max MacBook Pro | Upstream stock | 1 | pass · 12.69 s | pass · 5.39 s | 2.35× |
| 276 · Search for Switch accessories | M5 Max MacBook Pro | Upstream stock | 2 | pass · 12.93 s | pass · 5.34 s | 2.42× |
| 277 · Search for iPhone 13 batteries | M5 Max MacBook Pro | Upstream stock | 1 | pass · 16.49 s | pass · 5.96 s | 2.77× |
| 277 · Search for iPhone 13 batteries | M5 Max MacBook Pro | Upstream stock | 2 | pass · 16.96 s | pass · 5.82 s | 2.91× |
| 278 · Search for green tea bags | M5 Max MacBook Pro | Upstream stock | 1 | pass · 19.34 s | pass · 5.94 s | 3.26× |
| 278 · Search for green tea bags | M5 Max MacBook Pro | Upstream stock | 2 | pass · 19.36 s | pass · 6.52 s | 2.97× |
| 432 · Compare two drinks and add the cheaper one per unit | M5 Max MacBook Pro | Upstream stock | 1 | fail · 34.84 s | fail · 11.12 s | — |

All 40 native grades reproduced from saved responses and network events. The full WebArena suite is pending.

[Download the exact model](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/dc1cecc5b251ed3d4a4202a2267486a84a6f4684) · [Weight audit and reconstruction](WEBARENA-ORDER-STOP.md) · [Grade archive and pair timings](../evidence/webarena-frozen-checkpoint/) · [Watch the ordered film](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4)

```sh
python benchmark/replay_search.py evidence/webarena-frozen-checkpoint/native-grades.zip
```
