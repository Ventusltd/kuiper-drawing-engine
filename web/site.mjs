import {array,plant,validate} from './geometry.mjs';
export function siteModel(input){
 const s=validate(input),a=array(s),p=plant(s),points=a.modules.flatMap(m=>m.corners);
 const min=[0,1].map(i=>Math.min(...points.map(p=>p[i]))),max=[0,1].map(i=>Math.max(...points.map(p=>p[i])));
 const size=max.map((v,i)=>v-min[i]),tables=Math.ceil(p.modules/a.modules.length),columns=Math.ceil(Math.sqrt(tables)),rows=Math.ceil(tables/columns),pitch=size.map(v=>v+3);
 return {tables,columns,rows,pitch,size,min,max,modulesPerTable:a.modules.length,modules:p.modules,width:columns*pitch[0],height:rows*pitch[1],groupSize:Math.max(1,Math.ceil(tables/400))};
}
export function tableAt(site,index,edits={}){
 if(!Number.isInteger(index)||index<0||index>=site.tables)throw Error('Array index is outside the plant');
 const override=edits[index];const x=override?.x??(index%site.columns)*site.pitch[0],y=override?.y??Math.floor(index/site.columns)*site.pitch[1];
 return {index,x,y,modules:Math.min(site.modulesPerTable,site.modules-index*site.modulesPerTable)};
}
export function validatePlacements(raw,site){
 if(!Array.isArray(raw)||raw.length>10000)throw Error('Too many moved arrays');const result={};
 for(const row of raw){if(!row||Object.keys(row).some(k=>!['index','x','y'].includes(k))||!Number.isInteger(row.index)||row.index<0||row.index>=site.tables||!Number.isFinite(row.x)||!Number.isFinite(row.y)||Math.abs(row.x)>1e6||Math.abs(row.y)>1e6||row.index in result)throw Error('Invalid array position');result[row.index]={x:row.x,y:row.y};}
 return result;
}
