"""Replay the sanitized network records with the official offline grader."""
import argparse
import json
from pathlib import Path
import zipfile

from webarena_verified.api import WebArenaVerified
from webarena_verified.types.config import WebArenaVerifiedConfig

def grader(receipt=None):
    if receipt and receipt.get('fixture_origin'):
        return WebArenaVerified(config=WebArenaVerifiedConfig(environments={receipt['site']:{'urls':[receipt['fixture_origin']]}}))
    return WebArenaVerified(config=WebArenaVerifiedConfig(environments={
        'shopping': {'urls':['http://127.0.0.1:7770']},
        'reddit': {'urls':['http://127.0.0.1:9999']}}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive',type=Path)
    args=parser.parse_args()
    wa=grader()
    with zipfile.ZipFile(args.archive) as z:
        names=sorted(n for n in z.namelist() if n.startswith('receipts/'))
        totals={'original':0,'selective':0}
        for name in names:
            rec=json.loads(z.read(name))
            events=json.loads(z.read(name.replace('receipts/','network/')))
            result=grader(rec).evaluate_task(task_id=rec['id'],agent_response=rec['answer'],network_trace=events)
            if result.score!=rec['score'] or str(result.status)!=rec['grade']:
                raise ValueError(f'Grade disagrees for {name}')
            totals[rec['arm']]+=int(result.score==1)
        if len(names)!=40:raise ValueError('Expected two runs for each of twenty tasks')
        print(f"{len(names)} official grades reproduced. Upstream {totals['original']}/20, selective {totals['selective']}/20.")
