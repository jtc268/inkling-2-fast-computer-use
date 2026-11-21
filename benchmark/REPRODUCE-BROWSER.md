# Reproduce the browser runs

The video opens with WebArena task 190. The model finds the total of the latest completed order in a local copy of a store. The correct answer is $65.32. The public harness reads visible page text and numbered controls, executes the model’s commands in Brave and asks WebArena-Verified to grade the result.

## Run task 190 on a Mac

Install [uv](https://docs.astral.sh/uv/), [Brave](https://brave.com/download/) and [Docker](https://docs.docker.com/desktop/setup/install/mac-install/). Start Docker with Linux/AMD64 emulation enabled. Allow disk space for two model downloads (about 20 GB each), the store image and recordings. The filmed run used an M5 Max MacBook Pro and MLX.

```sh
git clone https://github.com/jtc268/inkling-2-fast-computer-use.git
cd inkling-2-fast-computer-use
uv sync --locked --python 3.12 --extra webarena
.venv/bin/playwright install ffmpeg
.venv/bin/python benchmark/reproduce_browser.py --out runs/mac-headline
```

The runner downloads stock and the exact Mac edit, checks the output-layer shard against the published SHA-256, and runs each checkpoint twice in opposite orders. Docker starts a fresh store with the same benchmark account for each run. Use a fresh output directory and run one comparison at a time per fixture.

Each run saves the browser recording, network trace, actions, elapsed time and grade. Open `runs/mac-headline/pairs.json` for the two comparisons. A speedup requires both grades to equal 1. The timer includes model decisions and browser actions after warmup. Both models use identical cursor timing, greedy decoding, `reasoning_effort=none`, up to 12 actions and 512 generated tokens per decision. Browser, hardware, fixture placement and cache state can affect seconds.

We repeated task 190 on the M5 Max with a local Docker store. Both models returned $65.32 in both orders. Stock took 31.37 s and 46.14 s. The edit took 5.02 s and 8.18 s (6.26× and 5.64×). [Pair timings](../evidence/public-rerun/mac-pairs.json) · [Replayable grades](../evidence/public-rerun/mac-grades.zip)

On the 128 GiB Mac, both checkpoints peaked at 20.8 GiB of active MLX memory during a replay of the filmed order lookup. This measures model inference. [Allocator measurements](../evidence/public-rerun/mac-memory.json)

To measure a replay, create a fresh MLX worker for each checkpoint. Run the standard warmup, synchronize with `mlx.core.synchronize()` and call `mlx.core.reset_peak_memory()`. Replay the saved browser observations through `MlxWorker.decide_web` in order. Synchronize again and divide `mlx.core.get_peak_memory()` by 2³⁰ for GiB. The measurement excludes Brave and the Docker fixture.

## Match a video chapter

Use `--checkpoint NAME --id NUMBER` for a WebArena chapter. Download revisions and hashes are in the [checkpoint list](browser_checkpoints.json).

| Video scene | Checkpoint | Device |
| --- | --- | --- |
| Opening, completed order (190) | `mac-headline` | M5 Max |
| Canceled order (188), searches (274, 276, 277) | `order-stop` | M5 Max |
| Xbox and green tea searches (275, 278) | `filmed-click` | M5 Max |
| Form and cart, cases 02 and 03 | `two-row` | M5 Max |
| Autocomplete and email, seeds 103 and 104 | `two-row` | M5 Max |

For the form and cart, run `.venv/bin/python benchmark/run.py --mode test --arm both` from the repository root. It tests six cases on public demo sites. For MiniWoB++, use the [pinned BrowserGym setup](BROWSERGYM.md), then run these commands with the model paths from that guide.

```sh
.gym-venv/bin/python benchmark/run_headline.py --task use-autocomplete --seed 103 --output runs/autocomplete
.gym-venv/bin/python benchmark/run_headline.py --task email-inbox --seed 104 --output runs/email
```

## Check the published scores and times

With the WebArena dependencies installed, these commands replay the stored grader inputs and check the paired timings. They require neither model inference nor Docker.

```sh
.venv/bin/python benchmark/replay_search.py evidence/webarena-order-checkpoints/native-grades.zip
.venv/bin/python benchmark/verify_browser_timings.py evidence/webarena-order-checkpoints/native-grades.zip evidence/webarena-order-checkpoints/pairs.json
```

[Video and timing table](https://jtc268.github.io/inkling-2-fast-computer-use/) · [Additional runs and grades](https://jtc268.github.io/inkling-2-fast-computer-use/all-runs.html) · [WebArena paired results](WEBARENA-ORDER-CHECKPOINTS.md)
