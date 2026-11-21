# Form and cart replication

The original demonstration filled and submitted the official Selenium test form, then set the quantity of a product on Automation Exercise and added it to the cart. The driver checked the submitted fields and the product and quantity in the cart. These two practice sites and this exact sequence are outside the 812-task WebArena catalog.

The original six-case MacBook Pro result was 20.34 s original and 7.93 s edited, or 2.56×, with six completions each. This fresh Brave browser run used the same device, MLX, six cases, driver, greedy decoding and reasoning setting. Each case rotated the order of the four standalone checkpoints.

| Checkpoint | Passes | Joint passes with original | Original median on those cases | Edited median | Speed ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| Original | 4/6 | 4/6 | 16.62 s | 16.62 s | 1.00× |
| First release, channel swap | 6/6 | 4/6 | 16.62 s | 6.96 s | 2.39× |
| Tweeted WebArena click/stop edit | 6/6 | 4/6 | 16.62 s | 14.76 s | 1.13× |
| Channel swap plus click/stop | 6/6 | 4/6 | 16.62 s | 7.04 s | 2.36× |

Each ratio divides the two medians on the same cases where both checkpoints verified the form and cart. Live site latency is included. The first release exceeded 2.5× on two of the four completed pairs (cases 05 and 06, at 2.62× and 4.02×). Across all four, its individual ratios ranged from 1.68× to 4.02×.

| Case | Original | First release | Click/stop | Swap + click/stop |
| ---: | ---: | ---: | ---: | ---: |
| 01 | pass · 15.87 s | pass · 7.29 s | pass · 15.32 s | pass · 7.29 s |
| 02 | fail · 14.43 s | pass · 6.84 s | pass · 13.43 s | pass · 7.30 s |
| 03 | pass · 15.25 s | pass · 9.10 s | pass · 14.19 s | pass · 6.48 s |
| 04 | fail · 14.08 s | pass · 8.11 s | pass · 15.27 s | pass · 5.88 s |
| 05 | pass · 17.37 s | pass · 6.62 s | pass · 13.71 s | pass · 6.97 s |
| 06 | pass · 25.52 s | pass · 6.35 s | pass · 18.44 s | pass · 7.12 s |

Case 02, Original. control is occluded.

Case 04, Original. control is occluded.

Screenshots for cases 02 and 04 show a live product-information pop-up over the cart controls. The driver recorded the occlusion and kept both failed attempts in the results.

## Time spent generating the two plans

This excludes typing, mouse movement, page loads and cart verification. All attempts in which both page plans were generated are eligible, including failures after the second plan.

| Checkpoint | Two-plan attempts | Median model time | Median generated tokens |
| --- | ---: | ---: | ---: |
| Original | 6 | 11.23 s | 223.5 |
| First release, channel swap | 6 | 2.34 s | 34.5 |
| Tweeted WebArena click/stop edit | 6 | 9.84 s | 223.5 |
| Channel swap plus click/stop | 6 | 2.08 s | 34.5 |

## RTX 5090 checks

The same filmed case (03, Nora Reed, quantity two) was also run on CUDA. Each original/edited pair used one physical card. These are single-case observations.

| Checkpoint | Original | Edited | Ratio on joint success |
| --- | ---: | ---: | ---: |
| First release, channel swap | pass · 7.08 s | pass · 6.89 s | 1.03× |
| Channel swap plus click/stop | pass · 6.76 s | pass · 5.73 s | 1.18× |

## WebArena analogues

Task 431 compares unit prices across open tabs before adding one product. The original and click/stop models both earned 0/3. Task 630 requires typing and submitting a forum post. The original passed 3/3 and the click/stop edit passed 0/3. [Ten native WebArena tasks and replayable grades](https://github.com/jtc268/inkling-2-fast-computer-use/blob/main/benchmark/WEBARENA-10.md) · [WebArena-Verified](https://github.com/ServiceNow/webarena-verified)

[Fresh recording of case 03 at 1×](https://jtc268.github.io/inkling-2-fast-computer-use/form-cart-recheck.mp4) · [All 24 Mac run receipts and four CUDA receipts](https://github.com/jtc268/inkling-2-fast-computer-use/raw/refs/heads/main/evidence/form-cart-recheck/receipts.zip) · [WebArena task catalog](https://github.com/web-arena-x/webarena/blob/main/config_files/test.raw.json)

## The form and cart edits on native WebArena tasks

Each checkpoint ran once on the native cart and forum tasks. The first-release pair used the Linux RTX 5090. The four-row pair used the USB4 RTX 5090. Each pair used the same hardware, decoding settings and browser driver. Every attempt began with a fresh fixture and received a WebArena-Verified grade. Task 431 requires comparing unit prices across tabs before adding a product. Task 630 requires writing and submitting a forum post. Task 653 on the internal 5090 asks the model to fill the store’s contact form with a refund request, order number and SKU, leaving it unsubmitted. Its native grader only requires a successful GET of the contact page and a success response from the agent. It does not inspect the unsubmitted field values.

| Official task | Weight edit | Original | Edited | Speed ratio on joint completion |
| --- | --- | ---: | ---: | ---: |
| 431 | First release | fail · 16.09 s | fail · 10.01 s | — |
| 431 | Four-row edit | fail · 15.82 s | fail · 8.89 s | — |
| 630 | First release | pass · 21.04 s | fail · 2.50 s | — |
| 630 | Four-row edit | pass · 20.22 s | fail · 2.42 s | — |
| 653 | Four-row edit | fail · 26.87 s | fail · 4.75 s | — |

The four-row edit alternated between the first two product tabs on 431. On 630 it declared navigation complete before posting. Both attempts earned zero.

The four-row checkpoint also ran on WebArena search 274 on the third physical RTX 5090. Original 1/1 in 5.33 s. Edited 1/1 in 3.45 s. Both passed, a 1.55× speedup. [Twelve grade receipts and network traces](https://github.com/jtc268/inkling-2-fast-computer-use/raw/refs/heads/main/evidence/form-cart-recheck/native-analogue-receipts.zip) · [Per-run timing](https://github.com/jtc268/inkling-2-fast-computer-use/blob/main/evidence/form-cart-recheck/native-analogue-results.json)

Replay the native grades with `python benchmark/replay_search.py evidence/form-cart-recheck/native-analogue-receipts.zip` after installing the pinned project dependencies.
