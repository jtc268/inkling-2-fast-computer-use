"""Greedy SGLang worker for an already-loaded Inkling checkpoint."""
import json
import time
from urllib.request import Request, urlopen
from transformers import AutoTokenizer

class CudaWorker:
    def __init__(self,endpoint,tokenizer_dir,hardware,token_limit=384):
        self.endpoint=endpoint.rstrip('/')
        self.tokenizer=AutoTokenizer.from_pretrained(str(tokenizer_dir),local_files_only=True)
        self.hardware=hardware
        self.token_limit=token_limit

    def decide_web(self,prompt,system):
        messages=[{'role':'system','content':system},{'role':'user','content':prompt}]
        rendered=self.tokenizer.apply_chat_template(messages,tokenize=False,reasoning_effort='none')
        input_ids=self.tokenizer.encode(rendered,add_special_tokens=False)
        params={'temperature':0,'max_new_tokens':self.token_limit,'skip_special_tokens':False}
        body=json.dumps({'input_ids':input_ids,'sampling_params':params}).encode()
        start=time.perf_counter()
        with urlopen(Request(self.endpoint+'/generate',data=body,headers={'Content-Type':'application/json'}),timeout=90) as response:
            result=json.load(response)
        elapsed=time.perf_counter()-start
        ids=result['output_ids']
        decoded=self.tokenizer.decode(ids,skip_special_tokens=False)
        segments=decoded.split('<|content_text|>')
        final=segments[-1].split('<|end_message|>')[0].split('<|content_model_end_sampling|>')[0].strip() if len(segments)>1 else ''
        inside=False
        thinking=0
        for token in ids:
            if token==200008:inside=True
            elif token in (200004,200001,200005,200006):inside=False
            elif inside:thinking+=1
        return dict(final=final,generated=len(ids),thinking=thinking,seconds=elapsed)
