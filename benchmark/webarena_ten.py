"""Run a frozen WebArena-Verified panel with a fresh fixture per episode."""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import time
from urllib.parse import urljoin, urlsplit
from html.parser import HTMLParser
from urllib.request import HTTPCookieProcessor, Request, build_opener, urlopen
from http.cookiejar import CookieJar

from playwright.sync_api import sync_playwright, Error as BrowserError
from webarena_verified.api import WebArenaVerified
from webarena_verified.types.config import WebArenaVerifiedConfig
from run import BOOT, BRAVE, Planner, tap, write_json

HERE = Path(__file__).resolve().parent
PANEL = json.loads((HERE.parent / 'evidence/webarena-ten-panel.json').read_text())
PANEL['max_decisions'] = 12
PORTS = {'shopping': 7770, 'reddit': 9999, 'shopping_admin': 7780}
FIXTURES = {'shopping': 'shop', 'reddit': 'forum', 'shopping_admin': 'shop-admin'}
FIXTURE_IMAGES = {
    'reddit': 'am1n3e/webarena-verified-reddit@sha256:0594908059a03e5f610005689440a95c05e776e734006197c7b1eba12734cb46',
    'shopping': 'am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb',
    'shopping_admin': 'am1n3e/webarena-verified-shopping_admin@sha256:d0531dd27ed98d0c459ff9e88118bf2ed8b660b0ed99c38837db46c065a5be13',
}
# Synthetic benchmark accounts shipped with each fixture.
AUTH = {'shopping': ('X-M2-Customer-Auto-Login', 'emma.lopez@gmail.com:Password.123'),
        'shopping_admin': ('X-M2-Admin-Auto-Login', 'admin:admin1234'),
        'reddit': ('X-Postmill-Auto-Login', 'MarvelsGrantMan136:test1234')}
URL = {site: f'http://127.0.0.1:{port}' for site, port in PORTS.items()}
SYSTEM = """Operate this browser to finish the user's task. Return one action per decision.
C id clicks a link or button. H id hovers a menu. F id text fills a field. K Enter submits the focused field. S id label selects an option. D or U scrolls one screen. B goes back. T number switches to a listed tab.
When you have reached the requested page, return DONE navigate. After successfully changing something, return DONE mutate. To answer a question, return ANSWER followed by a JSON array of the requested values. Submit success only after observing the requested result. If a goal cannot be completed after checking, return FAIL followed by task type (RETRIEVE, NAVIGATE or MUTATE), status (NOT_FOUND_ERROR, ACTION_NOT_ALLOWED_ERROR, PERMISSION_DENIED_ERROR, DATA_VALIDATION_ERROR or UNKNOWN_ERROR), and a short reason. Use only the listed controls. Return just one command."""
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
   let state='';
   if(e.matches('input:not([type=password]):not([type=submit]):not([type=button]),textarea,select'))state+=' value='+JSON.stringify(String(e.value||'').slice(0,110));
   if(e.matches('input[type=checkbox],input[type=radio]'))state+=' checked='+e.checked;
   if(e===document.activeElement)state+=' focused';
   controls.push(id+' '+(e.type||e.tagName.toLowerCase())+' '+label.slice(0,110)+state);
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

def storefront_links_match(html,origin):
    targets=[]
    class AccountLinks(HTMLParser):
        def handle_starttag(self,tag,attrs):
            if tag=='a':
                target=urlsplit(urljoin(origin+'/',dict(attrs).get('href') or ''))
                if target.path.rstrip('/')=='/customer/account':targets.append(target.netloc)
    AccountLinks().feed(html)
    return bool(targets) and all(t==urlsplit(origin).netloc for t in targets)

def fresh(site):
    """Only replace a container carrying this experiment's unique owner label."""
    name = 'inkling-wa-' + FIXTURES[site]
    found = subprocess.run(['docker','inspect','--format','{{index .Config.Labels "inkling.experiment"}}',name],capture_output=True,text=True)
    if found.returncode == 0:
        if found.stdout.strip() != 'webarena':
            raise RuntimeError('Fixture name belongs to another process')
        subprocess.run(['docker','rm','-f',name],check=True,stdout=subprocess.DEVNULL)
    port = PORTS[site]
    ctrl = {'shopping':7771, 'reddit':9998, 'shopping_admin':7781}[site]
    image = FIXTURE_IMAGES[site]
    subprocess.run(['docker','run','-d','--rm','--platform','linux/amd64','--name',name,
                    '--label','inkling.experiment=webarena','-p',f'127.0.0.1:{port}:80',
                    '-p',f'127.0.0.1:{ctrl}:8877','-e',f'WA_ENV_CTRL_EXTERNAL_SITE_URL={URL[site]}',image],
                   check=True,stdout=subprocess.DEVNULL)
    start=time.monotonic()
    cache_cleared=False
    healthy_path, marker={'shopping':('/customer/account/',b'Account Information'),
                          'reddit':('/',b'MarvelsGrantMan136'),'shopping_admin':('/admin',b'Dashboard')}[site]
    while time.monotonic()-start < 250:
        try:
            fetch=build_opener(HTTPCookieProcessor(CookieJar())).open if site=='shopping_admin' else urlopen
            with fetch(Request(URL[site]+healthy_path,headers=dict([AUTH[site]])),timeout=18) as resp:
                if resp.status==200 and urlsplit(resp.url).netloc==urlsplit(URL[site]).netloc and marker in resp.read():
                    if site=='shopping':
                        check=subprocess.run(['docker','exec',name,'curl','-fsS','--max-time','8',
                            'http://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=5s'],
                            capture_output=True,text=True)
                        if check.returncode or json.loads(check.stdout).get('status') not in ('yellow','green'):
                            time.sleep(2)
                            continue
                        with urlopen(Request(URL[site]+'/',headers=dict([AUTH[site]])),timeout=18) as home:
                            matches=storefront_links_match(home.read().decode('utf-8','replace'),URL[site])
                        if not matches:
                            if not cache_cleared:
                                subprocess.run(['docker','exec',name,'php','/var/www/magento2/bin/magento','cache:clean','config','full_page','block_html'],capture_output=True,timeout=55)
                                cache_cleared=True
                            time.sleep(2)
                            continue
                    return
        except (OSError, ValueError):
            pass
        time.sleep(2)
    raise RuntimeError(f'{site} fixture did not pass signed-in health check')

def perform(page,ctx,line,field_selection='keyboard'):
    # Compact and spaced control IDs express the same action. Keep prose invalid.
    line=re.sub(r'^([CHFST])(?=\d)',r'\1 ',line,flags=re.I)
    if line.startswith('['):
        values=json.loads(line)
        if isinstance(values,list):
            return page,'finished',dict(task_type='RETRIEVE',status='SUCCESS',retrieved_data=values)
    parts=line.split(maxsplit=2)
    if not parts:raise ValueError('No final action')
    op,*args=parts
    op=op.upper()
    if op == 'FAIL':
        from webarena_verified.types.agent_response import FinalAgentResponse, Status
        _, goal, status, reason = line.split(maxsplit=3)
        status = Status(status.upper())
        if status == Status.SUCCESS or not reason.strip():
            raise ValueError('Expected a failure status and reason')
        response = FinalAgentResponse.model_validate(dict(task_type=goal, status=status, error_details=reason))
        return page, 'finished', response.model_dump(mode='json')
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
                if field_selection=='select-text':
                    el.select_text()
                else:
                    el.press('ControlOrMeta+a')
                page.keyboard.type(args[1],delay=25)
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

def wait_for_start_page(page,site):
    page.wait_for_load_state('load',timeout=45000)
    if site=='shopping_admin' and page.get_by_role('heading',name='Dashboard',exact=True).count():
        # Magento fills the dashboard tabs and their table asynchronously.
        page.locator('a').filter(has_text=re.compile(r'^\s*Most Viewed Products\s*$')).first.wait_for(state='visible',timeout=30000)
        page.locator('#productsOrderedGrid_table tbody td.col-product').first.wait_for(state='visible',timeout=30000)
        page.evaluate("async () => { await document.fonts.ready; await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))); }")

def matched_admin_dashboard(ctx,page,expected=None,*,attach_pointer=False):
    # The official storefront can list tied bestsellers in different orders.
    # Compare the complete observed UI before inference. Each retry loads the unmodified dashboard.
    for attempt in range(16):
        if attempt:
            page.reload(wait_until='load',timeout=45000)
        wait_for_start_page(page,'shopping_admin')
        if attach_pointer:page.evaluate('attachPointer()')
        observed_at=time.perf_counter()
        view=observation(ctx,page)
        if expected is None or view==expected:
            return view,attempt,observed_at
    raise RuntimeError('Could not reproduce the first arm’s dashboard before inference.')

def episode(browser,worker,wa,task,arm,out,fixture_reset=fresh,field_selection='keyboard',expected_start_view=None):
    if field_selection not in ('keyboard','select-text'):
        raise ValueError('Unknown field selection method')
    num=task['id']; site={'shop':'shopping','forum':'reddit'}.get(task['site'],task['site'])
    origin=URL[site]
    fixture_reset(site)
    native=wa.get_task(num)
    entry=origin+'/admin' if site=='shopping_admin' else origin
    urls=[u.replace('__'+site.upper()+'__',entry) for u in native.start_urls]
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
        prepared_view=None
        preflight_reloads=0
        wait_for_start_page(page,site)
        page.evaluate('attachPointer()')
        movie=out/(stem+'.webm')
        recorders = list(ctx.pages)
        capture_start = []
        for index, tab in enumerate(recorders):
            path = movie if index == 0 else out / (stem + f'.tab{index+1}.webm')
            capture_start.append(time.perf_counter())
            tab.screencast.start(path=path, fps=20, size={'width':1200,'height':720})
        start=time.perf_counter()
        if site=='shopping_admin':
            # Recording can change the visible viewport. Match the live decision input
            # with the recorder attached, and include its observation in the task clock.
            prepared_view,preflight_reloads,start=matched_admin_dashboard(
                ctx,page,expected_start_view,attach_pointer=True)
        for _ in range(PANEL['max_decisions']):
            step_start=time.perf_counter()-start
            active_tab=ctx.pages.index(page)+1
            if not steps and prepared_view is not None:
                step_start=0.0
                view=prepared_view
            else:view=observation(ctx,page)
            prompt=native.intent+'\n'+view+'\nPrevious actions: '+(' / '.join(history[-6:]) or 'none')
            if hasattr(worker,'decide_web'):
                response=worker.decide_web(prompt,SYSTEM)
            else:
                worker.proc.stdin.write(json.dumps(dict(prompt=prompt,system=SYSTEM))+'\n');worker.proc.stdin.flush()
                response=json.loads(worker.proc.stdout.readline())
            if 'final' not in response: raise RuntimeError('Inference worker failed')
            line=response['final'].strip()
            step=dict(start_s=step_start,tab=active_tab,view=view,action=line,generated=response['generated'],thinking=response['thinking'],inference_s=response['seconds'])
            steps.append(step)
            try:
                page,state,answer=perform(page,ctx,line,field_selection)
            except (ValueError, AssertionError, BrowserError) as exc:
                step['error']=str(exc).splitlines()[0][:180]
                state='invalid'
            history.append(line[:200]+(' ['+step['error']+']' if 'error' in step else ''))
            if state in ('stopped','finished'): break
        elapsed=time.perf_counter()-start
        for tab in recorders: tab.screencast.stop()
    finally:
        ctx.close()
    result=wa.evaluate_task(task_id=num,agent_response=answer,network_trace=har)
    trace_hash=hashlib.file_digest(har.open('rb'),'sha256').hexdigest()
    receipt=dict(capture_lead_s=[start-t for t in capture_start],id=num,arm=arm,site=site,elapsed_s=elapsed,termination=state,answer=answer,
                 score=result.score,grade=str(result.status),grader_error=result.error_msg,
                 grader_version=result.webarena_verified_version,har_sha256=trace_hash,steps=steps)
    if hasattr(worker,'hardware'):
        receipt['hardware']=worker.hardware
        receipt['fixture_origin']=origin
    receipt['field_selection']=field_selection
    if site=='shopping_admin':receipt['preflight_reloads']=preflight_reloads
    write_json(out/(stem+'.json'),receipt)
    print(num,arm,result.score,result.status,round(elapsed,2),len(steps),flush=True)

