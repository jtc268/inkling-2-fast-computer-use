"""Summarize matched BrowserGym cases; compare latency only for joint successes."""
import argparse
import json
from pathlib import Path
from statistics import median

TASKS=('email-inbox','use-autocomplete','social-media-all','choose-date','book-flight')
SEEDS=(101,102,103,104)

def summarize(pairs):
    original=[a for a,b in pairs]
    edited=[b for a,b in pairs]
    both=[(a,b) for a,b in pairs if a['success'] and b['success']]
    return dict(pairs=len(pairs),original_pass=sum(r['success'] for r in original),
                edited_pass=sum(r['success'] for r in edited),both_pass=len(both),
                original_only=sum(a['success'] and not b['success'] for a,b in pairs),
                edited_only=sum(b['success'] and not a['success'] for a,b in pairs),
                both_fail=sum(not a['success'] and not b['success'] for a,b in pairs),
                median_original_s_joint_success=median(a['elapsed_s'] for a,b in both) if both else None,
                median_edited_s_joint_success=median(b['elapsed_s'] for a,b in both) if both else None)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('directory',type=Path)
    ap.add_argument('output',type=Path)
    args=ap.parse_args()
    rows={}
    pairs=[]
    for task in TASKS:
        items=[]
        for seed in SEEDS:
            a,b=[json.loads((args.directory/f'{task}-{seed}-{v}.json').read_text()) for v in ('original','edited')]
            if a['goal']!=b['goal']:
                raise ValueError(f'Paired goals differ: {task} {seed}')
            items.append((a,b))
        rows[task]=summarize(items)
        pairs.extend(items)
    report=dict(suite='BrowserGym MiniWoB++',browser='Brave',seeds=SEEDS,
        tasks=rows,aggregate=summarize(pairs),reset_goals_identical=True,
        starts_with_identical_rendered_dom=sum(a['steps'][0]['observation']==b['steps'][0]['observation'] for a,b in pairs),
        elapsed='After environment reset through native reward or stop; warm checkpoints. Latency medians use only identical seeds both models solved.',
        settings=dict(browsergym_core='0.14.3',browsergym_miniwob='0.14.3',miniwob_revision='7fd85d71a4b60325c6585396ec4f48377d049838',max_decisions=16,reasoning_effort='none',sampling='greedy',max_generated_per_decision=384,observation='Rendered DOM with BrowserGym IDs and prior actions; no screenshots passed to the model.',actions='One BrowserGym click or fill per decision. Identical state/action repetition or malformed action ends the episode with zero credit.'))
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['aggregate']))

if __name__=='__main__':
    main()
