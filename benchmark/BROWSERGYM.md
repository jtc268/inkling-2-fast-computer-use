# Five BrowserGym environments

The two checkpoints run in Brave through Gymnasium and BrowserGym’s MiniWoB++ integration. Seeds 101–104 are paired in each environment. The task page and native grader come from the MiniWoB++ revision recommended by BrowserGym. The agent sees the goal, a compact rendered DOM including offscreen rows, and its previous actions. BrowserGym executes one click or fill per decision. No screenshot enters the model.

The checkpoints alternate order across tasks and seeds. Each gets up to 16 decisions and 384 generated tokens per decision. An invalid command or the same action repeated in the same state ends the run. Completion requires a positive native reward. Wall times exclude environment setup and checkpoint loading. Compare latency on seeds both models solved.

## Reproduce

Start in this repository with the model environment installed from the main README. Use a second Python environment for BrowserGym’s Playwright dependency. The benchmark stores one receipt per task, seed and checkpoint and resumes if interrupted. Set a fresh output directory for a new trial.

~~~sh
uv venv --python 3.12 .gym-venv
uv pip install --python .gym-venv/bin/python browsergym-core==0.14.3 browsergym-miniwob==0.14.3
PLAYWRIGHT_BROWSERS_PATH=0 .gym-venv/bin/playwright install chromium
git clone https://github.com/Farama-Foundation/miniwob-plusplus.git miniwob-plusplus
git -C miniwob-plusplus checkout 7fd85d71a4b60325c6585396ec4f48377d049838
.venv/bin/hf download thinkingmachines/Inkling-2-Mini --revision ed40e7da625f594fc9c4990f5f66be24873c22d7 --local-dir original
.venv/bin/hf download husky8/Inkling-2-Mini-Fast-Browser-Use --revision d4562716ff6d8d0281bf09814a1df0db570f6be3 --local-dir edited
export INKLING_ORIGINAL="$PWD/original" INKLING_EDITED="$PWD/edited"
export INKLING_MLX_PYTHON="$PWD/.venv/bin/python"
export MINIWOB_URL="$(.gym-venv/bin/python -c 'from pathlib import Path; print(Path("miniwob-plusplus/miniwob/html/miniwob").resolve().as_uri()+"/")')"
export PLAYWRIGHT_BROWSERS_PATH=0
.gym-venv/bin/python benchmark/gym.py
python3 benchmark/score_gym.py gym-runs browsergym-summary.json
~~~

Brave is the task browser. BrowserGym also launches its bundled Chromium for its internal chat panel. BRAVE_PATH overrides the default macOS application path.

[BrowserGym setup](https://github.com/ServiceNow/BrowserGym/tree/main/browsergym/miniwob) · [MiniWoB++ task definitions](https://miniwob.farama.org/environments/list/)
