# Closing browser reasoning earlier

WebArena 630 requires composing and submitting a forum post. WebArena 274 is the USB Wi-Fi search used in the earlier speed check. Each row pairs upstream with a standalone edit on the same RTX 5090. Warm model, greedy decoding, the same reasoning setting, cursor, typing delay and native grader throughout.

| WebArena ID | GPU | Edit | Original | Edited | Speed on two passes | Thinking tokens, original → edit |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| 630 | linux | Moderate end-message edit | pass · 28.64 s | fail · 29.12 s | — | 1478 → 3070 |
| 274 | linux | Moderate end-message edit | pass · 4.93 s | pass · 4.97 s | 0.99× | 274 → 274 |
| 630 | usb | Stronger end-message edit | pass · 22.34 s | pass · 17.97 s | 1.24× | 1368 → 944 |
| 274 | usb | Stronger end-message edit | pass · 6.79 s | pass · 6.31 s | 1.08× | 274 → 274 |
| 630 | internal | Moderate edit plus click spelling | fail · 13.12 s | fail · 31.39 s | — | 1081 → 3197 |
| 274 | internal | Moderate edit plus click spelling | pass · 6.35 s | pass · 6.17 s | 1.03× | 318 → 270 |

The edit changes the row for Inkling’s native end-of-message token (200010). One version also changes row 34, which scores the click verb. The thinking and answer channel rows retain their upstream values. The weight calculation used unrelated synthetic browser screens and measured whether forcing a transition at different reasoning lengths still yielded the correct command. Rows were solved directly and rounded to BF16. Every unchanged shard byte and auxiliary model file was compared against upstream.

Initial text observations were identical in 5/6 pairs. All 12 official grades were replayed from the saved network traces. These six pairs are exploratory timing measurements.

In the successful exploratory forum pair, all nine browser commands matched. The stronger edit cut thinking tokens from 1,368 to 944. Of the 424 tokens saved, 409 came before the first command, a bare control number the driver rejected in both runs. The remaining 15 came before filling the post body.

## Independent Linux verification

The independent RTX 5090 repeat evaluated the edited checkpoint first. Each episode began with an empty model prefix cache, a shared warmup and a fresh browser fixture. There was no background model calibration or checkpoint hashing during timing.

| Task | Pair | Upstream | Edited | Speed on two passes | Inference, upstream → edit |
| --- | --- | ---: | ---: | ---: | ---: |
| 630 | r1 | pass · 22.69 s | pass · 18.64 s | 1.22× | 11.18 s → 7.99 s |
| 630 | r2 | pass · 24.52 s | pass · 20.56 s | 1.19× | 10.77 s → 8.54 s |
| 274 | r1 | pass · 5.05 s | pass · 4.68 s | 1.08× | 2.34 s → 2.34 s |

Across the 2 jointly successful fresh forum pairs, the medians were 23.60 s original and 19.60 s edited (1.20×).

On ten distinct synthetic action checks, correct commands and median generated tokens were original 8/10 and 75 tokens, linux 8/10 and 75 tokens, usb 8/10 and 75 tokens, internal 8/10 and 75 tokens.

The attempted USB4 repeat did not start an episode. Docker inventory timed out before lease admission, so the order-reversed checks ran on Linux.

[Exploratory receipts](https://github.com/jtc268/inkling-2-fast-computer-use/raw/refs/heads/main/evidence/webarena-reasoning-close/receipts.zip) · [Order-reversed receipts](https://github.com/jtc268/inkling-2-fast-computer-use/raw/refs/heads/main/evidence/webarena-reasoning-close/independent-receipts.zip). Replay either archive with `python benchmark/replay_search.py ARCHIVE.zip`. [Forum post at 1×](https://jtc268.github.io/inkling-2-fast-computer-use/webarena-forum.mp4). [Download the one-row checkpoint](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/forum-reasoning-close).

## End-message row with ranking constraints

On 21 unrelated synthetic screens, the command was verified at a prefix the original model normally used for thinking. The revised end-message row had the highest raw next-token score at 21 chosen positions after BF16 rounding. Its displacement was 0.520 times the original row norm. The fit used 248 additional token-ranking constraints.

| Task | Original | Edited | Ratio on joint completion |
| --- | ---: | ---: | ---: |
| 630 | pass · 23.39 s | fail · 25.24 s | — |
| 274 | pass · 4.83 s | pass · 5.15 s | 0.94× |
