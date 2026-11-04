import subprocess,json,datetime
from pathlib import Path
r=Path(__file__).resolve().parent;root='https://bd.wd104.myworkdayjobsgov.com/wday/cxs/bd/frb';jobs=[]
def fetch(url,path,payload=None):
 cmd=['curl','-fLsS','--max-time','25',url]
 if payload is not None:cmd+=['-H','Content-Type: application/json','--data',json.dumps(payload)]
 cmd+=['-o',str(path)];x=subprocess.run(cmd,capture_output=True,text=True);a={'url':url,'payload':payload,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':x.returncode,'error':x.stderr}
 with (r/'frb-audit.jsonl').open('a') as f:f.write(json.dumps(a)+'\n')
 if x.returncode:print(a);return None
 return json.loads(path.read_text())
(r/'frb').mkdir(exist_ok=True)
offset=0
while True:
 p={'appliedFacets':{},'limit':20,'offset':offset,'searchText':''};d=fetch(root+'/jobs',r/'frb'/('page-'+str(offset)+'.json'),p)
 if d is None:break
 jobs+=d.get('jobPostings',[]);print('Page',offset,'total',d.get('total'),flush=True)
 offset+=20
 if offset>=d.get('total',0) or not d.get('jobPostings'):break
(r/'frb'/'unique.json').write_text(json.dumps(jobs,indent=2))
for j in jobs:
 req=j['bulletFields'][0];d=fetch(root+j['externalPath'],r/'frb'/(req+'.json'))
 if d is None:break
 print(req,j['title'],flush=True)
