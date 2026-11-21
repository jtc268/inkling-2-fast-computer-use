"""Measure a two-page model-driven browser task on an empty, disposable Brave cart."""
import argparse
import contextlib
import json
import os
from pathlib import Path
import random
import re
import sys
from datetime import datetime
import subprocess
import time
from urllib.parse import urlsplit, parse_qs

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
from huggingface_hub import snapshot_download

REPOSITORIES = {
    'original': ('thinkingmachines/Inkling-2-Mini', 'ed40e7da625f594fc9c4990f5f66be24873c22d7'),
    'edited': ('husky8/Inkling-2-Fast-Computer-Use', 'd4562716ff6d8d0281bf09814a1df0db570f6be3'),
}
MLX = sys.executable
BRAVE = os.environ.get('BRAVE_PATH', '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser')

def checkpoint(variant):
    local = os.environ.get('INKLING_' + variant.upper())
    if local:
        return local
    repo, revision = REPOSITORIES[variant]
    return snapshot_download(repo, revision=revision, allow_patterns=[
        'model*.safetensors', '*.json', 'chat_template.jinja',
    ])

FORM = 'https://www.selenium.dev/selenium/web/web-form.html'
SIZE = {'width':1024,'height':680}
CASES = [
 ('dev','Robin West','Use the side entrance',1,2),
 ('01','Maya Chen','Leave by the blue door',1,3),
 ('02','Alex Lane','Use the front entrance',2,4),
 ('03','Nora Reed','Ring the doorbell',3,2),
 ('04','Sam Park','Use the parcel shelf',4,3),
 ('05','Luca West','Leave at reception',5,4),
 ('06','Jules Gray','Knock twice',6,2),
]
BOOT = (HERE/'motion.js').read_text()+'''
window.attachPointer=()=>{
 if(window.demoPointer)return;
 const canvas=document.createElement('canvas');
 Object.assign(canvas.style,{position:'fixed',inset:'0',width:'100vw',height:'100vh',pointerEvents:'none',zIndex:'2147483646'});
 canvas.setAttribute('aria-hidden','true');document.documentElement.appendChild(canvas);
 window.demoPointer=new CuaMotion.MotionPlayer(canvas,{float:false});
 demoPointer.place({x:innerWidth*.53,y:innerHeight*.5});
};
'''
def write_json(path, obj):
    tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(obj,indent=2));tmp.replace(path)
class Planner:
    def __init__(self,variant):
        self.variant=variant
        self.proc=subprocess.Popen([MLX,str(HERE/'model.py'),checkpoint(variant)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True,env={**os.environ,'HF_HUB_OFFLINE':'1'})
        if self.proc.stdout.readline().strip()!='READY':raise RuntimeError('Failed to initialize checkpoint')
    def decide(self,prompt):
        self.proc.stdin.write(json.dumps({'prompt':prompt})+'\n');self.proc.stdin.flush()
        res=json.loads(self.proc.stdout.readline());assert 'final' in res,res
        return res
    def close(self):
        self.proc.stdin.close();self.proc.wait(timeout=30)

def controls(page,region,seed):
    els=page.locator(region).locator('input:enabled:not([type=hidden]):not([readonly]), textarea:enabled, select:enabled, button:enabled')
    locs={};lines=[]
    rng=random.Random(seed);ids=rng.sample(range(10,90),min(80,els.count()))
    for i,num in enumerate(ids):
        el=els.nth(i)
        if not el.is_visible():continue
        name,typ=el.evaluate("""n=>[(n.labels?.[0]?.innerText||n.getAttribute('aria-label')||n.innerText||n.placeholder||n.name||'').trim().split('\\n')[0],n.tagName=='INPUT'?n.type:n.tagName.toLowerCase()]""")
        locs[num]=(el,typ);lines.append(f'{num} {typ} {name}')
    return locs,'\n'.join(lines)
def tap(page,el):
    el.scroll_into_view_if_needed(timeout=2500)
    box=el.bounding_box(); assert box
    x=box['x']+box['width']/2;y=box['y']+box['height']/2
    page.evaluate("""async a=>{attachPointer();await demoPointer.moveTo({x:a[0],y:a[1]},{params:{style:'signature_arc',timing:'fixed',glideDurationMs:360},target:a[2],click:true});}""",[x,y,[box['x'],box['y'],box['width'],box['height']]])
    assert el.evaluate('(n,p)=>n.contains(document.elementFromPoint(...p))',[x,y]), 'control is occluded'
    page.mouse.click(x,y)
def execute(page,locs,response):
    actions=[]
    for line in response.splitlines():
        if not line.strip():continue
        match=re.fullmatch(r'\s*([FC])\s+(\d+)(?:\s+(.+))?\s*',line)
        if not match:raise ValueError('Invalid action: '+line[:120])
        op,idx,val=match.groups()
        el,typ=locs[int(idx)]
        if op=='C' and (typ!='button' or val is not None):raise ValueError('Unexpected click')
        if op=='F' and (typ not in ('text','textarea','number') or val is None):raise ValueError('Unexpected field')
        actions.append((op,el,val))
    if not actions or len(actions)>7:raise ValueError('Unexpected batch size')
    for op,el,val in actions:
        tap(page,el)
        if op=='F':
            el.press('ControlOrMeta+a');page.keyboard.type(val,delay=25)
def mark(page,color):
    # Optical timecode for frame alignment. The export crops these eight rows.
    page.evaluate("""color=>{const m=document.createElement('div');Object.assign(m.style,{position:'fixed',left:0,top:0,width:'24px',height:'8px',zIndex:2147483647,pointerEvents:'none',background:color});document.documentElement.append(m)}""",color)

def run(pw,browser,planner,case,variant,folder):
    case_id,name,note,pid,qty=case
    record={'case':case_id,'variant':variant,'product_id':pid,'quantity':qty,'name':name,'note':note,'success':False,'plans':[]}
    ctx=browser.new_context(viewport=SIZE,device_scale_factor=1,locale='en-US')
    page=ctx.new_page();page.set_default_timeout(6000)
    page.add_init_script(script=BOOT)
    path=folder/f'{case_id}-{variant}.webm'
    recording=False;t0=None
    try:
        page.goto(FORM,wait_until='load',timeout=20000)
        page.evaluate('attachPointer()')
        page.screencast.start(path=path,fps=25,size=SIZE);recording=True
        t0=time.perf_counter()
        mark(page,'#13f084')
        for stage in ('form','shop'):
            seed=f'{case_id}-{stage}'
            if stage=='form':
                locs,obs=controls(page,'main form',seed)
                job=f'Fill Text input with "{name}" and Textarea with "{note}", then submit this form. Enter the values without quotes.'
            else:
                page.goto(f'https://automationexercise.com/product_details/{pid}',wait_until='domcontentloaded',timeout=15000)
                title=page.locator('.product-information h2').inner_text();record['product']=title
                locs,obs=controls(page,'section .product-details',seed)
                job=f'On the product page for {title}, set Quantity to {qty}, then add it to cart.'
            prompt=f'{job}\nVisible controls:\n{obs}'
            ans=planner.decide(prompt)
            record['plans'].append(dict(stage=stage,observation=obs,**ans))
            execute(page,locs,ans['final'])
            if stage=='form':
                page.wait_for_url('**/submitted-form.html?**',wait_until='domcontentloaded')
                val=parse_qs(urlsplit(page.url).query)
                assert val.get('my-text')==[name] and val.get('my-textarea')==[note],'wrong form fields'
                assert page.get_by_text('Received!',exact=True).is_visible()
                record['form_s']=time.perf_counter()-t0
        modal=page.locator('#cartModal.show')
        modal.wait_for()
        tap(page,modal.get_by_text('View Cart',exact=True))
        row=page.locator(f'#product-{pid}')
        row.wait_for()
        assert page.locator('#cart_info_table tbody tr').count()==1
        actual_qty=int(row.locator('.cart_quantity').inner_text().strip())
        actual_title=row.locator('.cart_description h4').inner_text().strip()
        assert (actual_title,actual_qty)==(title,qty),(actual_title,actual_qty)
        record.update(success=True,actual_quantity=actual_qty,actual_product=actual_title,elapsed_s=time.perf_counter()-t0)
        mark(page,'#fc18af')
        page.wait_for_timeout(550)
    except Exception as exc:
        record['error']=str(exc)[:550];record['elapsed_s']=time.perf_counter()-t0 if t0 else None
        with contextlib.suppress(Exception):page.screenshot(path=str(folder/f'{case_id}-{variant}-error.png'))
    finally:
        if recording:page.screencast.stop()
        ctx.close()
        write_json(folder/f'{case_id}-{variant}.json',record)
    print(case_id,variant,record['success'],record.get('elapsed_s'),record.get('error',''),[(p['stage'],p['final'][:95]) for p in record['plans']],flush=True)
    return record

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--mode',choices=['dev','test'],default='dev');a.add_argument('--arm',choices=['edited','original','both'],default='edited');args=a.parse_args()
    folder=Path('runs')/datetime.now().strftime('%Y%m%d-%H%M%S-%f');folder.mkdir(parents=True);print(f'Recordings and results: {folder}', flush=True)
    if not Path(BRAVE).is_file(): raise SystemExit('Install Brave or set BRAVE_PATH to its executable.')
    results=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(executable_path=BRAVE,headless=True)
        plans={}
        try:
            if args.mode=='test' and args.arm=='both':
                for label in ('original','edited'):plans[label]=Planner(label)
            for i,case in enumerate(CASES[:1] if args.mode!='test' else CASES[1:]):
                order=['original','edited'] if i%2==0 else ['edited','original']
                if args.arm!='both':order=[args.arm]
                for variant in order:
                    if variant not in plans:plans[variant]=Planner(variant)
                    results.append(run(pw,b,plans[variant],case,variant,folder))
        finally:
            for proc in plans.values():proc.close()
            b.close()

    if not all(r['success'] for r in results): sys.exit(1)
