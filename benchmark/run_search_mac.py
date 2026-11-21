"""Run two Inkling checkpoints on a single-site WebArena shopping or forum task in Brave."""
import argparse
import gc
import hashlib
import json
from pathlib import Path
import time

import mlx.core as mx
from mlx_lm import load, stream_generate
from mlx_lm.sample_utils import make_sampler

import webarena_ten as bench


class MlxWorker:
    def __init__(self, directory, digest):
        self.model, self.tokenizer = load(str(directory), trust_remote_code=True)
        self.sampler = make_sampler(temp=0)
        self.hardware = dict(engine='MLX', sampler='greedy', token_limit=512, shard_sha256=digest)

    def decide_web(self, prompt, system):
        messages = [dict(role='system', content=system), dict(role='user', content=prompt)]
        formatted = self.tokenizer.apply_chat_template(messages, tokenize=False, reasoning_effort='none')
        inputs = self.tokenizer.encode(formatted, add_special_tokens=False)
        start = time.perf_counter()
        tokens = [step.token for step in stream_generate(
            self.model, self.tokenizer, prompt=inputs, sampler=self.sampler, max_tokens=512
        )]
        text = self.tokenizer.decode(tokens, skip_special_tokens=False)
        parts = text.split('<|content_text|>')
        final = parts[-1].split('<|end_message|>')[0].split('<|content_model_end_sampling|>')[0].strip() if len(parts) > 1 else ''
        thinking = 0
        inside = False
        for token in tokens:
            if token == 200008:
                inside = True
            elif token in (200004, 200001, 200005, 200006):
                inside = False
            elif inside:
                thinking += 1
        return dict(final=final, generated=len(tokens), thinking=thinking, seconds=time.perf_counter() - start)


def shard_digest(directory):
    index = json.loads((directory / 'model.safetensors.index.json').read_text())
    shard = index['weight_map']['model.llm.unembed.weight']
    with (directory / shard).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def official_task(task_id):
    config = bench.WebArenaVerifiedConfig(
        environments={name: {'urls': [origin]} for name, origin in bench.URL.items()}
    )
    grader = bench.WebArenaVerified(config=config)
    task = grader.get_task(task_id)
    sites = [site.value for site in task.sites]
    if len(sites) != 1 or sites[0] not in bench.FIXTURE_IMAGES:
        raise ValueError(f'Task {task_id} needs {", ".join(sites)}. Supported single-site fixtures: {", ".join(bench.FIXTURE_IMAGES)}.')
    return grader, sites[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original', type=Path)
    parser.add_argument('edited', type=Path)
    parser.add_argument('--id', required=True, type=int, help='Official WebArena task ID on shopping or reddit')
    parser.add_argument('--out', required=True, type=Path, help='New directory for receipts, HARs and recordings')
    parser.add_argument('--repeats', default=2, type=int)
    parser.add_argument('--edited-first', action='store_true')
    parser.add_argument('--brave', default=bench.BRAVE)
    parser.add_argument('--field-selection', choices=('select-text', 'keyboard'), default='select-text',
                        help='Select the current field contents before typing. Historical runs used keyboard.')
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error('Use at least one repeat.')
    try:
        wa, site = official_task(args.id)
    except (ValueError, IndexError, KeyError) as exc:
        parser.error(str(exc))
    checkpoints = {'original': args.original, 'edited': args.edited}
    digests = {arm: shard_digest(directory) for arm, directory in checkpoints.items()}
    args.out.mkdir(parents=True, exist_ok=False)
    pairs = []
    with bench.sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=args.brave, headless=True)
        for i in range(args.repeats):
            folder = args.out / f'r{i+1}'
            folder.mkdir()
            order = ['edited', 'original'] if bool(i % 2) != args.edited_first else ['original', 'edited']
            initial_view=None
            for arm in order:
                worker = MlxWorker(checkpoints[arm], digests[arm])
                worker.decide_web('Click Go. Controls: 7 button Go.', bench.SYSTEM)
                bench.episode(browser, worker, wa, dict(id=args.id, site=site), arm, folder,
                              field_selection=args.field_selection,expected_start_view=initial_view)
                if site=='shopping_admin' and initial_view is None:
                    initial_view=json.loads((folder/f'{args.id:03}-{arm}.json').read_text())['steps'][0]['view']
                del worker
                gc.collect()
                mx.clear_cache()
            records = [json.loads((folder / f'{args.id:03}-{arm}.json').read_text())
                       for arm in ('original', 'edited')]
            stock, edit = records
            if any(record['grader_error'] is not None for record in records):
                raise RuntimeError(f'Native grader error in {folder}.')
            if stock['steps'][0]['view'] != edit['steps'][0]['view']:
                raise ValueError('Initial browser observations differ.')
            joint = stock['score'] == edit['score'] == 1
            pairs.append(dict(repeat=i+1, order=order, original_score=stock['score'], edited_score=edit['score'],
                              original_s=stock['elapsed_s'], edited_s=edit['elapsed_s'],
                              ratio=stock['elapsed_s'] / edit['elapsed_s'] if joint else None))
            bench.write_json(args.out / 'pairs.json', dict(id=args.id, shard_sha256=digests, pairs=pairs))
        browser.close()


if __name__ == '__main__':
    main()
