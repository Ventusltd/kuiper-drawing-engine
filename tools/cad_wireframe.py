"""Local STEP edge preview. Source and derived drawings retain source restrictions.

No upload or publication. Requires an isolated OCP runtime supplied by the user.
"""
import argparse
import json
import math
import sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--runtime', type=Path, required=True)
p.add_argument('--step', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
a = p.parse_args()
sys.path.insert(0, str(a.runtime))
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Curve

reader = STEPControl_Reader()
if reader.ReadFile(str(a.step)) != IFSelect_RetDone:
    raise ValueError('STEP could not be read')
reader.TransferRoots()
explorer = TopExp_Explorer(reader.OneShape(), TopAbs_EDGE)
lines = []
while explorer.More():
    curve = BRepAdaptor_Curve(TopoDS.Edge_s(explorer.Current()))
    first, last = curve.FirstParameter(), curve.LastParameter()
    if not math.isfinite(first + last):
        raise ValueError('Unbounded edge')
    points = []
    for i in range(21):
        point = curve.Value(first + (last - first) * i / 20)
        x, y, z = point.X(), point.Y(), point.Z()
        points.append((math.sqrt(3) / 2 * (x - y), (x + y) / 2 - z))
    lines.append(points)
    if len(lines) > 10000:
        raise ValueError('Preview edge budget exceeded')
    explorer.Next()
if not lines:
    raise ValueError('No edges found')
xs = [p[0] for line in lines for p in line]
ys = [p[1] for line in lines for p in line]
lo = [min(xs), min(ys)]
factor = min(960 / max(max(xs) - lo[0], 1e-9), 660 / max(max(ys) - lo[1], 1e-9))
paths = []
for line in lines:
    points = ' '.join(f'{20+(x-lo[0])*factor:.3f},{20+(y-lo[1])*factor:.3f}' for x,y in line)
    paths.append(f'<polyline points="{points}"/>')
a.out.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700"><title>Local CAD edge preview; uniformly sampled curves; source restrictions apply</title><g fill="none" stroke="#333" stroke-width="0.5">' + ''.join(paths) + '</g></svg>')
print(json.dumps({'status': 'pass', 'edges': len(lines), 'curve_samples': len(lines) * 21,
                  'bytes': a.out.stat().st_size, 'publication': 'not authorized by this tool'}))
