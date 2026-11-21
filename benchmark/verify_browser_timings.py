"""Check every full-task speed ratio and token count against the published episode timings."""
import argparse
import json
import math
from pathlib import Path
from zipfile import ZipFile


def verify(archive_path, pairs_path):
    def check(condition, message):
        if not condition:
            raise ValueError(message)

    pairs=json.loads(pairs_path.read_text())['pairs']
    with ZipFile(archive_path) as archive:
        names=[n for n in archive.namelist() if n.startswith('timing/')]
        episodes={}
        for name in names:
            event=json.loads(archive.read(name))
            grade=json.loads(archive.read(name.replace('timing/','receipts/',1)))
            check(event['seconds']==grade['elapsed_s'] and event['score']==grade['score'],f'{name}: grade and timing disagree')
            times=[s['start_s'] for s in event['steps']]+[event['seconds']]
            check(bool(event['steps']) and all(math.isfinite(t) and t>=0 for t in times),f'{name}: invalid timestamps')
            for start,end,s in zip(times,times[1:],event['steps']):
                check(0<=s['inference_s']<=end-start+1e-6 and 0<=s['thinking']<=s['generated'],f'{name}: invalid step duration or token count')
            digest=event['receipt_sha256']
            check(digest not in episodes or episodes[digest]==event,f'{name}: conflicting episode identity')
            episodes[digest]=event
        used=set()
        for p in pairs:
            original,edited=(episodes[p[a]['receipt_sha256']] for a in ('original','edited'))
            label=f"WebArena {p['task']}, {p['checkpoint']}, repeat {p['repeat']}"
            check(original['steps'][0]['view_sha256']==edited['steps'][0]['view_sha256'],f'{label}: different initial observations')
            for arm,event in [('original',original),('edited',edited)]:
                result=p[arm]
                check((p['task'],arm,result['seconds'],result['score'],result['shard_sha256'])==(event['task'],event['arm'],event['seconds'],event['score'],event['shard_sha256']),f'{label}: wrong {arm} episode')
                check([s['action'] for s in event['steps']]==result['commands'],f'{label}: different {arm} actions')
                check(sum(s['generated'] for s in event['steps'])==result['generated'],f'{label}: different {arm} token count')
                check(sum(s['thinking'] for s in event['steps'])==result['thinking'],f'{label}: different {arm} reasoning token count')
                check(math.isclose(sum(s['inference_s'] for s in event['steps']),result['inference_seconds'],rel_tol=1e-12),f'{label}: different {arm} inference time')
                used.add(event['receipt_sha256'])
            if p['comparable'] and original['score']==edited['score']==1:
                check(edited['seconds']>0 and isinstance(p['ratio'],(int,float)) and math.isclose(original['seconds']/edited['seconds'],p['ratio'],rel_tol=1e-12),f'{label}: speed ratio disagrees with the clock')
            else:
                check(p['ratio'] is None,f'{label}: speed ratio on an unsuccessful or incomparable pair')
        check(bool(pairs) and used==set(episodes) and len(names)==2*len(pairs),'Incomplete timing archive')
    return len(pairs),len(names)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive',type=Path)
    parser.add_argument('pairs',type=Path)
    args=parser.parse_args()
    count,total=verify(args.archive,args.pairs)
    print(f'Verified {count} paired comparisons against {total} recorded episode timings.')
