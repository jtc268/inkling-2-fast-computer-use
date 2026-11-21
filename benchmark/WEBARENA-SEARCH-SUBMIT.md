# Submitting a shopping search in WebArena

The earlier four-row checkpoint entered “switch accessories” and declared success on the home page. The native grader gave it zero. We changed the output row for the click command using that failed decision and synthetic search pages. The edit raises the click score on a filled search box while constraining the change on sampled empty boxes, results pages and command arguments.

The new checkpoint differs from its predecessor in one row and from Inkling 2 Mini in four rows of `model.llm.unembed.weight`. The browser prompt, greedy decoding, reasoning setting, cursor animation and typing delays matched within each pair. The model received visible page text and numbered controls. Time starts at the first observation and ends at the model’s final action. Every episode used a fresh signed-in fixture. The Mac pairs reversed execution order on the repeat.

| Device | Task | Role | Repeat | Original | Edited | Both passed |
|---|---|---|---:|---:|---:|---:|
| M5 Max MacBook Pro | 276 · Switch accessories | development | 1 | 17.22 s · pass | 7.60 s · pass | 2.27× |
| M5 Max MacBook Pro | 274 · USB Wi-Fi adapter | prior control | 1 | 14.80 s · pass | 27.61 s · pass | 0.54× |
| M5 Max MacBook Pro | 276 · Switch accessories | development | 2 | 13.43 s · pass | 6.20 s · pass | 2.17× |
| M5 Max MacBook Pro | 274 · USB Wi-Fi adapter | prior control | 2 | 14.21 s · pass | 19.98 s · pass | 0.71× |
| M5 Max MacBook Pro | 277 · iPhone 13 batteries | held out | 1 | 16.85 s · pass | 3.78 s · fail | — |
| M5 Max MacBook Pro | 277 · iPhone 13 batteries | held out | 2 | 16.67 s · pass | 3.76 s · fail | — |
| RTX 5090 | 276 · Switch accessories | development | 1 | 5.09 s · pass | 6.64 s · pass | 0.77× |
| RTX 5090 | 274 · USB Wi-Fi adapter | prior control | 1 | 4.72 s · pass | 6.08 s · pass | 0.78× |

Both Mac repeats on Switch accessories passed. The median paired speed ratio was 2.22×. The USB Wi-Fi control took 14.51 s for stock and 23.79 s for the edit across joint successes. On the held-out battery query, stock passed 2/2 and the edit passed 0/2. On both attempts the edit filled the field and declared success before clicking Search.

On RTX 5090 the Switch-accessories pair took 5.09 s for stock and 6.64 s for the edit. The edited checkpoint reached the 512-token cap on its click decision in both RTX searches.

The byte audit found 2,293 changed BF16 values in click row 34 versus the prior edit and 9,162 across four output rows versus stock. All other shard bytes and auxiliary model files matched. The edit used a direct linear solve without gradient training. Its constraints apply to the sampled states. Accuracy on other tasks remains open.

The project has native grades for 24 distinct WebArena IDs across experimental checkpoints. The original and at least one edit have grades on 22 IDs. The full suite contains 812 tasks.

16 grades reproduced with the network traces. [Download the traces](../evidence/webarena-search-submit/receipts.zip) · [Results and median paired ratios](../evidence/webarena-search-submit/summary.json) · [Byte audit](../evidence/webarena-search-submit/weight-audit.json) · [Full real-time recordings](../evidence/webarena-search-submit/recordings.zip)

```sh
python benchmark/replay_search.py evidence/webarena-search-submit/receipts.zip
```

To verify downloaded checkpoints against the measured four-row edit, run

```sh
python benchmark/verify_output_rows.py ORIGINAL EDITED --rows 34 200004 200006 200008 --expect-base-sha256 65e60f51aa1284d4fb022584908c315270334d991828bb774af60584523539d1 --out weights.json
```

[Download the standalone search-submit weights](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/658c5be9d81f5b2374bf6576d31ad47df904b0db).
