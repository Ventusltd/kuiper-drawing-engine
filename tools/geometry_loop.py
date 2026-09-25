"""Bounded synthetic array geometry comparison; compact local outputs only."""
import argparse, json, math, os, subprocess, time
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import cupy as cp

SPACE=720*601*10*60*271*2
KERNEL=cp.RawKernel(r'''
extern "C" __global__ void corners(unsigned long long start,int n,double* out){
 int k=blockDim.x*blockIdx.x+threadIdx.x;if(k>=n)return;
 unsigned long long i=start+k;int a=i%720;i/=720;int t=i%601;i/=601;
 int rows=i%10+1;i/=10;int cols=i%60+1;i/=60;int h=i%271;i/=271;int landscape=i%2;
 double az=a*0.5*3.141592653589793/180.,tilt=t*0.1*3.141592653589793/180.;
 double length=landscape?1.2:2.4,width=landscape?2.4:1.2;
 double run=rows*length+(rows-1)*.02,half=(cols*width+(cols-1)*.02)/2.;
 out[3*k]=cos(az)*half-sin(az)*cos(tilt)*run;
 out[3*k+1]=-sin(az)*half-cos(az)*cos(tilt)*run;
 out[3*k+2]=.3+h*.01+sin(tilt)*run;
}''','corners')

def atomic(path,data):
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');temp.replace(path)

def witness(ids):
    results=[]
    for value in ids:
        i=int(value);a=i%720;i//=720;t=i%601;i//=601;rows=i%10+1;i//=10;cols=i%60+1;i//=60;h=i%271;i//=271;landscape=i%2
        az=math.radians(a*.5);tilt=math.radians(t*.1);length,width=(1.2,2.4) if landscape else (2.4,1.2)
        run=rows*length+(rows-1)*.02;half=(cols*width+(cols-1)*.02)/2
        u=np.array([math.cos(az),-math.sin(az),0.]);v=np.array([-math.sin(az)*math.cos(tilt),-math.cos(az)*math.cos(tilt),math.sin(tilt)])
        results.append(u*half+v*run+np.array([0.,0.,.3+h*.01]))
    return np.array(results)

def batch(start,n):
    i=cp.arange(start,start+n,dtype=cp.uint64);a=i%720;i//=720;t=i%601;i//=601;rows=i%10+1;i//=10;cols=i%60+1;i//=60;h=i%271;i//=271;landscape=i%2
    az=a.astype(cp.float64)*(.5*math.pi/180);tilt=t.astype(cp.float64)*(.1*math.pi/180)
    run=rows*cp.where(landscape,1.2,2.4)+(rows-1)*.02
    half=(cols*cp.where(landscape,2.4,1.2)+(cols-1)*.02)/2
    radius=cp.hypot(half,run*cp.cos(tilt));angle=cp.arctan2(-run*cp.cos(tilt),half)-az
    other=cp.stack([radius*cp.cos(angle),radius*cp.sin(angle),.3+h*.01+run*cp.cos(math.pi/2-tilt)],axis=1)
    actual=cp.empty((n,3),cp.float64);KERNEL(((n+255)//256,),(256,),(np.uint64(start),np.int32(n),actual))
    error=float(cp.max(cp.abs(actual-other)).get());invalid=int(cp.count_nonzero(~cp.isfinite(actual)).get())
    sample=np.unique(np.linspace(0,n-1,min(n,257),dtype=np.int64));got=cp.asnumpy(actual[cp.asarray(sample)])
    cpu_error=float(np.max(np.abs(got-witness(start+sample))))
    return dict(max_gpu_difference=error,max_cpu_difference=cpu_error,cpu_witnesses=len(sample),nonfinite=invalid)

def temperature():
    try:return float(subprocess.check_output(['nvidia-smi','--query-gpu=temperature.gpu','--format=csv,noheader,nounits'],text=True,timeout=10).splitlines()[0])
    except Exception:return None

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--hours',type=float,default=5);ap.add_argument('--batch',type=int,default=1048576);ap.add_argument('--smoke',action='store_true');args=ap.parse_args()
    if not 0<args.hours<=5 or not 1<=args.batch<=4194304:raise ValueError('Bound exceeded')
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);lock=out/'running.lock'
    fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
    start_time=time.time();deadline=start_time+args.hours*3600
    state=dict(status='starting',pid=os.getpid(),started_at=datetime.now(timezone.utc).isoformat(),deadline_epoch=deadline,
               unique_cases=0,space=SPACE,batches=0,cpu_witnesses=0,max_gpu_difference=0.,max_cpu_difference=0.,
               scope='Synthetic rectangular-array corner geometry only; not shading, electrical suitability or engineering approval.')
    cp.get_default_memory_pool().set_limit(size=2*1024**3)
    try:
        # Dispersed whole-domain witnesses, not only the first azimuth interval.
        for index in [0,719,720,432719,SPACE//2,SPACE-1024]:
            test=batch(index,128)
            if max(test['max_gpu_difference'],test['max_cpu_difference'])>1e-8 or test['nonfinite']:raise ValueError('Initial reference comparison failed')
        while time.time()<deadline and state['unique_cases']<SPACE:
            if (out/'STOP').exists():state['status']='stopped';break
            temp=temperature();state['temperature_c']=temp;state['heartbeat']=datetime.now(timezone.utc).isoformat()
            if temp is None or temp>=80:
                state['status']='thermal_pause';atomic(out/'status.json',state);time.sleep(30);continue
            n=min(args.batch,SPACE-state['unique_cases']);begin=state['unique_cases'];tick=time.perf_counter();result=batch(begin,n);elapsed=time.perf_counter()-tick
            if max(result['max_gpu_difference'],result['max_cpu_difference'])>1e-8 or result['nonfinite']:raise ValueError('Numerical disagreement; results quarantined')
            state.update(status='running',unique_cases=begin+n,batches=state['batches']+1,last_batch_seconds=elapsed,
                         cpu_witnesses=state['cpu_witnesses']+result['cpu_witnesses'],
                         max_gpu_difference=max(state['max_gpu_difference'],result['max_gpu_difference']),
                         max_cpu_difference=max(state['max_cpu_difference'],result['max_cpu_difference']))
            atomic(out/'status.json',state)
            if args.smoke:break
            time.sleep(1)
        if state['status']=='running':state['status']='smoke_pass' if args.smoke else 'deadline_reached' if time.time()>=deadline else 'domain_complete'
    except Exception as exc:
        state.update(status='failed',error=type(exc).__name__+': '+str(exc));raise
    finally:
        state['elapsed_seconds']=time.time()-start_time;atomic(out/'status.json',state);lock.unlink(missing_ok=True)
        print(json.dumps({k:state.get(k) for k in ['status','unique_cases','cpu_witnesses','max_gpu_difference','max_cpu_difference']}))
if __name__=='__main__':main()
