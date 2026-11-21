# Twenty WebArena tasks

Two checkpoints operate Brave on the same MacBook Pro. Each gets the official user intent, the titles of open tabs, the current URL path, and text and numbered controls visible in a 1200 × 720 viewport. The model can click, hover, type, select, submit, scroll, go back, switch tabs and return an answer. A shared mouse driver takes 360 ms per click movement and types at 25 ms per character.

The [20 task IDs](../evidence/webarena-panel.json) were published before the first episode. Thirteen come from the WebArena storefront and seven from the forum. We chose recognizable consumer tasks from the 812-task catalog. Each pair runs once in alternating arm order. Each episode starts with a fresh container from the pinned upstream image and a fresh browser context. The host permits requests only to the current fixture. Setup, model warmup and grading are outside the clock. Elapsed time includes the model, browser actions and final answer. One task opens three tabs.

The inference worker uses greedy decoding with the same prompt, reasoning setting and a maximum of 384 generated tokens per decision. At most eight decisions are allowed. Both models see DOM text. The screen recording shows the real browser at 1×. The recorded surface follows the initial tab in a multi-tab task.

[WebArena-Verified v1.2.3](https://github.com/ServiceNow/webarena-verified) grades the agent's final response and the browser network trace. A pass requires a full score of 1.0. As an unscored control, an Xbox search received 1.0 for the Xbox goal and 0.0 for a different search goal. [Control scores](../evidence/webarena-grader-control.json)

## Reproduce

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
