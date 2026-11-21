"""Check every full-task speed ratio and token count against the published episode timings."""
import argparse
import json
import math
from pathlib import Path
from zipfile import ZipFile


def verify(archive_path, pairs_path):
    pairs=json.loads(pairs_path.read_text())['pairs']
    with ZipFile(archive_path) as archive:
        names=[n for n in archive.namelist() if n.startswith('timing/')]
        episodes={}
        for name in names:
            event=json.loads(archive.read(name))
            grade=json.loads(archive.read(name.replace('timing/','receipts/',1)))
            assert event['seconds']==grade['elapsed_s'] and event['score']==grade['score']
            times=[s['start_s'] for s in event['steps']]+[event['seconds']]
            assert all(math.isfinite(t) and t>=0 for t in times)
            for start,end,s in zip(times,times[1:],event['steps']):
                assert 0<=s['inference_s']<=end-start+1e-6 and 0<=s['thinking']<=s['generated']
            digest=event['receipt_sha256']
            assert digest not in episodes or episodes[digest]==event
            episodes[digest]=event
        used=set()
        for p in pairs:
            original,edited=(episodes[p[a]['receipt_sha256']] for a in ('original','edited'))
            assert original['steps'][0]['view_sha256']==edited['steps'][0]['view_sha256']
            for arm,event in [('original',original),('edited',edited)]:
                result=p[arm]
                assert (p['task'],arm,result['seconds'],result['score'],result['shard_sha256'])==(event['task'],event['arm'],event['seconds'],event['score'],event['shard_sha256'])
                assert [s['action'] for s in event['steps']]==result['commands']
                assert sum(s['generated'] for s in event['steps'])==result['generated']
                assert sum(s['thinking'] for s in event['steps'])==result['thinking']
                assert math.isclose(sum(s['inference_s'] for s in event['steps']),result['inference_seconds'],rel_tol=1e-12)
                used.add(event['receipt_sha256'])
            if p['comparable'] and original['score']==edited['score']==1:
                assert math.isclose(original['seconds']/edited['seconds'],p['ratio'],rel_tol=1e-12)
            else:
                assert p['ratio'] is None
        assert used==set(episodes) and len(names)==2*len(pairs)
    return len(pairs),len(names)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive',type=Path)
    parser.add_argument('pairs',type=Path)
    args=parser.parse_args()
    count,total=verify(args.archive,args.pairs)
    print(f'Verified {count} paired comparisons against {total} recorded episode timings.')
