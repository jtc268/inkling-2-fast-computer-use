"""Repeat one timed checkpoint on the frozen ten-task panel with local fixtures."""
import argparse
import json
from pathlib import Path
from urllib.request import urlopen

import webarena_ten as bench
from cuda_worker import CudaWorker


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--endpoint', required=True, help='SGLang HTTP origin')
    parser.add_argument('--model-id', required=True, help='Expected served model name')
    parser.add_argument('--tokenizer', required=True, type=Path)
    parser.add_argument('--arm', required=True, choices=('original', 'candidate'))
    parser.add_argument('--gpu-uuid', required=True, help='Physical device identifier for the receipt')
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--ids', nargs='+', type=int, help='Optional subset of the ten official IDs')
    parser.add_argument('--repetitions', type=int, default=3)
    args = parser.parse_args()
    tasks = bench.PANEL['tasks']
    requested = set(args.ids or [t['id'] for t in tasks])
    if requested - {t['id'] for t in tasks} or args.repetitions < 1:
        parser.error('Choose IDs from the frozen panel and at least one repetition.')
    with urlopen(args.endpoint.rstrip('/')+'/v1/models', timeout=6) as response:
        names = {model['id'] for model in json.load(response)['data']}
    if args.model_id not in names:
        raise ValueError('The endpoint is serving a different model.')
    hw = dict(engine='SGLang', device='CUDA', gpu_uuid=args.gpu_uuid, served_model=args.model_id, sampler='greedy', token_limit=512)
    worker = CudaWorker(args.endpoint, args.tokenizer, hw, token_limit=512)
    worker.decide_web('Click Go. Controls: 7 button Go.', bench.SYSTEM)
    with bench.sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=bench.BRAVE, headless=True)
        try:
            for rep in range(1, args.repetitions + 1):
                out = args.out / f'r{rep}'
                out.mkdir(parents=True, exist_ok=True)
                for task in tasks:
                    if task['id'] not in requested or (out / f"{task['id']:03d}-{args.arm}.json").is_file():
                        continue
                    site = task['site']
                    config = bench.WebArenaVerifiedConfig(environments={site: {'urls': [bench.URL[site]]}})
                    bench.episode(browser, worker, bench.WebArenaVerified(config=config), task, args.arm, out)
        finally:
            browser.close()


if __name__ == '__main__':
    main()
