"""Local-only lexical drawing-code inventory; never executes discovered code.

GPU channel matches literal byte patterns; CPU channel independently uses bytes
membership on every input. Agreement proves matching only, not code semantics.
Paths and inventory stay outside the public repository. No file contents output.
"""
import argparse, hashlib, json, os, subprocess, time
from pathlib import Path
import numpy as np
import cupy as cp

PATTERNS = [b'canvas', b'webgl', b'buffergeometry', b'linesegments', b'orthographic',
            b'perspective', b'junction', b'azimuth', b'portrait', b'landscape',
            b'transform', b'polyline', b'polygon', b'quaternion', b'arraygeometry',
            b'modulegeometry', b'raycast', b'svg', b'instanc', b'bezier']
KERNEL = cp.RawKernel(r'''
extern "C" __global__ void match(const unsigned char* text,const long long* ends,
 const unsigned char* patterns,const int* sizes,int files,int count,unsigned char* out){
 int k=blockDim.x*blockIdx.x+threadIdx.x;if(k>=files*count)return;
 int f=k/count,p=k%count,n=sizes[p];long long begin=f?ends[f-1]:0,end=ends[f];
 unsigned char found=0;
 for(long long j=begin;j+n<=end&&!found;j++){
  int t=0;while(t<n&&text[j+t]==patterns[p*32+t])t++;if(t==n)found=1;
 }out[k]=found;
}''', 'match')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--out',required=True)
    args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    start=time.perf_counter();records=[];skipped=0;total=0;bytes_read=0;gpu_ms=0.;mismatch=0
    patterns=np.zeros((len(PATTERNS),32),np.uint8)
    for i,p in enumerate(PATTERNS):patterns[i,:len(p)]=np.frombuffer(p,np.uint8)
    gp=cp.asarray(patterns);gs=cp.asarray(np.array(list(map(len,PATTERNS)),np.int32))
    batch=[];batch_bytes=0
    def flush():
        nonlocal total,bytes_read,gpu_ms,mismatch,batch,batch_bytes
        if not batch:return
        contents=[x[2] for x in batch];ends=np.cumsum([len(x) for x in contents],dtype=np.int64)
        body=b''.join(contents);result=cp.empty((len(batch),len(PATTERNS)),cp.uint8)
        dev=cp.asarray(np.frombuffer(body,np.uint8));de=cp.asarray(ends)
        a,b=cp.cuda.Event(),cp.cuda.Event();a.record()
        KERNEL(((result.size+127)//128,),(128,),(dev,de,gp,gs,len(batch),len(PATTERNS),result));b.record();b.synchronize()
        gpu_ms+=cp.cuda.get_elapsed_time(a,b);got=cp.asnumpy(result)
        reference=np.array([[p in content for p in PATTERNS] for content in contents],np.uint8)
        mismatch+=int(np.count_nonzero(got!=reference))
        for (repo,path,content),flags in zip(batch,got):
            found=[p.decode() for p,v in zip(PATTERNS,flags) if v]
            if found:records.append(dict(repository=repo,path=path,bytes=len(content),sha256=hashlib.sha256(content).hexdigest(),patterns=found,review='lexical candidate; licence and semantics not yet admitted'))
        total+=len(batch);bytes_read+=len(body);batch=[];batch_bytes=0
    for repo in sorted(Path(args.root).iterdir()):
        if not repo.is_dir() or not (repo/'.git').exists():continue
        proc=subprocess.run(['git','ls-files','-z'],cwd=repo,capture_output=True)
        if proc.returncode:continue
        for name in proc.stdout.decode('utf-8',errors='replace').split('\0'):
            path=repo/name
            if not name or path.suffix.lower() not in {'.js','.mjs','.cjs','.ts','.tsx','.html','.py','.glsl','.wgsl'}:continue
            if any(part in {'node_modules','.venv','vendor','dist','build'} for part in Path(name).parts):continue
            try:
                if path.is_symlink() or path.stat().st_size>2_000_000:skipped+=1;continue
                content=path.read_bytes().lower()
            except OSError:skipped+=1;continue
            batch.append((repo.name,name,content));batch_bytes+=len(content)
            if batch_bytes>=32_000_000 or len(batch)>=512:flush()
    flush()
    records.sort(key=lambda r:(-len(r['patterns']),r['repository'],r['path']))
    with (out/'drawing-candidates.private.jsonl').open('w',encoding='utf-8') as f:
        for row in records:f.write(json.dumps(row)+'\n')
    receipt=dict(status='pass' if mismatch==0 else 'fail',files=total,bytes=bytes_read,candidates=len(records),skipped=skipped,
                 pattern_checks=total*len(PATTERNS),cpu_gpu_differences=mismatch,gpu_kernel_ms=gpu_ms,wall_seconds=time.perf_counter()-start,
                 scope='Tracked text code in local repositories; excluded vendored/generated/oversize files. Literal matching only; no semantic or complete estate claim.')
    (out/'inventory-summary.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print(json.dumps(receipt))
    return bool(mismatch)
if __name__=='__main__':raise SystemExit(main())
