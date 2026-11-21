# Inkling 2 Mini Fast Browser Use

On WebArena’s completed-order lookup, Inkling 2 Mini returned the correct total in **5.13 s** after a four-row weight edit. The original took **45.89 s** on the same M5 Max MacBook Pro. Both issued the same three clicks and returned **$65.32**. The **8.95×** result is the faster of two passing pairs. Reversing run order gave **8.00×**.

[Real-time recordings and task timings](https://jtc268.github.io/inkling-2-fast-computer-use/) · [Exact weights for WebArena 190](https://huggingface.co/husky8/Inkling-2-Mini-Fast-Browser-Use/tree/686faa4d1748f0120008ec007dc97677678e1643) · [Weight diff](evidence/webarena-order-checkpoints/complete-cross/weight-audit.json)

## Where the time went

| WebArena 190, M5 Max MacBook Pro | Original Inkling 2 Mini | Edited Inkling 2 Mini |
|---|---:|---:|
| Task completion | 45.89 s | 5.13 s |
| Inference | 43.03 s | 2.84 s |
| Generated tokens | 1,555 | 28 |
| Thinking tokens | 1,509 | 0 |

We developed this checkpoint on task 190. The two runs used the same storefront, prompt, Brave controls, cursor timing and MLX greedy decoder. Both set `reasoning_effort=none`. The original generated one empty action in addition to the three clicks and the answer.

## Weight edit

The completed-order checkpoint changes **9,192 BF16 values** in `model.llm.unembed.weight`, the output matrix with 201,024 rows and 2,304 columns. We exchanged the answer-text and thinking rows (200004 and 200008) and adjusted the click-command and end-of-generation rows (34 and 200006). We used no additional training. The audit records byte offsets and SHA-256 digests for the original and edited rows. [Byte-level audit](evidence/webarena-order-checkpoints/complete-cross/weight-audit.json)

The 11 filmed comparisons use four edited checkpoints. Both models passed each selected task. Mean completion time was **20.42 s original** and **5.30 s edited**. Dividing total original time by total edited time gives **3.85×** for this selection. On a separate panel of 20 MiniWoB++ cases, the original passed 11 and the two-row edit passed 6. [Filmed timings](https://huggingface.co/husky8/Inkling-2-Mini-Fast-Browser-Use/blob/84e26036e22c6a1a4420cf37285c5f8a3946f4ec/benchmark/speedups-timings.json) · [Paired receipts](https://huggingface.co/husky8/Inkling-2-Mini-Fast-Browser-Use/resolve/84e26036e22c6a1a4420cf37285c5f8a3946f4ec/benchmark/speedups-film-receipts.zip) · [MiniWoB++ scores](benchmark/BROWSERGYM.md)

On the 128 GiB Mac, both checkpoints peaked at 20.8 GiB of active MLX memory during a replay of the filmed order lookup. This measures model inference. [Measurement record](evidence/public-rerun/mac-memory.json)

## Reproduce the completed-order lookup

Install Brave, Docker and `uv` on Apple silicon. Start Docker with Linux/AMD64 emulation enabled.

```sh
git clone https://github.com/jtc268/inkling-2-fast-computer-use.git
cd inkling-2-fast-computer-use
uv sync --locked --python 3.12 --extra webarena
.venv/bin/playwright install ffmpeg
.venv/bin/python benchmark/reproduce_browser.py --out runs/mac-headline
```

The runner downloads the pinned checkpoints, checks their hashes and executes both model orders. Each arm starts with a fresh store. The output directory contains the browser recordings, observations, actions, grades and `pairs.json`. [Fixture setup, alternative tasks and grade replay](benchmark/REPRODUCE-BROWSER.md)

## Use the edited weights

The model card’s default revision contains the two-row edit used for the forms and MiniWoB++ runs. To use the four-row completed-order edit, download its exact revision. The caller supplies browser observations and executes the model’s commands. [Checkpoint registry](benchmark/browser_checkpoints.json)

```sh
hf download husky8/Inkling-2-Mini-Fast-Browser-Use \
  --revision 686faa4d1748f0120008ec007dc97677678e1643 --local-dir inkling-browser
```

To run the form-and-cart harness, use `.venv/bin/python benchmark/run.py`. Set `INKLING_EDITED` to select an existing local checkpoint. [Form-and-cart comparisons](benchmark/FORM-CART-RECHECK.md)

Base model by Thinking Machines Lab. [Inkling 2 Mini](https://huggingface.co/thinkingmachines/Inkling-2-Mini) · [Apache 2.0](LICENSE) · [Cursor motion license](benchmark/CUA-LICENSE.txt)
