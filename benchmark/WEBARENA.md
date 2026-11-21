# Twenty WebArena tasks

Brave runs on a MacBook Pro. For the CUDA panel a pair of checkpoints runs on the same physical RTX 5090 for each task. Each gets the official user intent, the titles of open tabs, the current URL path, and text and numbered controls visible in a 1200 × 720 viewport. The model can click, hover, type, select, submit, scroll, go back, switch tabs and return an answer. A shared mouse driver takes 360 ms per click movement and types at 25 ms per character.

The [20 task IDs](../evidence/webarena-panel.json) were published before the first episode. Thirteen come from the WebArena storefront and seven from the forum. We chose recognizable consumer tasks from the 812-task catalog. Each pair runs once. Arm order alternates by manifest index. Each episode starts with a fresh container from the pinned upstream image and a fresh browser context. The host permits requests only to the current fixture. Setup, model warmup and grading are outside the clock. Elapsed time includes the model, browser actions and final answer. One task opens three tabs.

The inference worker uses greedy decoding with the same prompt, reasoning setting and a maximum of 384 generated tokens per decision. At most eight decisions are allowed. Both models see DOM text. The screen recording shows the real browser at 1×. The recorded surface follows the initial tab in a multi-tab task.

[WebArena-Verified v1.2.3](https://github.com/ServiceNow/webarena-verified) grades the agent's final response and the browser network trace. A pass requires a full score of 1.0. As an unscored control, an Xbox search received 1.0 for the Xbox goal and 0.0 for a different search goal. [Control scores](../evidence/webarena-grader-control.json)

## Run a CUDA case

The primary comparison used the same SGLang image on RTX 5090. The upstream arm went first on the even indices and the selective arm went first on the odd indices. Each device loaded the opposite checkpoint from disk before repeating its tasks. A separate RTX 5090 baseline repeated the upstream arm. [Hardware assignments](../evidence/webarena-cuda-protocol.json)

For a short development loop, load your checkpoint in SGLang and run a single task. Change the output directory for each repeat. Set up the dependencies below first.

~~~sh
.venv/bin/python benchmark/run_cuda.py --endpoint http://127.0.0.1:30000 \
  --model-name inkling-wa-selective --tokenizer /path/to/checkpoint \
  --arm selective --task 274 --out runs/search-01
~~~

Use the same GPU, prompt, server settings and task for the upstream arm. A full comparison omits the task filter. The private SGLang serving profile used 8,192 context, four maximum running requests, FA4 attention, 4,096 chunked prefill, greedy decoding and the same NVFP4 model format. The image ID for these runs was `sha256:efac853b46811ccb760545b7b29e7119bdf907537ccf6e863fac3011fe8b98de`. Browser and GPU communicate via local SSH forwards. Public network records replay offline with the official grader.

## Run the Mac version

Install Docker Desktop, Brave, uv and both checkpoints. From the repository root, on a compatible Apple Silicon Mac:

~~~sh
uv sync --frozen
uv pip install --python .venv/bin/python webarena-verified==1.2.3
export INKLING_ORIGINAL=/absolute/path/to/upstream-inkling
export INKLING_EDITED=/absolute/path/to/selective-inkling
.venv/bin/python benchmark/webarena.py --out webarena-runs
~~~

The runner uses loopback ports 7770, 7771, 9998 and 9999. It recreates only containers with its experiment label and saves a receipt, original HAR and real-time video locally. Completed receipts are resumable. The downloadable checkpoint is the complete selective edit. It requires a compatible inference runtime and an agent that supplies browser observations and executes the model's actions.

[Standalone model](https://huggingface.co/husky8/Inkling-2-Fast-Computer-Use/tree/selective-experiment) · [Weight audit](../evidence/selective-weight-audit.json) · [Nine calibration screens](../evidence/calibration-prompts.json) · [Reproduce the edited rows](derive_selective_rows.py)
