"""Local GPU similarity graph over lexical code features; not semantic approval."""
import argparse,json,time
from pathlib import Path
import cupy as cp
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--audit',required=True);args=ap.parse_args();root=Path(args.audit)
rows=[json.loads(x) for x in (root/'drawing-candidates.private.jsonl').read_text().splitlines()]
vocabulary=sorted({p for r in rows for p in r['patterns']});lookup={p:i for i,p in enumerate(vocabulary)}
x=np.zeros((len(rows),len(vocabulary)),np.float32)
for i,r in enumerate(rows):
    for p in r['patterns']:x[i,lookup[p]]=1
idf=np.log((len(rows)+1)/(x.sum(0)+1))+1;x*=idf;x/=np.maximum(np.linalg.norm(x,axis=1,keepdims=True),1e-12)
gx=cp.asarray(x);indices=[];weights=[];max_error=0.;started=time.perf_counter()
for begin in range(0,len(rows),256):
    similarity=gx[begin:begin+256]@gx.T
    local=cp.arange(similarity.shape[0]);similarity[local,begin+local]=-1
    best=cp.argpartition(similarity,-5,axis=1)[:,-5:];value=cp.take_along_axis(similarity,best,axis=1)
    indices.append(best);weights.append(cp.maximum(value,0))
    if begin==0:
        actual=cp.asnumpy(similarity[:8,:128]);expected=x[:8]@x[:128].T
        for i in range(8):expected[i,i]=-1
        max_error=float(np.max(np.abs(actual-expected)))
neighbors=cp.concatenate(indices);weight=cp.concatenate(weights);weight/=cp.maximum(weight.sum(1,keepdims=True),1e-12)
seed=np.array([sum(p in r['patterns'] for p in ['modulegeometry','arraygeometry','portrait','azimuth','junction']) for r in rows],np.float32)
seed/=max(float(seed.sum()),1);base=cp.asarray(seed);rank=base.copy()
for _ in range(24):
    nxt=.2*base;cp.add.at(nxt,neighbors.ravel(),(.8*rank[:,None]*weight).ravel());rank=nxt
selected=cp.asnumpy(cp.argsort(rank)[-100:][::-1]);scores=cp.asnumpy(rank[selected]);result=[]
for index,score in zip(selected,scores):
    row=dict(rows[int(index)]);row['lexical_graph_score']=float(score);result.append(row)
(root/'drawing-shortlist.private.json').write_text(json.dumps({'scope':'Lexical feature similarity and bounded propagation. Candidate discovery only; source/licence review still required.','items':result},indent=2))
summary=dict(files=len(rows),edges=len(rows)*5,propagation_steps=24,cpu_gpu_similarity_error=max_error,wall_seconds=time.perf_counter()-started,status='pass' if max_error<1e-5 else 'fail')
(root/'distillation-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary))
if max_error>=1e-5:raise SystemExit(1)
