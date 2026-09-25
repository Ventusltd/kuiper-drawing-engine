// Original geometry. Coordinates: east (x), north (y), up (z); metres.
export const defaults=Object.freeze({rows:5,columns:6,orientation:'portrait',layout:'east-west',azimuth:90,tilt:12,height:1,gap:.02,ridgeGap:.3,moduleLength:2.4,moduleWidth:1.2,moduleW:650,series:30,stringsPerInverter:24,invertersPerBlock:24,targetMW:1000,boxLayout:'unknown',boxU:.5,boxV:.5,heightMode:'tilt',upperHeight:5,supportBays:2,structure:'braced'});
export function validate(input){
 if(!input||typeof input!=='object'||Array.isArray(input))throw Error('Expected numeric layout settings');
 for(const k of Object.keys(input))if(!Object.hasOwn(defaults,k))throw Error('Unknown setting: '+k);
 const s={...defaults,...input};
 const limits={rows:[1,10],columns:[1,60],azimuth:[0,360],tilt:[0,60],height:[.1,20],upperHeight:[.1,20],supportBays:[1,20],gap:[0,.2],ridgeGap:[0,3],moduleLength:[.1,4],moduleWidth:[.1,3],moduleW:[1,1500],series:[1,60],stringsPerInverter:[1,100],invertersPerBlock:[1,100],targetMW:[.001,10000],boxU:[0,1],boxV:[0,1]};
 for(const[k,[lo,hi]]of Object.entries(limits))if(typeof s[k]!=='number'||!Number.isFinite(s[k])||s[k]<lo||s[k]>hi)throw Error(k+' is outside its supported range');
 for(const k of ['supportBays','rows','columns','series','stringsPerInverter','invertersPerBlock'])if(!Number.isInteger(s[k]))throw Error(k+' must be a whole number');
 if(!['portrait','landscape'].includes(s.orientation)||!['fixed','east-west'].includes(s.layout)||!['unknown','one','two','three'].includes(s.boxLayout))throw Error('Unknown layout');
 if(!['tilt','edges'].includes(s.heightMode)||!['none','posts','braced'].includes(s.structure))throw Error('Unknown height or support mode');
 const run=s.rows*(s.orientation==='portrait'?s.moduleLength:s.moduleWidth)+(s.rows-1)*s.gap;
 if(s.heightMode==='edges'){const rise=s.upperHeight-s.height;if(rise<0||rise>run*Math.sin(Math.PI/3)+1e-10)throw Error('Upper edge must be above lower edge and reachable with this table at 0?60 degrees');s.tilt=Math.asin(Math.min(1,rise/run))*180/Math.PI;}else s.upperHeight=s.height+run*Math.sin(s.tilt*Math.PI/180);
 if(s.upperHeight>20+1e-10)throw Error('Upper edge exceeds 20 m; reduce tilt or lower edge');
 return s;
}
const rad=x=>x*Math.PI/180;
export function basis(azimuth,tilt){const a=rad(azimuth),t=rad(tilt);return {u:[Math.cos(a),-Math.sin(a),0],v:[-Math.sin(a)*Math.cos(t),-Math.cos(a)*Math.cos(t),Math.sin(t)],normal:[Math.sin(a)*Math.sin(t),Math.cos(a)*Math.sin(t),Math.cos(t)]};}
export function point(origin,u,v,x,y){return origin.map((p,i)=>p+u[i]*x+v[i]*y);}
export function array(supplied){
 const s=validate(supplied),length=s.orientation==='portrait'?s.moduleLength:s.moduleWidth,width=s.orientation==='portrait'?s.moduleWidth:s.moduleLength;
 const run=s.rows*length+(s.rows-1)*s.gap,span=s.columns*width+(s.columns-1)*s.gap;
 const directions=s.layout==='east-west'?[s.azimuth,(s.azimuth+180)%360]:[s.azimuth];const modules=[],structure=[];
 for(const [wing,az]of directions.entries()){
  const {u,v,normal}=basis(az,s.tilt),a=rad(az),projected=run*Math.cos(rad(s.tilt));
  const origin=s.layout==='east-west'?[Math.sin(a)*(projected+s.ridgeGap/2),Math.cos(a)*(projected+s.ridgeGap/2),s.height]:[0,0,s.height];
  if(s.structure!=='none'){
   const low=[],high=[],ground=p=>[p[0],p[1],0],add=(kind,a,b)=>structure.push({kind,wing,points:[a,b]});
   for(let bay=0;bay<=s.supportBays;bay++){const x=-span/2+bay*span/s.supportBays,l=point(origin,u,v,x,0),h=point(origin,u,v,x,run);low.push(l);high.push(h);add('post',ground(l),l);add('post',ground(h),h);add('rafter',l,h);}
   add('rail',low[0],low.at(-1));add('rail',high[0],high.at(-1));
   if(s.structure==='braced')for(let bay=0;bay<s.supportBays;bay++)for(const line of [low,high]){add('brace',ground(line[bay]),line[bay+1]);add('brace',ground(line[bay+1]),line[bay]);}
  }
  for(let row=0;row<s.rows;row++)for(let col=0;col<s.columns;col++){
   const x=col*(width+s.gap)-span/2,y=row*(length+s.gap);
   const corners=[[0,0],[width,0],[width,length],[0,length]].map(([dx,dy])=>point(origin,u,v,x+dx,y+dy));
   const count={unknown:0,one:1,two:2,three:3}[s.boxLayout];
   // Normalised box positions are user settings, not manufacturer-approved coordinates.
   const boxes=Array.from({length:count},(_,k)=>{const across=count===1?s.boxU:Math.max(0,Math.min(1,s.boxU+(k-(count-1)/2)*.28));const dx=s.orientation==='portrait'?width*across:width*s.boxV,dy=s.orientation==='portrait'?length*s.boxV:length*across;return point(origin,u,v,x+dx,y+dy);});
   modules.push({id:modules.length+1,wing,row:row+1,column:col+1,corners,boxes,normal});
  }
 }
 return {modules,structure,span,run,rise:run*Math.sin(rad(s.tilt)),projectedRun:run*Math.cos(rad(s.tilt)),height:s.height,settings:s};
}
export function plant(supplied){
 const s=validate(supplied),strings=Math.ceil(s.targetMW*1e6/(s.moduleW*s.series)),modules=strings*s.series,inverters=Math.ceil(strings/s.stringsPerInverter),blocks=Math.ceil(inverters/s.invertersPerBlock);
 return {targetDCMW:s.targetMW,actualDCMW:modules*s.moduleW/1e6,modules,strings,inverters,blocks,lastInverterStrings:strings-(inverters-1)*s.stringsPerInverter,lastBlockInverters:inverters-(blocks-1)*s.invertersPerBlock};
}
