"""Private draft height-envelope sweep. Candidate counts are not probabilities."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import cupy as cp

p=argparse.ArgumentParser()
p.add_argument('--evidence',type=Path,required=True)
p.add_argument('--profile',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
a=p.parse_args()
e=json.loads(a.evidence.read_text());s=json.loads(a.profile.read_text())
facts={row['key']:row for row in e['facts']}
floor=facts['module_lowest_part_height_min']['value']
ceiling=facts['module_highest_part_height_max']['value']
length=s['moduleLength'] if s['orientation']=='portrait' else s['moduleWidth']
run=s['rows']*length+(s['rows']-1)*s['gap']
heights=np.arange(math.ceil(floor*100),math.floor(ceiling*100)+1)/100
tilts=np.arange(6001)/100
gpu=cp.asarray(heights)[:,None]+run*cp.sin(cp.deg2rad(cp.asarray(tilts)))[None,:]
actual=cp.asnumpy(gpu)
cpu=heights[:,None]+run*np.sin(tilts*np.pi/180)[None,:]
error=float(np.max(np.abs(actual-cpu)));band=np.abs(cpu-ceiling)<=1e-9
differences=int(np.count_nonzero(((actual<=ceiling)!=(cpu<=ceiling))&~band))
if error>1e-9 or differences or not np.isfinite(actual).all():raise RuntimeError('Envelope comparison failed')
top=s['height']+run*math.sin(math.radians(s['tilt']))
result={'scope':'Known contract height bounds only; no structural, terrain, shading or as-built admission',
        'candidate_cells':int(cpu.size),'feasible_outside_boundary_band':int(((cpu<ceiling)&~band).sum()),
        'boundary_band_cells':int(band.sum()),'max_cpu_gpu_error_m':error,
        'classification_differences_outside_boundary_band':differences,
        'selected_top_height_m':top,'selected_satisfies_known_height_bounds':s['height']>=floor and top<=ceiling,
        'source_facts':[facts[k] for k in ['module_lowest_part_height_min','module_highest_part_height_max']],
        'unknowns':['approved nominal tilt and mounting geometry','field-specific exceptions','terrain and structural loading'],
        'publication':'private only; no probability or engineering approval claim'}
a.out.write_text(json.dumps(result,indent=2))
print(json.dumps({k:result[k] for k in ['candidate_cells','max_cpu_gpu_error_m','classification_differences_outside_boundary_band']}))
