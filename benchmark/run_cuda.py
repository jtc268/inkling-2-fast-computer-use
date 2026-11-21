"""Run one arm on a user-supplied local SGLang instance and the standard fixtures."""
import argparse
import json
from pathlib import Path
from urllib.request import urlopen
from webarena import BRAVE, PANEL, SYSTEM, URL, WebArenaVerified, WebArenaVerifiedConfig, episode, sync_playwright
from cuda_worker import CudaWorker

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--endpoint',required=True,help='SGLang origin, for example http://127.0.0.1:30000')
    ap.add_argument('--model-name',required=True,help='Expected model ID served by the endpoint')
    ap.add_argument('--tokenizer',type=Path,required=True)
    ap.add_argument('--arm',choices=('original','selective'),required=True)
    ap.add_argument('--indices',choices=('even','odd','all'),default='all')
    ap.add_argument('--task',type=int,action='append',help='Run only these official task IDs, repeatable')
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    with urlopen(args.endpoint.rstrip('/')+'/v1/models',timeout=5) as resp:
        available={m['id'] for m in json.load(resp)['data']}
    if args.model_name not in available:raise ValueError('The endpoint is serving a different checkpoint')
    known={t['id'] for t in PANEL['tasks']}
    if args.task and not set(args.task)<=known:raise ValueError('Task is outside the frozen panel')
    args.out.mkdir(parents=True,exist_ok=True)
    worker=CudaWorker(args.endpoint,args.tokenizer,{'device':'CUDA','engine':'SGLang','model_id':args.model_name})
    worker.decide_web('Click Go. Controls: 7 button Go.',SYSTEM)
    native=WebArenaVerified(config=WebArenaVerifiedConfig(environments={s:{'urls':[u]} for s,u in URL.items()}))
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path=BRAVE,headless=True)
        try:
            for i,t in enumerate(PANEL['tasks']):
                if args.task and t['id'] not in args.task:continue
                if args.indices!='all' and (i%2==0)!=(args.indices=='even'):continue
                if (args.out/f"{t['id']:03d}-{args.arm}.json").is_file():continue
                episode(browser,worker,native,t,args.arm,args.out)
        finally:browser.close()
