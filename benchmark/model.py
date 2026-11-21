from pathlib import Path
import sys,json,time
from mlx_lm import load,stream_generate
from mlx_lm.sample_utils import make_sampler
import mlx.core as mx
m,t=load(sys.argv[1],trust_remote_code=True)
sampler=make_sampler(temp=0)
def respond(req):
 messages=[{'role':'system','content':'Operate the browser using the numbered controls in the observation. Work efficiently. Respond directly with the actions, one per line. A fill is F <id> <value>. A button click is C <id>. Use only the provided IDs. No commentary.'},{'role':'user','content':req['prompt']}]
 prompt=t.apply_chat_template(messages,tokenize=False,reasoning_effort='none')
 tokens=t.encode(prompt,add_special_tokens=False)
 ids=[];start=time.perf_counter()
 for x in stream_generate(m,t,prompt=tokens,sampler=sampler,max_tokens=384):
  ids.append(x.token)
 s=t.decode(ids,skip_special_tokens=False)
 # Extract only explicit final-channel content. Reasoning never reaches the browser.
 segments=s.split('<|content_text|>')
 final=segments[-1].split('<|end_message|>')[0].split('<|content_model_end_sampling|>')[0].strip() if len(segments)>1 else ''
 n_think=0;inside=False
 for i in ids:
  if i==200008:inside=True
  elif i in (200004,200001,200005,200006):inside=False
  elif inside:n_think+=1
 return dict(final=final,generated=len(ids),thinking=n_think,seconds=time.perf_counter()-start)
respond({'prompt':'Click Go. Controls: 7 button Go.'})
print('READY',flush=True)
for l in sys.stdin:
 try:print(json.dumps(respond(json.loads(l))),flush=True)
 except Exception as e:print(json.dumps({'error':str(e)}),flush=True)
