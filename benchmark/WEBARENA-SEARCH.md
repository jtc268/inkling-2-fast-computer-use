# One WebArena task, parallel weight edits

WebArena 274 asks the model to open search results for “usb wifi.” Each row compares full native scores on the same physical RTX 5090, with the same rendered text, browser controls, greedy decoding, cursor and reasoning setting. Variants are standalone weight edits. The full search control used a 512-token limit and at most 12 decisions.

| Edit | RTX 5090 | Original | Edited | Speed ratio on two passes | Original inference | Edited inference |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Conditional early answer | USB4 | pass · 5.31 s | pass · 4.98 s | 1.07× | 2.56 s | 2.22 s |
| Channel swap plus click/stop | USB4 | pass · 5.31 s | pass · 3.49 s | 1.52× | 2.56 s | 0.83 s |
| Direct answer with verb corrections | USB4 | pass · 5.31 s | fail · 1.79 s | — | 2.56 s | 0.73 s |
| Channel swap plus click/stop | Linux | pass · 5.29 s | pass · 3.43 s | 1.54× | 2.62 s | 1.06 s |
| Direct answer with verb corrections | Tower internal | pass · 5.11 s | fail · 1.75 s | — | 2.47 s | 0.72 s |
| Direct answer with search-key correction | USB4 | pass · 6.40 s | fail · 1.80 s | — | 2.50 s | 0.78 s |

The original was measured once for the first three USB4 trials, then retimed for the search-key trial. A failed attempt has no completion-time ratio. The original comparison, which changed only the click and stop rows, ran separately and took 4.74 s versus 4.71 s over three paired completions. [All ten tasks](https://github.com/jtc268/inkling-2-fast-computer-use/blob/main/benchmark/WEBARENA-10.md)

The 1× film shows the USB4 pair for channel swap plus click/stop. Both passed. [Video](https://jtc268.github.io/inkling-2-fast-computer-use/webarena-search-fast.mp4)

## Edits

The conditional edit adjusts two channel rows using 22 synthetic screens where immediate answering was tested against known next actions. The global swap exchanges the output rows for thinking and answering. Both retain the earlier click and end-of-generation corrections. The third edit also adjusts command-verb scores, using synthetic expected first tokens. The search-key edit instead favors the model’s native `K Enter` command on twelve synthetic focused search forms. All calculations use forward activations or explicit row swaps. No official task answers enter the weight calculation. The search task informed which hypotheses to try, so its timings are development results.

[Download the four-row checkpoint](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/fa1ef63d66ec9d489dc185cd0a8ca5452a28bfe9) · [Byte audit](https://github.com/jtc268/inkling-2-fast-computer-use/blob/main/evidence/webarena-search/direct-weight-audit.json) · [Offline grading traces](https://github.com/jtc268/inkling-2-fast-computer-use/raw/refs/heads/main/evidence/webarena-search/parallel-receipts.zip)
