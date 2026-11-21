"""Replay each search or form-and-cart analogue trace with WebArena-Verified."""
import argparse
import json
from zipfile import ZipFile

from webarena_verified.api import WebArenaVerified
from webarena_verified.types.config import WebArenaVerifiedConfig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive')
    args = parser.parse_args()
    graders = {}
    with ZipFile(args.archive) as archive:
        receipts = sorted(name for name in archive.namelist() if name.startswith('receipts/'))
        if not receipts:
            raise ValueError('No receipts in archive')
        for name in receipts:
            receipt = json.loads(archive.read(name))
            trace = json.loads(archive.read(name.replace('receipts/', 'network/', 1)))
            site = receipt['site']
            origin = receipt['fixture_origin']
            if (site, origin) not in graders:
                config = WebArenaVerifiedConfig(environments={site: {'urls': [origin]}})
                graders[site, origin] = WebArenaVerified(config=config)
            result = graders[site, origin].evaluate_task(
                task_id=receipt['id'], agent_response=receipt['answer'], network_trace=trace
            )
            if (result.score, str(result.status), result.error_msg) != (receipt['score'], receipt['grade'], None):
                raise ValueError(f'Grade mismatch in {name}')
            print(f'{name}: {result.score:g}')
    print(f'{len(receipts)} recorded grades reproduced.')


if __name__ == '__main__':
    main()
