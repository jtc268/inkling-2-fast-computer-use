# WebArena coverage and new shopping cases

There are native grades for **23 distinct WebArena task IDs**. The original checkpoint and at least one weight edit have grades on **21 IDs**. The repeated ten-task panel ran three times per checkpoint. Counts include failures and earlier exploratory checkpoints.

The frozen four-row checkpoint ran an existing search control and two new shopping tasks on RTX 5090. Each original/edit pair used the same model runtime, prompt, decode settings, browser controls and native evaluator. Each episode started after model warmup and a fixture reset. The native grader's results were independently replayed with the saved network events.

The first control setup retried before timing while the recorder located its encoder. The trace exporter then needed the new fixture port to replay the saved control. The original native grade and clock were retained.

| WebArena task | Original | Four-row edit | Time ratio on joint success |
| --- | ---: | ---: | ---: |
| 274 · USB Wi-Fi search · prior control | pass · 5.31 s | pass · 3.55 s | 1.49× |
| 276 · Switch accessories search · new | pass · 5.38 s | fail · 1.74 s | — |
| 270 · Men’s shoes below $30 · new | fail · 26.59 s | fail · 7.78 s | — |

The catalog contains 812 task IDs. The search control is counted once in coverage, regardless of repeat count. MiniWoB++ seeds, Selenium forms and the manually constructed Xbox grader control are excluded. A single paired attempt on each new ID establishes an outcome on that case. It does not establish a full-suite speed or accuracy rate. [Coverage by task ID](../evidence/webarena-expansion/coverage.json) · [Six grade receipts and replay inputs](../evidence/webarena-expansion/receipts.zip) · [Selection and settings](../evidence/webarena-expansion/protocol.json)

To reproduce all six grades offline, run this from the repository with WebArena-Verified 1.2.3 installed.

~~~sh
python benchmark/replay_search.py evidence/webarena-expansion/receipts.zip
~~~
