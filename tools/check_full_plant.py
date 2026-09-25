"""Enumerate all virtual-plant module corners in GPU batches; retain only summary.

Input template is produced by tested JS geometry. CPU checks placement arithmetic
independently; this is not an independent check of the input module template.
"""
import argparse
import json
import time
from pathlib import Path
import numpy as np
import cupy as cp

parser = argparse.ArgumentParser()
parser.add_argument('--template', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
source = json.loads(args.template.read_text())
site = source['site']
base = np.array(source['corners'], dtype=np.float64)
gpu_base = cp.asarray(base)
lo = np.full(3, np.inf)
hi = -lo
max_error = 0.
start = time.perf_counter()
for begin in range(0, site['modules'], 131072):
    stop = min(begin + 131072, site['modules'])
    ids = cp.arange(begin, stop, dtype=cp.int64)
    table = ids // site['modulesPerTable']
    points = gpu_base[ids % site['modulesPerTable']].copy()
    points[:, :, 0] += ((table % site['columns']) * site['pitch'][0] - site['min'][0])[:, None]
    points[:, :, 1] += ((table // site['columns']) * site['pitch'][1] - site['min'][1])[:, None]
    actual = cp.asnumpy(points)
    # Host quotient/remainder and offset matrix provide the second placement path.
    host = np.arange(begin, stop)
    tables, local = np.divmod(host, len(base))
    row, column = np.divmod(tables, site['columns'])
    offsets = np.column_stack([column * site['pitch'][0], row * site['pitch'][1], np.zeros(len(host))])
    expected = base[local] - np.array([*site['min'], 0]) + offsets[:, None, :]
    max_error = max(max_error, float(np.max(np.abs(actual - expected))))
    if not np.isfinite(actual).all() or max_error > 1e-8:
        raise RuntimeError('Full-plant placement mismatch')
    lo = np.minimum(lo, actual.min(axis=(0, 1)))
    hi = np.maximum(hi, actual.max(axis=(0, 1)))
result = {'status': 'pass', 'modules': site['modules'], 'corners': site['modules'] * 4,
          'coordinates': site['modules'] * 12, 'max_cpu_gpu_difference_m': max_error,
          'bounds_min_m': lo.tolist(), 'bounds_max_m': hi.tolist(),
          'seconds': time.perf_counter() - start,
          'scope': 'Every module in synthetic regular placement; no terrain, exclusions, cables or approval. Template geometry checked separately in JS tests.'}
args.out.write_text(json.dumps(result, indent=2))
print(json.dumps({k: result[k] for k in ['status', 'modules', 'coordinates', 'max_cpu_gpu_difference_m', 'seconds']}))
