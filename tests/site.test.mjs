import test from 'node:test';import assert from 'node:assert/strict';import {defaults,plant} from '../web/geometry.mjs';import {siteModel,tableAt,validatePlacements,overlapsFor} from '../web/site.mjs';
test('every 1GW module belongs to exactly one virtual array',()=>{const s=siteModel(defaults);let count=0;for(let i=0;i<s.tables;i++)count+=tableAt(s,i).modules;assert.equal(count,plant(defaults).modules);assert(tableAt(s,s.tables-1).modules>0);assert.equal(tableAt(s,s.tables-1).modules,s.modules-(s.tables-1)*s.modulesPerTable);});
test('regular footprints do not overlap and edits round-trip',()=>{const s=siteModel(defaults);assert(s.pitch[0]>s.size[0]);assert(s.pitch[1]>s.size[1]);const e=validatePlacements([{index:10,x:100,y:200}],s);assert.deepEqual(tableAt(s,10,e),{index:10,x:100,y:200,modules:60});assert.throws(()=>validatePlacements([{index:0,x:0,y:0},{index:0,x:1,y:1}],s));assert.throws(()=>validatePlacements([{index:s.tables,x:0,y:0}],s));});

test('overlap lookup matches exhaustive footprint checks after array moves',()=>{
 const site=siteModel({...defaults,targetMW:.1}),edits={0:{x:siteModel({...defaults,targetMW:.1}).pitch[0],y:0},2:{x:-100,y:0}};
 for(let i=0;i<site.tables;i++){const a=tableAt(site,i,edits),expected=[];
 for(let j=0;j<site.tables;j++){if(i===j)continue;const b=tableAt(site,j,edits);if(Math.min(a.x+site.size[0],b.x+site.size[0])-Math.max(a.x,b.x)>1e-9&&Math.min(a.y+site.size[1],b.y+site.size[1])-Math.max(a.y,b.y)>1e-9)expected.push(j);}
 assert.deepEqual(overlapsFor(site,i,edits).sort((a,b)=>a-b),expected);}
 assert(overlapsFor(site,0,edits).includes(1));
});
