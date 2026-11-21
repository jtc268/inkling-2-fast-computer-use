"""Evaluate two checkpoints on five seeded BrowserGym environments in Brave."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

import browsergym.miniwob
from browsergym.core.action.highlevel import HighLevelActionSet
import gymnasium as gym

TASKS = ('email-inbox','use-autocomplete','social-media-all','choose-date','book-flight')
SEEDS = (101,102,103,104)
MAX_DECISIONS = 16
HERE = Path(__file__).resolve().parent
BRAVE = os.environ.get('BRAVE_PATH', '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser')
SENSE = r"""() => {
 const lines=[];
 function walk(el,depth) {
   if(!el.getClientRects().length || getComputedStyle(el).visibility==='hidden') return;
   const tag=el.tagName.toLowerCase(), bid=el.getAttribute('bid');
   let own=Array.from(el.childNodes).filter(n=>n.nodeType===3).map(n=>n.textContent).join(' ').replace(/\s+/g,' ').trim();
   const attrs=['id','class','title','aria-label','placeholder','type','readonly','alt','role'].filter(k=>el.hasAttribute(k)).map(k=>el.getAttribute(k)||k);
   if (el.matches('input,textarea,select')) attrs.push('value='+el.value);
   if (el.matches('input[type=checkbox],input[type=radio]')) attrs.push(el.checked?'checked':'unchecked');
   if (bid && (own || attrs.length || el.matches('button,a,textarea,select,input'))) {
     lines.push(' '.repeat(Math.min(depth,8))+'['+bid+'] '+tag+' '+attrs.join(' ')+' '+own);
   }
   for (const c of el.children) walk(c,depth+1);
 }
 walk(document.body,0);
 return lines.join('\n');
}"""
TOOL = re.compile(r'^([FC])\s+(\d+)(?:\s+(.+))?$')
def inference_proc(path):
    python=os.environ['INKLING_MLX_PYTHON']
    p=subprocess.Popen([python,str(HERE/'model.py'),path],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True,env={**os.environ,'HF_HUB_OFFLINE':'1'})
    if p.stdout.readline().strip()!='READY':
        raise RuntimeError('Could not warm model')
    return p

def evaluate(task,seed,arm,worker,out):
    env=gym.make('browsergym/miniwob.'+task,headless=True,pw_chromium_kwargs={'executable_path':BRAVE},action_mapping=HighLevelActionSet(subsets=['bid'],multiaction=False).to_python_code)
    try:
        obs,_=env.reset(seed=seed)
        page=env.unwrapped.page
        log=dict(environment=task,seed=seed,arm=arm,goal=obs['goal'],steps=[],success=False,reason='decision limit')
        start=time.perf_counter()
        seen=set()
        history=[]
        for number in range(MAX_DECISIONS):
            view=page.evaluate(SENSE)
            prompt=(f"Goal: {obs['goal']}\nChoose exactly one next browser action, then wait for the updated page. "
                    "Use C <id> to click, or F <id> <value> to fill a writable text field. Readonly fields open by clicking. "
                    "IDs are in brackets. The indented rows show the rendered DOM, including elements below the scroll position.\n"
                    f"Previous actions: {history}\nCurrent page:\n{view}")
            worker.stdin.write(json.dumps({'prompt':prompt})+'\n')
            worker.stdin.flush()
            ans=json.loads(worker.stdout.readline())
            final=ans['final'].strip()
            key=(view,final)
            step=dict(observation=view,action=final,generated=ans['generated'],thinking=ans['thinking'],inference_s=ans['seconds'])
            log['steps'].append(step)
            match=TOOL.fullmatch(final)
            if match is None:
                log['reason']='invalid action format'
                break
            if key in seen:
                log['reason']='repeated same state and action'
                break
            seen.add(key)
            op,bid,value=match.groups()
            if f'[{bid}] ' not in view or (op=='C')!=(value is None):
                log['reason']='invalid visible ID or arguments'
                break
            action=f'click({bid!r})' if op=='C' else f'fill({bid!r},{value!r},True)'
            obs,reward,terminated,truncated,info=env.step(action)
            err=obs.get('last_action_error','')
            if err:
                step['error']=err.split('\n')[0][:250]
            history.append(final+(' [action failed]' if err else ''))
            if terminated or truncated:
                log.update(success=bool(reward>0),reward=float(reward),reason='native grader' if terminated else 'truncated')
                break
        log['elapsed_s']=time.perf_counter()-start
        (out/f'{task}-{seed}-{arm}.json').write_text(json.dumps(log,indent=2)+'\n')
        print(task,seed,arm,log['success'],len(log['steps']),round(log['elapsed_s'],2),log['reason'],flush=True)
    finally:
        env.close()

def main():
    out=Path(os.environ.get('INKLING_GYM_OUTPUT','gym-runs'))
    out.mkdir(parents=True,exist_ok=True)
    workers={}
    try:
        for arm in ('original','edited'):
            workers[arm]=inference_proc(os.environ['INKLING_'+arm.upper()])
        for i,seed in enumerate(SEEDS):
            for j,task in enumerate(TASKS):
                order=('original','edited') if (i+j)%2==0 else ('edited','original')
                for arm in order:
                    if not (out/f'{task}-{seed}-{arm}.json').exists():
                        evaluate(task,seed,arm,workers[arm],out)
    finally:
        for p in workers.values():
            p.stdin.close()
            p.wait()

if __name__=='__main__':
    main()
