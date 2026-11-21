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

A clean checkout reran task 190 on the M5 Max with a local Docker store. Both models returned $65.32 in both orders. Stock took 31.37 s and 46.14 s. The edit took 5.02 s and 8.18 s (6.26× and 5.64×). [Pair timings](../evidence/public-rerun/mac-pairs.json) · [Replayable grades](../evidence/public-rerun/mac-grades.zip)

## Run the RTX comparison

Use the same setup commands on an NVIDIA Linux host with Brave and the NVIDIA Container Toolkit. The runner starts the [pinned SGLang image](sglang_browser.py) on the selected device, checks the loaded checkpoint and uses the same GPU for both arms. The first launch compiles inference kernels. Docker keeps those kernels for repeat runs. The published search-submit comparison used an RTX 5090 and Windows Brave.

```sh
for id in 275 190 189; do
  .venv/bin/python benchmark/reproduce_browser.py --engine rtx \
    --checkpoint search-submit --id "$id" --out "runs/rtx-$id"
done
```

The default uses local Brave. For a separate browser host, start a dedicated Brave profile with a loopback debugging port and pass its forwarded URL via `--cdp`. The browser must reach the fixture at the same loopback URL as the runner (shopping 7770, forum 9999). The runner also needs the corresponding fixture control port (7771 or 9998). Use `--gpu` to select a GPU by index or UUID. For existing checkpoint folders, pass `--original PATH --edited PATH`. The same shard checks apply.

## Match a video chapter

Use `--checkpoint NAME --id NUMBER` for a WebArena chapter. The opening and the later task 190 scene use different checkpoints. Download revisions and hashes are in the [checkpoint list](browser_checkpoints.json).

| Video scene | Checkpoint | Device |
| --- | --- | --- |
| Opening, completed order (190) | `mac-headline` | M5 Max |
| Canceled or pending orders (188, 189), searches (274, 276, 277) | `order-stop` | M5 Max |
| Completed order (190), later scene | `pending-stop` | M5 Max |
| Xbox and green tea searches (275, 278) | `filmed-click` | M5 Max |
| Headphone forum post (630) | `forum` | RTX 5090 |
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

[Video and timing table](https://jtc268.github.io/inkling-2-fast-computer-use/) · [All filmed outcomes](https://jtc268.github.io/inkling-2-fast-computer-use/all-runs.html) · [WebArena paired results](WEBARENA-ORDER-CHECKPOINTS.md)
