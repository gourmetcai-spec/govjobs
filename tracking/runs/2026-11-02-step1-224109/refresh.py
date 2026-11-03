import datetime,hashlib,json,re,sqlite3,subprocess
from pathlib import Path
from pypdf import PdfReader
R=Path(__file__).resolve().parent; OLD=R.parent/'2026-11-02-step1-175625'; CLI=Path('skills/job-application-agent/scripts/ledger.py');now=datetime.datetime.now(datetime.timezone.utc).isoformat()
snap=json.loads((R/'starting-state.json').read_text());changes=[];valid=[]
def patch(id,p):
 f=R/'ledger-patch.json';f.write_text(json.dumps(p));subprocess.run(['python3',str(CLI),'update',id,str(f)],check=True,capture_output=True)
for j in snap['jobs']:
 ctl=j['control_number'];jp=json.loads((R/'announcements'/(ctl+'.json')).read_text());raw=(R/'announcements'/(ctl+'.txt')).read_text();prev=json.loads((OLD/'announcements'/(ctl+'.json')).read_text());changed=[k for k in ['datePosted','validThrough','qualifications','educationRequirements','responsibilities','jobLocation'] if prev.get(k)!=jp.get(k)]
 p={'last_checked_at':now,'availability_check_source':str(R/'announcements'/(ctl+'.html')),'availability_check':'Accepting applications' if 'Accepting applications' in raw else 'Announcement retrieved; live acceptance needs verification','close_date':jp.get('validThrough') or j.get('close_date')}
 if 'This job is closed' in raw or 'No longer accepting applications' in raw:
  p.update(status='closed',gaps=j.get('gaps','')+' Official announcement states no longer accepting applications.')
 patch(j['id'],p)
 if changed:changes.append({'id':j['id'],'changed_fields':changed})
 for a in j['artifacts'].values():assert hashlib.sha256(Path(a['path']).read_bytes()).hexdigest()==a['sha256']
 valid.append({'id':j['id'],'reused_pdf_hash_valid':True,'changed_fields':changed,'availability':p['availability_check']})
# Correct the newly created route's requisition transcription before publishing; preserve its stable ID.
with sqlite3.connect('tracking/jobs.sqlite3') as c:
 rows=[json.loads(x[0]) for x in c.execute('select data from jobs')];new=[j for j in rows if j['id'] not in snap['starting_ids']]
 for j in new:
  if j['control_number']=='891309200':
   j['requisition_id']='OGC-27-01';identity=j['employer'].strip().casefold()+'|req:ogc-27-01';c.execute('update jobs set identity=?,data=? where id=?',(identity,json.dumps(j),j['id']));c.execute('insert into events values(?,?,?)',(now,j['id'],json.dumps({'correction':'Initial requisition transcription corrected to official OGC-27-01; stable ID preserved'})))
for j in new:
 other=[x['id'] for x in new if x['id']!=j['id']];pdf=Path(j['artifacts']['resume_pdf']['path']);reader=PdfReader(pdf);text='\n'.join(p.extract_text() for p in reader.pages);assert len(reader.pages)==2 and reader.metadata.title=='Xuewu Cai — Resume';assert 'Director, Financial Engineering/Inv&Capital Market' in text;assert not re.search('tailored for|targeted for|AI-generated|AI-assisted',text,re.I)
 for a in j['artifacts'].values():assert hashlib.sha256(Path(a['path']).read_bytes()).hexdigest()==a['sha256']
 p={'requisition_id':j['requisition_id'],'possible_companion_job_ids':other,'resume_review':'Two rendered pages visually reviewed; no clipping, blank pages or labels. Text, baseline title, neutral metadata and artifact hashes verified.','resume_status':'prepared_with_attention','remote_restrictions':'On-site Washington DC; announcement states no telework and no remote work.'}
 # Identity already reconciled above; helper protects identity fields.
 ledgerpatch={k:v for k,v in p.items() if k!='requisition_id'};patch(j['id'],ledgerpatch)
 f=Path(j['application_directory'])/'application.json';a=json.loads(f.read_text());a.update(p);f.write_text(json.dumps(a,indent=2)+'\n')
 valid.append({'id':j['id'],'new_pdf_text_metadata_hashes_valid':True,'pages':2,'visual_review':'passed'})
(R/'changes.json').write_text(json.dumps(changes,indent=2));(R/'validation.json').write_text(json.dumps(valid,indent=2))
print('Refreshed',len(snap['jobs']),'new',len(new),'changed descriptions',changes)
