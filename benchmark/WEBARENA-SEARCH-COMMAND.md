# One browser command per decision

On the earlier checkpoint, a filled search field could produce a click, then a second answer declaring success on the home page. On RTX the click decision sometimes ran to the 512-token cap. This checkpoint adjusts the click row and the native stop row. It raises the stop score after a complete browser command. The model selects the command and its control number.

The direct linear edits used saved USB Wi-Fi and Switch-accessories states and synthetic screens. There was no gradient training. The original and edited models used the same prompt, greedy decoding, 512-token cap, browser commands, cursor animation and typing speed on each device. Every episode used a fresh signed-in WebArena fixture. The Mac pairs reversed their order.

| Device | Task | Role | Repeat | Original | Edited | Passing pair |
|---|---|---|---:|---:|---:|---:|
| M5 Max MacBook Pro | 274 · USB Wi-Fi adapter | development and prior control | 1 | 14.19 s · pass | 5.19 s · pass | 2.73× |
| M5 Max MacBook Pro | 274 · USB Wi-Fi adapter | development and prior control | 2 | 14.63 s · pass | 5.03 s · pass | 2.91× |
| M5 Max MacBook Pro | 276 · Switch accessories | development and prior control | 1 | 14.39 s · pass | 5.15 s · pass | 2.79× |
| M5 Max MacBook Pro | 276 · Switch accessories | development and prior control | 2 | 13.66 s · pass | 5.44 s · pass | 2.51× |
| M5 Max MacBook Pro | 277 · iPhone 13 batteries | previously failed query, excluded from edit | 1 | 16.82 s · pass | 6.18 s · pass | 2.72× |
| M5 Max MacBook Pro | 277 · iPhone 13 batteries | previously failed query, excluded from edit | 2 | 16.89 s · pass | 6.41 s · pass | 2.63× |
| M5 Max MacBook Pro | 278 · Green tea bags | fresh same-template holdout | 1 | 20.44 s · pass | 39.68 s · fail | — |
| RTX 5090 | 274 · USB Wi-Fi adapter | development and prior control | 1 | 5.23 s · pass | 3.82 s · pass | 1.37× |
| RTX 5090 | 276 · Switch accessories | development and prior control | 1 | 5.21 s · pass | 6.77 s · pass | 0.77× |

Across these runs the original passed 9/9 and the edit passed 8/9. Each reported speed is stock wall time divided by edited wall time on the same passing case. Shopping search queries share one interface and task template. Full-suite accuracy remains open.

On USB Wi-Fi adapter, the Mac median was 14.41 s for stock and 5.11 s for the edit. The median paired ratio was 2.82×.

On Switch accessories, the Mac median was 14.03 s for stock and 5.30 s for the edit. The median paired ratio was 2.65×.

On iPhone 13 batteries, the Mac median was 16.86 s for stock and 6.29 s for the edit. The median paired ratio was 2.68×.

The untouched green-tea query earned zero on the edited run. It filled the field 11 times and issued one invalid bare key command over 12 decisions. It never submitted the field. That run contributes to the pass counts and has no speed ratio.

On the first passing USB Wi-Fi adapter Mac pair, stock generated 377 tokens across 3 decisions and the edit generated 24 tokens across 3 decisions. Inference time fell from 11.49 s to 2.82 s.

On the first passing Switch accessories Mac pair, stock generated 312 tokens across 3 decisions and the edit generated 23 tokens across 3 decisions. Inference time fell from 11.73 s to 2.53 s.

On the first passing iPhone 13 batteries Mac pair, stock generated 413 tokens across 4 decisions and the edit generated 26 tokens across 3 decisions. Inference time fell from 13.79 s to 3.29 s.

On the RTX USB search, inference took 2.43 s for stock and 0.99 s for the edit. The rest of the browser loop took 2.80 s and 2.83 s. The tokenizer, cursor and typing delays matched.

An initial RTX lease request timed out while inventorying Docker. That request started zero episodes. The graded RTX runs used a separate admitted lease with the same checkpoint and a dedicated Windows Brave session.

The shard differs from Inkling 2 Mini in 9,171 BF16 values across four output rows (34, 200004, 200006 and 200008). Every byte outside those rows and all auxiliary inference files match upstream. The candidate shard’s SHA-256 is `ff8222dba1c5f343365251899ae5c7a57d6bed037633e85f16460715e3200060`.

The native grader reproduced all 18 recorded outcomes. Across project checkpoints, 25 of the 812 WebArena task IDs have native grades and 23 have both original and edited grades.

[Full browser recordings](../evidence/webarena-search-command/recordings.zip) · [Native grade replay](../evidence/webarena-search-command/receipts.zip) · [Byte audit](../evidence/webarena-search-command/stop-weight-audit.json) · [Every paired timing](../evidence/webarena-search-command/results.json)

```sh
python benchmark/replay_search.py evidence/webarena-search-command/receipts.zip
```

To time a new Mac pair with the pinned shopping fixture, run the following from the repository with Docker, Brave, the Inkling-compatible MLX runtime and WebArena-Verified 1.2.3 installed. This invocation starts the fixture locally. The reported Mac runs used a fixture on the LAN.

```sh
python benchmark/run_search_mac.py ORIGINAL EDITED --id 274 --repeats 2 --out usb-search-rerun
```

[Download the standalone command-stop checkpoint](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/bfd5050f8fb5ff8325ecde3008b842aeec2d467a).
