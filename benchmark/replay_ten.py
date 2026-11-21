"""Verify all 70 WebArena grades and each same-device pair from the released evidence."""
import argparse
import json
from pathlib import Path
from zipfile import ZipFile
from score_webarena import grader


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    args = parser.parse_args()
    panel = Path(__file__).resolve().parents[1] / 'evidence/webarena-ten-panel.json'
    ids = [task['id'] for task in json.loads(panel.read_text())['tasks']]
    pairs = {}
    graders = {}
    with ZipFile(args.archive) as archive:
        expected = []
        for task in ids:
            for rep in (1, 2, 3):
                for arm in ('original', 'candidate'):
                    expected.append(f'primary/r{rep}/{task:03d}-{arm}.json')
            expected.append(f'replica/r1/{task:03d}-original.json')
        if sorted(expected) != sorted(n.removeprefix('receipts/') for n in archive.namelist() if n.startswith('receipts/')):
            raise ValueError('Unexpected receipt inventory.')
        for name in expected:
            rec = json.loads(archive.read('receipts/' + name))
            events = json.loads(archive.read('network/' + name))
            group, rep, filename = name.split('/')
            if filename != f"{rec['id']:03d}-{rec['arm']}.json":
                raise ValueError(f'Unexpected identity in {name}.')
            site = (rec['site'], rec['fixture_origin'])
            if site not in graders:
                graders[site] = grader(rec)
            result = graders[site].evaluate_task(task_id=rec['id'], agent_response=rec['answer'], network_trace=events)
            if (result.score, str(result.status), result.error_msg) != (rec['score'], rec['grade'], None):
                raise ValueError(f'Grade mismatch for {name}.')
            if group == 'primary':
                pairs.setdefault((rep, rec['id']), set()).add(rec['hardware']['gpu_uuid'])
    if any(len(devices) != 1 for devices in pairs.values()):
        raise ValueError('A pair used different physical GPUs.')
    print('Reproduced 60 primary grades and 10 third-card grades. All 30 timing pairs used the same physical GPU.')


if __name__ == '__main__':
    main()
