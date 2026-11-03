import json,subprocess,sys,datetime,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
specs=json.loads(Path(sys.argv[1]).read_text())
for spec in specs:
 page=1
 while True:
  payload={**spec['payload'],'Page':page,'ResultsPerPage':100}
  file=ROOT/(spec['name']+'-p'+str(page)+'.json')
  result=subprocess.run(['curl','-fLsS','--max-time','30','https://www.usajobs.gov/Search/ExecuteSearch','-H','Content-Type: application/json','-H','User-Agent: Mozilla/5.0','--data',json.dumps(payload),'-o',str(file)],capture_output=True,text=True)
  audit={'name':spec['name'],'payload':payload,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':result.returncode}
  try:
   d=json.loads(file.read_text());audit.update(total=d.get('Total'),returned=len(d.get('Jobs',[])),pager=d.get('Pager'))
  except Exception as e:audit.update(error=result.stderr or str(e));d={}
  with (ROOT/'native-audit.jsonl').open('a') as f:f.write(json.dumps(audit)+'\n')
  print(json.dumps({k:v for k,v in audit.items() if k!='pager'}),flush=True)
  if spec.get('probe'):
   print('LOCATIONS', [x.get('LocationDisplay') for x in d.get('Jobs',[])[:10]],flush=True)
  if result.returncode or spec.get('probe') or not d.get('Pager',{}).get('HasNextPage'):break
  page+=1
