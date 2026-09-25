import test from 'node:test';import assert from 'node:assert/strict';import {defaults,array,plant,basis,validate} from '../web/geometry.mjs';
test('five portrait opposing faces and single portrait directions',()=>{assert.equal(array(defaults).modules.length,60);for(const azimuth of [0,90,180,270]){const m=array({...defaults,rows:1,columns:1,layout:'fixed',azimuth});assert.equal(m.modules.length,1);assert(Math.abs(m.rise-2.4*Math.sin(12*Math.PI/180))<1e-12);}});
test('orthonormal frame and module sizes over angular grid',()=>{for(let a=0;a<360;a+=5)for(let t=0;t<=60;t+=2){const b=basis(a,t);for(const v of Object.values(b))assert(Math.abs(Math.hypot(...v)-1)<1e-12);assert(Math.abs(b.u.reduce((s,v,i)=>s+v*b.v[i],0))<1e-12);const m=array({...defaults,rows:1,columns:1,layout:'fixed',azimuth:a,tilt:t}).modules[0];assert(Math.abs(Math.hypot(...m.corners[1].map((v,i)=>v-m.corners[0][i]))-1.2)<1e-10);}});
test('opposing faces meet across ridge and retain lower height',()=>{const m=array({...defaults,columns:1});const top=m.modules.filter(x=>x.row===5);const p=top[0].corners[3],q=top[1].corners[2];assert(Math.abs(p[2]-q[2])<1e-12);assert(m.modules.every(x=>x.corners.every(p=>p[2]>=defaults.height)));});
test('1 GW string rounding and bounded geometry',()=>{const p=plant(defaults);assert(p.actualDCMW>=1000);assert(p.actualDCMW-1000<defaults.series*defaults.moduleW/1e6);assert.equal(p.modules,p.strings*30);assert(p.lastInverterStrings>=1&&p.lastInverterStrings<=24);assert(array({...defaults,rows:10,columns:60}).modules.length<=1200);});
test('invalid imported values rejected',()=>{for(const x of [{rows:0},{tilt:NaN},{rows:1.2},{unknown:'value'},{boxV:2},{moduleW:Infinity}])assert.throws(()=>validate(x));});

test('unknown boxes hidden and specified positions rotate with module orientation',()=>{
 assert.equal(array(defaults).modules[0].boxes.length,0);
 for(const orientation of ['portrait','landscape']){
 const m=array({...defaults,rows:1,columns:1,layout:'fixed',azimuth:0,tilt:0,orientation,boxLayout:'one',boxU:.2,boxV:.8}).modules[0];
 const dx=m.boxes[0][0]-m.corners[0][0],dy=m.corners[0][1]-m.boxes[0][1];
 assert(Math.abs(dx-(orientation==='portrait'?defaults.moduleWidth*.2:defaults.moduleLength*.8))<1e-12);
 assert(Math.abs(dy-(orientation==='portrait'?defaults.moduleLength*.8:defaults.moduleWidth*.2))<1e-12);
 }
});

test('edge heights drive tilt and schematic supports without stretching modules',()=>{
 const s={...defaults,heightMode:'edges',height:4,upperHeight:5};const a=array(s);const z=a.modules.flatMap(m=>m.corners.map(p=>p[2]));assert(Math.abs(Math.min(...z)-4)<1e-10);assert(Math.abs(Math.max(...z)-5)<1e-10);assert(a.structure.some(m=>m.kind==='brace'));
 for(const m of a.structure.filter(m=>m.kind==='post')){assert.equal(m.points[0][2],0);assert(m.points[1][2]>=4&&m.points[1][2]<=5+1e-10);}
 for(const h of [.1,20]){const f=array({...s,height:h,upperHeight:h});assert.equal(f.settings.tilt,0);assert(f.modules.every(m=>m.corners.every(p=>p[2]===h)));}
 assert.throws(()=>array({...s,height:5,upperHeight:4}));assert.throws(()=>array({...s,rows:1,height:.1,upperHeight:20}));assert.throws(()=>array({...s,height:20.01,upperHeight:20.01}));
});
