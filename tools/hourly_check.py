"""Local supervisor report. Does not restart failed computations or publish."""
import argparse,json,subprocess,time
from pathlib import Path
from datetime import datetime,timezone
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--memory-dir');a=ap.parse_args();root=Path(a.out)
s=json.loads((root/'status.json').read_text());pid=s['pid']
p=subprocess.run(['tasklist','/FI',f'PID eq {pid}','/FO','CSV','/NH'],capture_output=True,text=True)
alive=f'"{pid}"' in p.stdout
r=dict(checked_at=datetime.now(timezone.utc).isoformat(),process_alive=alive,state=s['status'],unique_cases=s['unique_cases'],cpu_witnesses=s['cpu_witnesses'],max_gpu_difference=s['max_gpu_difference'],max_cpu_difference=s['max_cpu_difference'],temperature_c=s.get('temperature_c'),deadline_reached=time.time()>=s['deadline_epoch'])
(root/'hourly-status.json').write_text(json.dumps(r,indent=2)+'\n')
with (root/'hourly-history.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
if a.memory_dir:
    dest=Path(a.memory_dir);dest.mkdir(parents=True,exist_ok=True)
    now=datetime.now(timezone.utc);name=now.strftime('%Y%m%d-%H%M%S-array-layout.md')
    message='\n'.join(['# Array layout progress', '', 'Checked (UTC): '+r['checked_at'],
        'Worker alive: '+str(alive), 'State: '+r['state'],
        'Distinct synthetic geometry cases: '+str(r['unique_cases']),
        'Independent CPU witnesses: '+str(r['cpu_witnesses']),
        'Largest GPU-channel difference: '+str(r['max_gpu_difference']),
        'Largest CPU-reference difference: '+str(r['max_cpu_difference']),
        'GPU temperature C: '+str(r['temperature_c']),
        '', 'Scope: rectangular-array coordinates only. This does not establish electrical, structural or site approval.',
        'Private source documents and private equipment parameters stay outside public Git and website assets.',
        'Public interface: neutral wireframe array layout; configurable count, orientation, tilt and direction.',
        'Next: review current test/CI status and the private requirements admission ledger before release.',
        'This note is an automatic local checkpoint, not a claim that a human or AI reviewed this hour.', ''])
    (dest/name).write_text(message,encoding='utf-8')
    (dest/'LATEST.md').write_text(message,encoding='utf-8')
print(json.dumps(r))
