# Browser-use results · work in progress

**5.18× on one autocomplete case.** In the initial MiniWoB++ panel, case 103 took 19.86 s with the original Inkling 2 Mini and 3.84 s with the two-row checkpoint. Both passed on M5 Max MacBook Pro. For the same case on the M5 Max MacBook Pro, the independent video retake measured 15.46 → 3.36 seconds, saving 12.11 seconds. This is the largest individual ratio across the MiniWoB++ and form-and-cart comparisons listed here.

| Browser task | Original → edited | Speed | What passed |
| --- | ---: | ---: | --- |
| Autocomplete, original four seeds | 23.01 → 4.53 s | 5.08× | Original 2/4, edit 3/4, 2 joint |
| Autocomplete, same four seeds filmed again | 18.59 → 4.85 s | 3.83× | Original 2/4, edit 3/4, 2 joint |
| Reply to a specified email, original seed 104 | 30.00 → 7.02 s | 4.27× | Both passed the browser task |
| Email reply, same seed filmed again | 21.48 → 5.86 s | 3.66× | Original 1/1, edit 1/1, 1 joint |
| Email reply, separately timed video take | 26.01 → 5.98 s | 4.35× | Original 1/1, edit 1/1, 1 joint |
| Autocomplete, separately timed video take | 15.46 → 3.36 s | 4.61× | Original 1/1, edit 1/1, 1 joint |
| Email reply, same case on RTX 5090 | 6.68 → 4.32 s | 1.55× | Original 1/1, edit 1/1, 1 joint |
| Autocomplete, same case on RTX 5090 | 3.90 → 2.48 s | 1.57× | Original 1/1, edit 1/1, 1 joint |
| Initial form submission | 10.12 → 3.68 s | 2.75× | Original 6/6, edit 6/6, 6 joint |
| Repeated form submission | 8.53 → 3.03 s | 2.81× | Original 6/6, edit 6/6, 6 joint |
| Initial form and cart | 20.34 → 7.93 s | 2.57× | Original 6/6, edit 6/6, 6 joint |
| Repeated form and cart | 16.62 → 6.96 s | 2.39× | Original 4/6, edit 6/6, 4 joint |

Task-level ratios divide the two medians on the same successful pairs. Seconds saved and ratios use unrounded timings. The form timer ends when the submitted URL contains both requested field values. The cart timer ends after verifying the product and quantity. Both include model time and browser execution. The model read DOM text and sent actions to Brave on an M5 Max MacBook Pro using MLX. Each matched comparison used the same prompts and greedy decoding. The RTX 5090 comparison used SGLang for local-network inference, with the same Brave driver, field observations and native grader as the Mac runs. [M5 Max hardware verification](../evidence/headliners/hardware-proof.json) · [RTX 5090 case receipts](../evidence/headliners/rtx-headline-receipts.zip).

In the original autocomplete run on seed 103, both models issued exactly the same two commands. The original emitted 275 thinking-channel tokens and the edit emitted 0. Measured inference time fell from 18.11 to 2.06 seconds with greedy decoding and reasoning effort set to `none` in both arms.

The first release swapped the thinking and answer output rows. On the full five-task, 20-case MiniWoB++ panel, the original passed 11/20 and the edit passed 6/20. The email-reply example is one selected seed. The filmed autocomplete set includes all four published seeds. [Full BrowserGym panel](https://github.com/jtc268/inkling-2-fast-computer-use/blob/main/benchmark/BROWSERGYM.md) · [Original checkpoint revision](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/91ad325a3ba495d81838ff408d95ebf7ca5c79cd)

**WebArena on RTX 5090.** A separate four-row edit completed shopping search 1.52–1.55× faster in paired RTX 5090 runs. A one-row edit completed a forum post 1.20× faster in two independent paired repeats. Both models passed all three forum comparisons. WebArena also has a lowest-unit-price cart task (431) and a refund form (653). Neither the original nor the four-row edit passed those cases. The Selenium-to-cart workflow is a separate benchmark. The 2× WebArena target and full-suite accuracy remain open. [Cart and refund-form results](https://github.com/jtc268/inkling-2-fast-computer-use/blob/main/benchmark/FORM-CART-RECHECK.md) [Search results](https://github.com/jtc268/inkling-2-fast-computer-use/blob/main/benchmark/WEBARENA-SEARCH.md) · [Forum results](https://github.com/jtc268/inkling-2-fast-computer-use/blob/main/benchmark/WEBARENA-REASONING-CLOSE.md)

## Recordings

| Clip | Original → edited | Clip ratio | Video |
| --- | ---: | ---: | --- |
| Autocomplete | 15.46 → 3.36 s | 4.61× | [Watch at 1×](https://jtc268.github.io/inkling-2-fast-computer-use/headline-autocomplete.mp4) |
| Email reply | 26.01 → 5.98 s | 4.35× | [Watch at 1×](https://jtc268.github.io/inkling-2-fast-computer-use/headline-email-reply.mp4) |
| Form submit | 8.64 → 3.06 s | 2.83× | [Watch at 1×](https://jtc268.github.io/inkling-2-fast-computer-use/headline-form-submit.mp4) |

Each autocomplete and email clip uses a fresh native-reward pair. The autocomplete seed was selected by the fastest jointly successful result in the four-seed repeat. The table shows the separately timed video takes. Full task surfaces were sampled up to eight times per second and rendered at 1× against the native grade clock. [Timestamped source images, capture code and grade receipts](https://github.com/jtc268/inkling-2-fast-computer-use/raw/refs/heads/main/evidence/headliners/screen-recording-sources.zip). The Selenium clip is the paired form-stage recording closest to the repeated six-case ratio of medians. [All timing data](https://github.com/jtc268/inkling-2-fast-computer-use/blob/main/evidence/headliners/headline-evidence.json) · [Download the scorecard](https://jtc268.github.io/inkling-2-fast-computer-use/browser-use-scorecard.png) · [All freshly filmed outcomes and unedited browser recordings](https://github.com/jtc268/inkling-2-fast-computer-use/raw/refs/heads/main/evidence/headliners/filmed-receipts.zip)

## Run the same case

Use the two Python environments, pinned MiniWoB checkout and model paths from [BrowserGym setup](https://github.com/jtc268/inkling-2-fast-computer-use/blob/main/benchmark/BROWSERGYM.md). From the repository, run the following with the BrowserGym environment. It writes both native grade receipts.

~~~sh
python benchmark/run_headline.py --task use-autocomplete --seed 103 --output headline-103
~~~
