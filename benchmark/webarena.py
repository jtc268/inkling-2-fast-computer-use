"""Run a frozen WebArena-Verified panel with a fresh fixture per episode."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from playwright.sync_api import sync_playwright, Error as BrowserError
from webarena_verified.api import WebArenaVerified
from webarena_verified.types.config import WebArenaVerifiedConfig
from run import BOOT, BRAVE, Planner, tap, write_json

HERE = Path(__file__).resolve().parent
PANEL = json.loads((HERE.parent / 'evidence/webarena-panel.json').read_text())
PORTS = {'shopping': 7770, 'reddit': 9999}
FIXTURES = {'shopping': 'shop', 'reddit': 'forum'}
FIXTURE_IMAGES = {
    'reddit': 'am1n3e/webarena-verified-reddit@sha256:0594908059a03e5f610005689440a95c05e776e734006197c7b1eba12734cb46',
    'shopping': 'am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb',
}
# Synthetic benchmark accounts shipped with these two fixtures.
AUTH = {'shopping': ('X-M2-Customer-Auto-Login', 'emma.lopez@gmail.com:Password.123'),
        'reddit': ('X-Postmill-Auto-Login', 'MarvelsGrantMan136:test1234')}
URL = {site: f'http://127.0.0.1:{port}' for site, port in PORTS.items()}
SYSTEM = """Operate this browser to finish the user's task. Return one action per decision.
C id clicks a link or button. H id hovers a menu. F id text fills a field. K Enter submits the focused field. S id label selects an option. D or U scrolls one screen. B goes back. T number switches to a listed tab.
When you have reached the requested page, return DONE navigate. After successfully changing something, return DONE mutate. To answer a question, return ANSWER followed by a JSON array of the requested values. If you cannot finish, return STOP. Use only listed controls and the user's task. No commentary."""
VIEW = r"""() => {
 const clean = s => (s||'').replace(/\s+/g,' ').trim();
 const visible = e => {const r=e.getBoundingClientRect(), s=getComputedStyle(e); return r.width>0 && r.height>0 && s.visibility!=='hidden' && s.display!=='none';};
 const inView = e => {const r=e.getBoundingClientRect();return r.bottom>0&&r.top<innerHeight&&r.right>0&&r.left<innerWidth;};
 document.querySelectorAll('[data-ink-id]').forEach(e=>e.removeAttribute('data-ink-id'));
 const nodes=[...document.querySelectorAll('a[href],input:not([type=hidden]),textarea,button,select,[role=button],[role=menuitem],summary')].filter(e=>visible(e)&&inView(e)&&!e.disabled);
 let controls=[];
 for(const e of nodes){
   let label=clean(e.getAttribute('aria-label') || e.getAttribute('title') || e.labels?.[0]?.innerText || e.innerText || e.placeholder || e.alt || e.querySelector('img')?.alt || e.name || e.value);
   if(!label) continue;
   const id=controls.length+1; e.setAttribute('data-ink-id',id);
   if(e.tagName==='SELECT')label+=' ['+[...e.options].map(o=>clean(o.text)).join('|')+']';
   controls.push(id+' '+(e.type||e.tagName.toLowerCase())+' '+label.slice(0,110));
   if(controls.length>=68)break;
 }
 const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
 let text=[],length=0,n;
 while((n=walker.nextNode()) && length<1800){
   const el=n.parentElement,s=clean(n.textContent);
   if(!s||!el||['SCRIPT','STYLE','NOSCRIPT'].includes(el.tagName)||!visible(el)||!inView(el))continue;
   const range=document.createRange(); range.selectNodeContents(n);const r=range.getBoundingClientRect();
   if(!r.width||r.bottom<=0||r.top>=innerHeight)continue;
   text.push(s);length+=s.length+3;
 }
 return 'Text: '+text.join(' | ').slice(0,1800)+'\nControls:\n'+controls.join('\n');
}"""

def fresh(site):
    """Only replace a container carrying this experiment's unique owner label."""
    name = 'inkling-wa-' + FIXTURES[site]
    found = subprocess.run(['docker','inspect','--format','{{index .Config.Labels "inkling.experiment"}}',name],capture_output=True,text=True)
    if found.returncode == 0:
        if found.stdout.strip() != 'webarena':
            raise RuntimeError('Fixture name belongs to another process')
        subprocess.run(['docker','rm','-f',name],check=True,stdout=subprocess.DEVNULL)
    port = PORTS[site]
    ctrl = 7771 if site == 'shopping' else 9998
    image = FIXTURE_IMAGES[site]
    subprocess.run(['docker','run','-d','--rm','--platform','linux/amd64','--name',name,
                    '--label','inkling.experiment=webarena','-p',f'127.0.0.1:{port}:80',
                    '-p',f'127.0.0.1:{ctrl}:8877','-e',f'WA_ENV_CTRL_EXTERNAL_SITE_URL={URL[site]}',image],
                   check=True,stdout=subprocess.DEVNULL)
    start=time.monotonic()
    healthy_path='/customer/account/' if site=='shopping' else '/'
    marker=b'Account Information' if site=='shopping' else b'MarvelsGrantMan136'
    while time.monotonic()-start < 250:
        try:
            with urlopen(Request(URL[site]+healthy_path,headers=dict([AUTH[site]])),timeout=18) as resp:
                if resp.status==200 and urlsplit(resp.url).netloc==urlsplit(URL[site]).netloc and marker in resp.read():
                    if site=='shopping':
                        check=subprocess.run(['docker','exec',name,'curl','-fsS','--max-time','8',
                            'http://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=5s'],
                            capture_output=True,text=True)
                        if check.returncode or json.loads(check.stdout).get('status') not in ('yellow','green'):
                            time.sleep(2)
                            continue
                    return
        except (OSError, ValueError):
            pass
        time.sleep(2)
    raise RuntimeError(f'{site} fixture did not pass signed-in health check')

def perform(page,ctx,line):
    op,*args=line.split(' ',2)
    if op=='STOP' and not args: return page,'stopped',None
    if op=='DONE' and len(args)==1 and args[0].lower() in ('mutate','navigate'):
        return page,'finished',dict(task_type=args[0].upper(),status='SUCCESS',retrieved_data=None)
    if op=='ANSWER':
        values=json.loads(line.partition(' ')[2])
        if not isinstance(values,list): raise ValueError('Expected a JSON array')
        return page,'finished',dict(task_type='RETRIEVE',status='SUCCESS',retrieved_data=values)
    if op in ('D','U') and not args: page.mouse.wheel(0,580 if op=='D' else -580)
    elif op=='B' and not args: page.go_back(wait_until='domcontentloaded',timeout=12000)
    elif op=='K' and args==['Enter']: page.keyboard.press('Enter')
    elif op=='T' and len(args)==1:
        index=int(args[0])
        if not 1<=index<=len(ctx.pages): raise ValueError('Unknown tab')
        page=ctx.pages[index-1];page.bring_to_front()
    elif op in ('C','H','F','S') and len(args)==(2 if op in ('F','S') else 1):
        num=int(args[0])
        el=page.locator(f'[data-ink-id="{num}"]')
        if el.count()!=1: raise ValueError('Control unavailable')
        if op=='H': el.hover(timeout=2000)
        elif op=='S': el.select_option(label=args[1],timeout=2000)
        else:
            tap(page,el)
            if op=='F':
                if not el.is_editable(): raise ValueError('Control is not editable')
                el.press('ControlOrMeta+a');page.keyboard.type(args[1],delay=25)
    else: raise ValueError('Unrecognized action')
    page.wait_for_timeout(300)
    return page,'acting',None

def observation(ctx,page):
    # A browser click can still be committing a document after the pointer returns.
    for attempt in range(8):
        try:
            page.wait_for_load_state('domcontentloaded',timeout=15000)
            tabs=' | '.join(f'{i+1} {p.title()[:85]}' for i,p in enumerate(ctx.pages))
            return f'Tabs: {tabs}\nActive tab {ctx.pages.index(page)+1}, path {urlsplit(page.url).path}\n'+page.evaluate(VIEW)
        except BrowserError:
            if attempt==7: raise
            page.wait_for_timeout(200)

def episode(browser,worker,wa,task,arm,out,fixture_reset=fresh):
    num=task['id']; site='reddit' if task['site'] in ('forum','reddit') else 'shopping'
    origin=URL[site]
    fixture_reset(site)
    native=wa.get_task(num)
    urls=[u.replace('__'+site.upper()+'__',origin) for u in native.start_urls]
    stem=f'{num:03d}-{arm}'
    har=out/(stem+'.har')
    ctx=browser.new_context(viewport={'width':1200,'height':720},device_scale_factor=1,locale='en-US',
                            service_workers='block',record_har_path=har,record_har_content='embed',
                            extra_http_headers=dict([AUTH[site]]))
    ctx.route('**/*',lambda r:r.continue_() if urlsplit(r.request.url).netloc==urlsplit(origin).netloc else r.abort())
    ctx.add_init_script(script=BOOT)
    steps=[];answer=None;history=[];state='limit'
    try:
        for url in urls:
            p=ctx.new_page()
            p.set_default_timeout(5000)
            res=p.goto(url,wait_until='domcontentloaded',timeout=45000)
            if res is None or res.status!=200: raise RuntimeError(f'Start page unavailable: {url}')
        page=ctx.pages[0];page.bring_to_front()
        page.wait_for_load_state('load',timeout=45000)
        page.evaluate('attachPointer()')
        movie=out/(stem+'.webm')
        page.screencast.start(path=movie,fps=20,size={'width':1200,'height':720})
        start=time.perf_counter()
        for _ in range(PANEL['max_decisions']):
            view=observation(ctx,page)
            prompt=native.intent+'\n'+view+'\nPrevious actions: '+(' / '.join(history[-6:]) or 'none')
            if hasattr(worker,'decide_web'):
                response=worker.decide_web(prompt,SYSTEM)
            else:
                worker.proc.stdin.write(json.dumps(dict(prompt=prompt,system=SYSTEM))+'\n');worker.proc.stdin.flush()
                response=json.loads(worker.proc.stdout.readline())
            if 'final' not in response: raise RuntimeError('Inference worker failed')
            line=response['final'].strip()
            step=dict(view=view,action=line,generated=response['generated'],thinking=response['thinking'],inference_s=response['seconds'])
            steps.append(step)
            try:
                page,state,answer=perform(page,ctx,line)
            except (ValueError, AssertionError, BrowserError) as exc:
                step['error']=str(exc).splitlines()[0][:180]
                state='invalid'
            history.append(line[:200]+(' ['+step['error']+']' if 'error' in step else ''))
            if state in ('stopped','finished'): break
        elapsed=time.perf_counter()-start
        ctx.pages[0].screencast.stop()
    finally:
        ctx.close()
    result=wa.evaluate_task(task_id=num,agent_response=answer,network_trace=har)
    trace_hash=hashlib.file_digest(har.open('rb'),'sha256').hexdigest()
    receipt=dict(id=num,arm=arm,site=site,elapsed_s=elapsed,termination=state,answer=answer,
                 score=result.score,grade=str(result.status),grader_error=result.error_msg,
                 grader_version=result.webarena_verified_version,har_sha256=trace_hash,steps=steps)
    if hasattr(worker,'hardware'):
        receipt['hardware']=worker.hardware
        receipt['fixture_origin']=origin
    write_json(out/(stem+'.json'),receipt)
    print(num,arm,result.score,result.status,round(elapsed,2),len(steps),flush=True)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--site',choices=('forum','shopping','all'),default='all')
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    wa=WebArenaVerified(config=WebArenaVerifiedConfig(environments={s:{'urls':[u]} for s,u in URL.items()}))
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path=BRAVE,headless=True)
        workers={}
        try:
            workers['original']=Planner('original')
            workers['selective']=Planner('edited')
            for i,t in enumerate(PANEL['tasks']):
                if args.site!='all' and (t['site']=='shopping')!=(args.site=='shopping'):continue
                for arm in (('original','selective') if i%2==0 else ('selective','original')):
                    if (args.out/f"{t['id']:03d}-{arm}.json").exists(): continue
                    episode(browser,workers[arm],wa,t,arm,args.out)
        finally:
            for w in workers.values(): w.close()
            browser.close()
if __name__=='__main__':main()
