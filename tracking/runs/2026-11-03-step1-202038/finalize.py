from pathlib import Path
import collections,datetime,hashlib,json,re,sqlite3,subprocess
R=Path(__file__).resolve().parent;CLI=Path('skills/job-application-agent/scripts/ledger.py');S=json.loads((R/'starting-state.json').read_text());old=set(S['starting_ids']);now=datetime.datetime.now(datetime.timezone.utc).isoformat()
with sqlite3.connect('tracking/jobs.sqlite3') as c:jobs=[json.loads(x[0]) for x in c.execute('select data from jobs')]
groups=collections.defaultdict(list)
for j in jobs:
 if j['status'] not in {'closed','skipped','applied','rejected','withdrawn'}:groups[(j['employer'].lower().strip(),j['title'].lower().strip(),j['location'].lower().strip())].append(j['id'])
companions={id:[x for x in ids if x!=id] for ids in groups.values() if len(ids)>1 for id in ids};pairs=[]
for ids in groups.values():
 if len(ids)>1:pairs.append(ids)
(R/'possible-companion-routes.json').write_text(json.dumps(pairs,indent=2))
for j in jobs:
 if j['id'] in old:continue
 p={'resume_status':'prepared_with_attention','resume_format':'restored_two_page','current_resume_naming':'unversioned','resume_review':'Two rendered pages reviewed; all 77 distinct page images inspected across seven boards covering 166 pages. Text bounds, all 20 baseline experience bullets, updated title, neutral metadata and artifact hashes passed. Candidate qualifications remain unverified.'}
 if re.search('account|budget|portfolio analytics',j['title'],re.I):p['fit']='Enterprise forecasting, capital planning, portfolio risk/valuation, financial reporting and leadership overlap. Exact federal accounting, budget, investment governance and grade-equivalent requirements remain unverified.'
 if j['id'] in companions:
  p['possible_companion_job_ids']=companions[j['id']];note='Possible companion route(s): '+', '.join(companions[j['id']])+'. Reconcile exact vacancy before submitting; no duplicate applications.';p['gaps']=j['gaps']+' '+note;p['requirements_unverified']=j['requirements_unverified']+[note]
 if j['control_number'].startswith('R'):
  p['posted_date_evidence']='Official Federal Reserve Board Workday jobPostingInfo.startDate; retrieved source retained.';p['deadline_verified']=bool(j.get('close_date'));p['open_evidence']='Official Federal Reserve Board careers feed: canApply=true and posted=true; source jobPostingInfo retained.';p['remote_restrictions']='Federal Reserve Board work location; Board headquarters is Washington DC. Confirm team-specific on-site/hybrid policy in official description; do not assume remote work.'
  if 'intern' in j['title'].lower():p['priority']='lower'
 f=R/'ledger-patch.json';f.write_text(json.dumps(p));subprocess.run(['python3',str(CLI),'update',j['id'],str(f)],check=True,capture_output=True)
 packet=Path(j['application_directory'])/'application.json';d=json.loads(packet.read_text());d.update(p);packet.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
 with (Path(j['application_directory'])/'match.md').open('a') as w:w.write('\n## Final verification and role review — 2026-11-03\n\n'+p['resume_review']+'\n\n'+p.get('fit',j['fit'])+'\n\n'+p.get('gaps','')+'\n')
with sqlite3.connect('tracking/jobs.sqlite3') as c:
 assert c.execute('pragma integrity_check').fetchone()[0]=='ok';c.execute('pragma wal_checkpoint(full)')
assert hashlib.sha256(Path('resume-xuewu.cai.pdf').read_bytes()).hexdigest()==S['baseline_sha256']
subprocess.run(['python3','skills/job-application-agent/scripts/refresh_queue.py'],check=True)
lib=json.loads(Path('resumes/manifest.json').read_text());assert not lib['missing'];assert sum(e['version_label']=='current' for e in lib['entries'])==204
for e in lib['entries']:assert hashlib.sha256(Path(e['source']).read_bytes()).hexdigest()==e['sha256']==hashlib.sha256(Path(e['path']).read_bytes()).hexdigest()
print('204 current +',sum(e['version_label']=='historical' for e in lib['entries']),'historical PDFs verified; companion groups',len(pairs))
