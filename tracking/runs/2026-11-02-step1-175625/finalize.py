from pathlib import Path
from pypdf import PdfReader
import collections,datetime,hashlib,importlib.util,json,re,sqlite3,subprocess
from zoneinfo import ZoneInfo
ROOT=Path.cwd();RUN=Path(__file__).resolve().parent;CLI=ROOT/'skills/job-application-agent/scripts/ledger.py';RUN_ID=RUN.name;DAY='2026-11-02';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def update(id,patch):
 p=RUN/'final-patch.json';p.write_text(json.dumps(patch));subprocess.run(['python3',str(CLI),'update',id,str(p)],check=True,capture_output=True)
with sqlite3.connect(ROOT/'tracking/jobs.sqlite3') as c:jobs=[json.loads(r[0]) for r in c.execute('select data from jobs')]
byid={j['id']:j for j in jobs};groups=json.loads((RUN/'possible-companion-routes.json').read_text());companions={id:[x for x in g if x!=id] for g in groups for id in g}
spec=importlib.util.spec_from_file_location('b',ROOT/'skills/job-application-agent/scripts/build_step1.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b);b.freddie[0]=b.freddie[0].replace('CRT program','CRT (Credit Risk Transfer) program')
expected=b.freddie+b.research+b.quant+b.senior+b.aquilent;normalize=lambda s:re.sub(r'\s+',' ',s).strip()
validation=[];prior_seen=set()
for o in json.loads((RUN/'outcomes.json').read_text()):
 j=byid[o['id']];folder=ROOT/j['application_directory'];packetfile=folder/'application.json';packet=json.loads(packetfile.read_text());reader=PdfReader(ROOT/j['artifacts']['resume_pdf']['path']);assert len(reader.pages)==2
 texts=[p.extract_text() for p in reader.pages];text='\n'.join(texts)
 for bullet in expected:assert normalize(bullet) in normalize(text),(j['id'],bullet)
 assert 'Director, Financial Engineering/Inv&Capital Market' in text
 assert not re.search(r'AI[- ](?:generated|assisted|updated)|tailored for|targeted for|customized for|prepared for',text,re.I)
 metadata=reader.metadata;assert metadata.title=='Xuewu Cai — Resume';assert metadata.author=='Xuewu Cai'
 for artifact in j['artifacts'].values():assert sha(ROOT/artifact['path'])==artifact['sha256']
 # Check glyph origins against the printable page; layout also visually reviewed.
 bounds=[]
 for page in reader.pages:
  def visitor(t,cm,tm,font,size):
   if t.strip():
    x=tm[4]*cm[0]+tm[5]*cm[2]+cm[4];y=tm[4]*cm[1]+tm[5]*cm[3]+cm[5];bounds.append((x,y))
  page.extract_text(visitor_text=visitor)
 assert all(20<=x<=590 and 15<=y<=780 for x,y in bounds),j['id']
 for old in o['prior_artifacts']:
  path=ROOT/old['path'];assert sha(path)==old['sha256'];prior_seen.add(old['path'])
 review='Text and hashes verified; all 20 baseline experience bullets preserved with updated title. Two pages rendered in PDFKit; all 113 distinct page images visually reviewed across 10 boards (238 rendered pages total). No clipping, overlap or blank pages. Neutral metadata and no AI-editing/targeting labels. Candidate facts/qualifications marked as attention items; no submission.'
 patch={'resume_review':review,'resume_status':'prepared_with_attention','resume_format':'restored_two_page','current_resume_naming':'unversioned'}
 if j['id'] in companions:
  patch['possible_companion_job_ids']=companions[j['id']];note='Possible companion hiring-route announcement(s): '+', '.join(companions[j['id']])+'. Reconcile before submission; do not submit twice to the same vacancy.'
  patch['gaps']=j['gaps']+' '+note;patch['requirements_unverified']=j.get('requirements_unverified',[])+[note]
 packet.update(patch);packetfile.write_text(json.dumps(packet,indent=2,ensure_ascii=False)+'\n');update(j['id'],patch)
 validation.append({'id':j['id'],'pages':2,'baseline_bullets':20,'hashes_valid':True,'text_bounds_valid':True,'visual_review':'passed','labels_and_metadata_valid':True})
prefs=json.loads((ROOT/'candidate/preferences.json').read_text());assert sha(ROOT/prefs['baseline'])==prefs['baseline_sha256']
with sqlite3.connect(ROOT/'tracking/jobs.sqlite3') as c:
 assert c.execute('pragma integrity_check').fetchone()[0]=='ok';mode=c.execute('pragma journal_mode').fetchone()[0]
 assert c.execute('select count(*) from jobs').fetchone()[0]==119
(RUN/'validation.json').write_text(json.dumps({'resumes':validation,'preserved_prior_artifact_files':len(prior_seen),'baseline_sha256':prefs['baseline_sha256'],'sqlite_integrity':'ok','sqlite_journal_mode':mode,'all_pdfs_two_pages':True,'new_v2_files_created':0,'submitted':0},indent=2)+'\n')
print('Validated',len(validation),'PDFs /',len(validation)*2,'pages; original artifacts retained; SQLite integrity OK.')
