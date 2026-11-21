"""Compare the two published shards and verify the exact output-row swap."""
import argparse
import hashlib
import json
from pathlib import Path
import struct

SHARD = 'model-00001-of-00001.safetensors'

def verify(original, edited, spec):
    size = original.stat().st_size
    if size != edited.stat().st_size:
        raise ValueError('Shard sizes differ')
    with original.open('rb') as before, edited.open('rb') as after:
        header_length, = struct.unpack('<Q', before.read(8))
        tensor = json.loads(before.read(header_length))[spec['tensor']]
        if tensor['dtype'] != 'BF16' or tensor['shape'] != [201024, 2304]:
            raise ValueError('Unexpected output tensor')
        before.seek(0)
        row_bytes = tensor['shape'][1] * 2
        offsets = [8 + header_length + tensor['data_offsets'][0] + i*row_bytes for i in spec['rows']]
        original_rows, edited_rows = [], []
        base_hash, edit_hash = hashlib.sha256(), hashlib.sha256()
        for offset in [*offsets, size]:
            while before.tell() < offset:
                left = before.read(min(16*1024*1024, offset-before.tell()))
                right = after.read(len(left))
                if left != right:
                    raise ValueError('Bytes outside the two rows differ')
                base_hash.update(left)
                edit_hash.update(right)
            if offset != size:
                left, right = before.read(row_bytes), after.read(row_bytes)
                original_rows.append(left)
                edited_rows.append(right)
                base_hash.update(left)
                edit_hash.update(right)
        if edited_rows != original_rows[::-1]:
            raise ValueError('Rows are not an exact swap')
        if (base_hash.hexdigest(), edit_hash.hexdigest()) != (spec['base_sha256'], spec['edited_sha256']):
            raise ValueError('Files differ from the measured checkpoints')
        changed = sum(a != b for left,right in zip(original_rows,edited_rows)
                      for a,b in zip(struct.iter_unpack('<H',left),struct.iter_unpack('<H',right)))
        return changed

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original',type=Path,help='Original checkpoint directory')
    parser.add_argument('edited',type=Path,help='Edited checkpoint directory')
    args=parser.parse_args()
    spec=json.loads((Path(__file__).resolve().parents[1]/'evidence/weight-edit.json').read_text())
    values=verify(args.original/SHARD,args.edited/SHARD,spec)
    print(f'{values:,} BF16 values changed. Both SHA-256 digests match. Every byte outside the two rows is identical.')
