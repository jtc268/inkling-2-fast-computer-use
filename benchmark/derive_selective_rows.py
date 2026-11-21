"""Reproduce the experimental rows from the original model and development screens."""
import argparse
import ast
import json
from pathlib import Path
import mlx.core as mx
from mlx_lm import load
import numpy as np

HERE=Path(__file__).resolve().parent
CHANNELS=(200004,200008)

def bf16_bits(values):
    bits=np.asarray(values,dtype='<f4').view('<u4')
    return ((bits+0x7fff+((bits>>16)&1))>>16).astype('<u2')

def derive(base,prompts):
    model,tokenizer=load(str(base),trust_remote_code=True)
    system=next(n.value for n in ast.walk(ast.parse((HERE/'model.py').read_text()))
                if isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value.startswith('Operate the browser using'))
    rows=[np.asarray(model.lm_head.weight[i].astype(mx.float32)).astype(np.float64) for i in CHANNELS]
    activations=[]
    for sample in prompts:
        msgs=[{'role':'system','content':system},{'role':'user','content':sample['prompt']}]
        text=tokenizer.apply_chat_template(msgs,tokenize=False,reasoning_effort='none')
        ids=tokenizer.encode(text,add_special_tokens=False)+[200001]
        h=model.model.language_model(mx.array([ids]))[0,-1,:]
        activations.append(np.asarray(h.astype(mx.float32)).astype(np.float64))
    states=np.stack(activations)
    protected=states[[s['group']=='protect' for s in prompts]]
    direct=states[[s['group']=='direct' for s in prompts]]
    basis,_=np.linalg.qr(protected.T,mode='reduced')
    residual=direct-(direct@basis)@basis.T
    # Put the displacement in the nullspace of the protected activations.
    # On the direct activations, exchange the pre-softcap channel scores.
    target=direct@(rows[1]-rows[0])
    coefficients=np.linalg.lstsq(residual@residual.T,target,rcond=1e-10)[0]
    delta=residual.T@coefficients
    if np.max(np.abs(protected@delta))>1e-6 or np.max(np.abs(direct@delta-target))>1e-5:
        raise ValueError('Channel-score constraints failed')
    return np.concatenate([bf16_bits(rows[0]+delta),bf16_bits(rows[1]-delta)])

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('base',type=Path)
    ap.add_argument('output',type=Path)
    args=ap.parse_args()
    prompts=json.loads((HERE.parent/'evidence/calibration-prompts.json').read_text())
    weights=derive(args.base,prompts)
    with args.output.open('xb') as f:
        f.write(weights.tobytes())
