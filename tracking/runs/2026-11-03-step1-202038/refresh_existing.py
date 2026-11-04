import datetime,hashlib,json,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent;OLD=R.parent/'2026-11-02-step1-224109';CLI=Path('skills/job-application-agent/scripts/ledger.py');S=json.loads((R/'starting-state.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat();changes=[];validation=[]
for j in S['jobs']:
 ctl=j['control_number'];f=R/'announcements'/(ctl+'.json');raw=(R/'announcements'/(ctl+'.txt')).read_text();jp=json.loads(f.read_text());prev=json.loads((OLD/'announcements'/(ctl+'.json')).read_text());fields=[k for k in ['datePosted','validThrough','qualifications','educationRequirements','responsibilities','jobLocation'] if prev.get(k)!=jp.get(k)];close=jp.get('validThrough') or j.get('close_date');closed=bool(close and close<'2026-11-03') or bool(re.search(r'No longer accepting applications|This job is closed',raw,re.I));patch={'last_checked_at':now,'retrieved_at':now,'availability_check_source':str(f.with_suffix('.html')),'availability_check':'Closed: official announcement deadline has passed' if closed else 'Official announcement retrieved; date remains current','close_date':close,'discovery_window':['2026-09-03','2026-11-03']}
 if closed and j['status'] not in {'applied','submitting','submission_unknown','rejected','withdrawn'}:
  patch.update(status='closed',closure_reason='Official announcement closing date '+str(close)+' has passed, or announcement expressly states closure.',gaps=j.get('gaps','')+' Closed: official closing date '+str(close)+' has passed; do not start Step 2 unless agency verifies reopening.')
 p=R/'ledger-patch.json';p.write_text(json.dumps(patch));subprocess.run(['python3',str(CLI),'update',j['id'],str(p)],check=True,capture_output=True)
 for a in j['artifacts'].values():assert hashlib.sha256(Path(a['path']).read_bytes()).hexdigest()==a['sha256']
 if fields or closed:
  changes.append({'id':j['id'],'title':j['title'],'employer':j['employer'],'changed_fields':fields,'status':patch.get('status',j['status']),'close_date':close,'reason':patch.get('closure_reason','Official description changed')})
  folder=Path(j['application_directory']);packet=folder/'application.json';a=json.loads(packet.read_text());a.update(patch);packet.write_text(json.dumps(a,indent=2,ensure_ascii=False)+'\n')
  with (folder/'match.md').open('a') as w:w.write(('\n## Availability refresh — 2026-11-03\n\n'+patch['availability_check']+'. Evidence: '+str(f)+'. No application submitted.\n') if '## Availability refresh — 2026-11-03' not in (folder/'match.md').read_text() else '')
 if fields:
  with (Path(j['application_directory'])/'job.md').open('a') as w:w.write('\n## Official description refresh — '+now+'\n\n'+raw+'\n')
 validation.append({'id':j['id'],'reused_pdf_hash_valid':True,'changed_fields':fields,'status':patch.get('status',j['status'])})
(R/'changes.json').write_text(json.dumps(changes,indent=2));(R/'existing-validation.json').write_text(json.dumps(validation,indent=2));print('Existing refreshed',len(validation),'closed',sum(x['status']=='closed' for x in validation),'requirement changes',[x for x in changes if x['changed_fields']])
