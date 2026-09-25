// Local numeric interchange only. A private input produces a private output.
import fs from 'node:fs';
import {array,validate} from '../web/geometry.mjs';
import {siteModel} from '../web/site.mjs';
const [input,output]=process.argv.slice(2);
if(!input||!output)throw Error('Usage: node export_geometry_template.mjs settings.json output.json');
const settings=validate(JSON.parse(fs.readFileSync(input,'utf8')));
fs.writeFileSync(output,JSON.stringify({site:siteModel(settings),corners:array(settings).modules.map(m=>m.corners)}));
