# Where the browser time went

On the 4.12× Xbox search, the edit saved 15.47 seconds. Measured model generation fell from 18.22 to 2.80 seconds, accounting for 15.42 seconds of that difference. The first decision saved 1.28 seconds. Stock made five decisions and emitted 448 reasoning-channel tokens. The edit made three decisions and emitted zero reasoning-channel tokens. Both passed.

Across the ten paired M5 Max search runs, total time-to-success fell by 106.96 seconds. The sum of model generation time fell by 108.81 seconds. Individual ratios appear below. Both arms used the same cursor motion and typing delay.

| Device | ID | Run | Input | Total time | Generation time | First decision generation | Decisions | Speedup |
|---|---:|---|---|---:|---:|---:|---:|---:|
| M5 Max MacBook Pro | 278 | r1 | keyboard | 18.84 → 7.61 s | 15.45 → 3.00 s | 2.23 → 1.24 s | 5 → 3 | 2.47× |
| M5 Max MacBook Pro | 278 | r2 | keyboard | 20.14 → 6.58 s | 16.98 → 3.37 s | 2.74 → 1.28 s | 5 → 3 | 3.06× |
| M5 Max MacBook Pro | 274 | r1 | keyboard | 14.64 → 5.63 s | 12.29 → 3.21 s | 2.82 → 1.55 s | 3 → 3 | 2.60× |
| M5 Max MacBook Pro | 274 | r2 | keyboard | 14.30 → 5.42 s | 12.01 → 3.03 s | 2.85 → 1.32 s | 3 → 3 | 2.64× |
| M5 Max MacBook Pro | 276 | r1 | keyboard | 13.64 → 6.19 s | 11.01 → 3.39 s | 2.82 → 1.30 s | 3 → 3 | 2.20× |
| M5 Max MacBook Pro | 276 | r2 | keyboard | 13.13 → 5.49 s | 10.52 → 2.91 s | 2.62 → 1.23 s | 3 → 3 | 2.39× |
| M5 Max MacBook Pro | 277 | r1 | keyboard | 16.39 → 5.86 s | 13.32 → 2.90 s | 2.84 → 1.20 s | 4 → 3 | 2.80× |
| M5 Max MacBook Pro | 277 | r2 | keyboard | 16.68 → 6.60 s | 13.54 → 2.98 s | 2.79 → 1.24 s | 4 → 3 | 2.53× |
| M5 Max MacBook Pro | 275 | r1 | keyboard | 20.43 → 4.96 s | 18.22 → 2.80 s | 2.46 → 1.18 s | 5 → 3 | 4.12× |
| M5 Max MacBook Pro | 275 | r2 | keyboard | 18.25 → 5.14 s | 16.09 → 3.03 s | 2.40 → 1.50 s | 5 → 3 | 3.55× |
| RTX 5090 | 278 | r1 | select-text | 7.30 → 6.04 s | 3.72 → 0.93 s | 1.27 → 0.23 s | 4 → 4 | 1.21× |
| RTX 5090 | 278 | r1 | keyboard | 6.49 → 7.74 s | 2.99 → 1.45 s | 0.57 → 0.52 s | 4 → 5 | — |
| RTX 5090 | 278 | r2-same-device | select-text | 6.61 → 5.97 s | 3.05 → 1.15 s | 0.56 → 0.51 s | 4 → 4 | 1.11× |
| RTX 5090 | 278 | r2-same-device | keyboard | 7.22 → 7.31 s | 3.42 → 1.22 s | 0.87 → 0.24 s | 4 → 5 | — |

Each pair shows stock followed by the click-row edit. All times use the independent clock for that run. [Native outcomes and weight audit](WEBARENA-CLICK-ROW.md) · [Component values](../evidence/webarena-click-row/time-components.json)
