"""Assess official announcements, deduplicate and prepare local resumes only."""
import datetime,hashlib,importlib.util,inspect,json,re,subprocess,sqlite3
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path.cwd();RUN=Path(__file__).resolve().parent;CLI=ROOT/'skills/job-application-agent/scripts/ledger.py';NOW=datetime.datetime.now(datetime.timezone.utc).isoformat();TODAY='2026-11-02'
class Plain(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_starttag(self,t,a):
  if t in ('p','li','br','div'):self.parts.append('\n')
 def handle_data(self,d):self.parts.append(d)
def plain(s):
 p=Plain();p.feed(s);return re.sub(r'\n\s*\n+','\n',''.join(p.parts)).strip()
def clean(s):return re.sub(r'\s+',' ',plain(s)).strip()
def slug(s,n=60):return re.sub('[^a-z0-9]+','-',s.lower()).strip('-')[:n].rstrip('-')
def date(s):
 if not s:return None
 try:return datetime.datetime.strptime(s[:10],'%m/%d/%Y').date().isoformat()
 except ValueError:return s[:10]
def ledger(cmd,data=None,id=None):
 if data is None:return json.loads(subprocess.check_output(['python3',str(CLI),cmd],text=True))
 f=RUN/'ledger-input.json';f.write_text(json.dumps(data));return json.loads(subprocess.check_output(['python3',str(CLI),cmd,*([id] if id else []),str(f)],text=True))
spec=importlib.util.spec_from_file_location('baseline_builder',ROOT/'skills/job-application-agent/scripts/build_step1.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
source=inspect.getsource(b.resume).replace('### Freddie Mac | Director, Financial Engineering','### Freddie Mac | Director, Financial Engineering/Inv&Capital Market').replace("title='Xuewu Cai - '+req", "title='Xuewu Cai — Resume'").replace('order=[3,0,1,2,4,7,6,5] if financial else [1,3,4,5,0,2,6,7]','order=resume_order')
exec(source,b.__dict__)
b.freddie[0]=b.freddie[0].replace('CRT program','CRT (Credit Risk Transfer) program')
native={j['DocumentID']:j for j in json.loads((RUN/'native-unique.json').read_text())};existing=ledger('list');starting={j['id'] for j in existing};by_control={j.get('control_number',j['canonical_url'].rsplit('/',1)[-1]):j for j in existing};assert not any(j['status'] in {'applied','submitting','submission_unknown','approved'} for j in existing)
cards=json.loads((RUN/'review-cards.json').read_text());screen={r['control']:r['screen_out_reason'] for r in cards}
# Recent-graduate eligibility is an uncertainty, not proof of a mismatch.
screen['889011200']=None
controls={'891309200','891309300'}
all_outcomes=[];screened=[]
themes=[('forecast','enterprise forecasting and scenario analysis'),('capital','capital planning and transaction economics'),('risk','portfolio risk analytics'),('monte carlo','Monte Carlo simulation and statistical research'),('java','Java trading platforms and database integration'),('python','Python and quantitative software engineering'),('cloud','large-scale analytics on AWS and IBM Symphony'),('data','market-data infrastructure and analytical reporting'),('software','enterprise software and financial model implementation'),('ai','documented use of generative AI tools in engineering workflows')]
flags=[('CPIC','Federal capital planning/CPIC experience'),('FITARA','FITARA experience'),('OMB','OMB/federal budget procedures'),('SharePoint','SharePoint application/administration experience'),('Power Platform','Power Platform experience'),('TBM','Technology Business Management experience'),('NIST','NIST/security-control experience'),('CISSP','stated security certification requirements'),('disaster recovery','disaster-recovery evaluation experience'),('commissioned','examiner commission eligibility'),('21 semester','economics coursework/credit requirements'),('24 semester','qualifying coursework and calculus credits'),('GPA','required GPA evidence'),('accounting','required accounting background/coursework'),('OCR','document extraction/OCR experience'),('ETL','ETL/data-workflow experience'),('machine learning','production ML/AI scope'),('production grade','production AI engineering experience'),('SAP','SAP experience'),('PL/SQL','PL/SQL experience'),('.NET','.NET experience'),('Microsoft Dynamics','Microsoft Dynamics experience'),('SQL Server Reporting','SQL Server Reporting experience'),('Secret','security-clearance eligibility')]
for control in sorted(controls,key=lambda id:(date(json.loads((RUN/'announcements'/(id+'.json')).read_text()).get('validThrough')) or '9999',id)):
 old=by_control.get(control);n=native.get(control,{});jp=json.loads((RUN/'announcements'/(control+'.json')).read_text());raw=(RUN/'announcements'/(control+'.txt')).read_text();qual=clean(jp.get('qualifications',''));duties=clean(jp.get('responsibilities',''));edu=clean(jp.get('educationRequirements',''));description=clean(jp.get('description',''));posted=date(jp.get('datePosted'));close=date(jp.get('validThrough'))
 if not old and (not posted or posted<'2026-09-02' or posted>TODAY or (close and close<TODAY)):
  screened.append({'control':control,'reason':'Official dates outside new-discovery window or already closed','posted':posted,'close':close});continue
 locs=[(x.get('address',{}).get('addressLocality','')+', '+x.get('address',{}).get('addressRegion','').strip()) for x in jp.get('jobLocation',[])];dmv=[x for x in locs if x.rsplit(', ',1)[-1] in {'MD','VA','DC'}]
 if locs and not dmv:screened.append({'control':control,'reason':'Official locations do not offer DC/MD/VA'});continue
 title=jp['title'].strip();employer=old['employer'] if old else n.get('Agency') or jp.get('hiringOrganization');req=old['requisition_id'] if old else n.get('PositionID') or ('OGC-27-02-DE' if control=='891309300' else 'OGC-27-01-MP')
 qtext=(qual+' '+edu).lower();jobtext=(duties+' '+qual).lower();financial=bool(re.search(r'financial|finance|economist|capital markets',title,re.I));track='finance' if financial else 'quant' if re.search(r'research analyst|data scien',title,re.I) else 'engineering'
 pathcodes=[x['Code'] for x in n.get('HiringPath',[])];hiring=[x['SearchDisplay'] for x in n.get('HiringPath',[])]
 if not hiring:
  m=re.search(r'This job is open to(.*?)Duties',raw,re.S);hiring=[re.sub(r'\s+',' ',m.group(1)).strip()[:1000]] if m else ['See official announcement']
 attention=['Mandatory selective placement factor: extensive experience coordinating congressional committee interactions in banking, financial services, housing or oversight is unverified. Confirm 52 weeks at EL/GS-14 equivalent and all specialized-experience clauses. On-site Washington DC; no telework.']
 if pathcodes and 'public' not in pathcodes:attention.append('Hiring-path eligibility unverified: '+', '.join(hiring)+'. Confirm qualifying status before application; absence from baseline is not proof of ineligibility.')
 for token,label in flags:
  if re.search(r'\b'+re.escape(token)+r'\b',qtext,re.I):attention.append('Verify '+label+' against the exact qualification clause; not established by the baseline alone.')
 if 'recent graduate' in title.lower() or 'graduates' in pathcodes:attention.append('Confirm graduate/student hiring-path dates and eligibility; degree completion dates are not in the baseline.')
 if not attention:attention.append('Confirm the announcement-specific specialized experience, grade-equivalent scope and mandatory conditions against your actual work history.')
 attention.append('Hours worked per week and exact employment days, when required, need your confirmation; do not invent them.')
 if 'own words' in raw and ('artificial intelligence' in raw.lower()):attention.append('Any own-words/no-AI essay certification must be answered personally; no such essays drafted.')
 if control=='759326100':attention.append('Official September 1 posting date is confirmed. This existing record is retained although it predates today’s September 2 new-discovery cutoff. GPA and CIA screening requirements remain unverified.')
 if track=='finance':fit='Financial forecasting, capital/ROE, quantitative risk and engineering leadership overlap; federal budget/accounting/policy specialties remain attention items.'
 elif track=='quant':fit='Mathematics/CS education, Monte Carlo/statistical research, forecasting and decision-support modeling overlap; specialized domain/AI requirements need confirmation.'
 else:fit='Mortgage finance leadership, cross-team delivery and regulatory reporting overlap with financial oversight coordination; congressional engagement and federal audit workflow expertise remain unverified.'
 timezone='America/New_York' if re.search(r'(?:11:59|midnight|23:59).{0,90}(?:Eastern|\bET\b|\bEST\b)|Eastern.{0,60}(?:11:59|midnight)',raw,re.I) else None
 deadline_time='23:59' if timezone and '11:59' in raw else None
 early=re.findall(r'(?:This job will close when[^\n]{0,240}|first \d+ applications[^\n]{0,200}|may close[^\n]{0,180})',raw,re.I)
 cutoff='Weekly Friday cutoffs; standing register through closing date' if control in {'883691200','883693300','883695200'} else None
 status='closed' if close and close<TODAY else 'eligible' if control=='890584000' else 'needs_verification'
 record=dict(title=title,requisition_id=req,canonical_url='https://www.usajobs.gov/job/'+control,application_url='https://www.usajobs.gov/job/'+control,posted_date=posted,posted_date_evidence='Official announcement JobPosting.datePosted; corroborated by native search PositionStartDate where listed.',close_date=close,deadline_timezone=timezone,deadline_time=deadline_time,deadline_source='https://www.usajobs.gov/job/'+control,deadline_verified=True if close else False,early_closure_conditions=list(dict.fromkeys(early)),rolling_cutoff=cutoff,location='; '.join(dmv) if dmv else n.get('LocationDisplay') or old.get('location'),remote_restrictions='Offered DMV work location; verify telework/attendance and screening conditions in announcement.',salary=n.get('SalaryDisplay') or old.get('salary') if old else n.get('SalaryDisplay'),retrieved_at=NOW,control_number=control,fit=fit,gaps=' '.join(attention),requirements_confirmed_unmet=[],requirements_unverified=attention,preferred_requirements_note='See official qualifications/education sections; missing evidence does not establish an unmet requirement.',hiring_paths=hiring,open_evidence='Official announcement downloaded successfully; validThrough and native open-status evidence retained.',discovery_window=['2026-09-02','2026-11-02'])
 if old:
  id=old['id'];patch={k:v for k,v in record.items() if k not in {'requisition_id','canonical_url'}};patch['status']=status
  ledger('update',patch,id);job={**old,**patch}
 else:
  job={**record,'employer':employer,'status':'discovered','aliases':[]};added=ledger('add',job);id=added['id'];assert not added['duplicate'],'Reconcile unexpected duplicate rather than overwrite'
  folder=ROOT/'applications'/('2026-11-02__'+slug(employer,40)+'__'+slug(title,64)+'__'+id);folder.mkdir(exist_ok=False);job.update(id=id,application_directory=str(folder.relative_to(ROOT)),status=status);ledger('update',{'status':status,'application_directory':job['application_directory']},id)
 folder=ROOT/job['application_directory'];packetfile=folder/'application.json';prior=json.loads(packetfile.read_text()) if packetfile.exists() else None
 previous=[{'path':a['path'],'sha256':a['sha256']} for a in (prior or {}).get('artifacts',{}).values() if a.get('path')]
 (folder/'job.md').write_text('# '+title+'\n\n'+json.dumps(record,indent=2,ensure_ascii=False)+'\n\n## Summary\n\n'+plain(jp.get('description',''))+'\n\n## Duties\n\n'+plain(jp.get('responsibilities',''))+'\n\n## Qualifications\n\n'+plain(jp.get('qualifications',''))+'\n\n## Education\n\n'+plain(jp.get('educationRequirements',''))+'\n\n## Full rendered official announcement\n\n'+raw.rstrip()+'\n')
 # Tailor only through supported themes, terminology and ordering, never by copying unsupported requirements.
 selected=[label for token,label in themes if token in jobtext][:3]
 if not selected:selected=['financial engineering and enterprise analytics','technical leadership and multi-project delivery']
 summary='Financial engineering director and technology leader with more than 20 years across mortgage finance, quantitative research, risk management and trading systems. Experience includes '+', '.join(selected)+'. Combines hands-on Java, Python, MATLAB and C/C++ expertise with large-scale analytics on AWS and IBM Symphony and documented financial model implementation.'
 b.summary_fin=summary;b.summary_eng=summary
 words=set(re.findall(r'[a-z]{3,}',jobtext));order=sorted(range(len(b.freddie)),key=lambda i:(-len(words&set(re.findall(r'[a-z]{3,}',b.freddie[i].lower()))),i));b.resume_order=order
 base='resume-xuewu-cai__'+slug(employer,40)+'__'+slug(title,64)+'__'+slug(control,16);md=folder/(base+'.md');pdf=folder/(base+'.pdf')
 if md.exists() or pdf.exists():raise RuntimeError('Current unversioned file already exists; archive and compare before regeneration')
 md,pdf=b.resume(folder,base,financial,req)
 artifacts={k:{'path':str(path.relative_to(ROOT)),'sha256':b.sha(path)} for k,path in [('resume_markdown',md),('resume_pdf',pdf)]}
 versions=(prior or {}).get('artifact_versions',[])
 if prior and prior.get('artifacts') and not any(v.get('artifacts')==prior['artifacts'] for v in versions):versions.append({'revision_id':'prior-current','artifacts':prior['artifacts'],'resume_review':prior.get('resume_review')})
 versions.append({'revision_id':NOW,'artifacts':artifacts,'baseline_sha256':hashlib.sha256((ROOT/'resume-xuewu.cai.pdf').read_bytes()).hexdigest()})
 packet={**(prior or {}),**job,'status':status,'step':1,'selected':False,'submitted':False,'artifacts':artifacts,'artifact_versions':versions,'resume_status':'prepared_with_attention','resume_review':'Two selectable-text pages; restored format and baseline title. Visual review pending; missing candidate answers remain explicit.','required_answers_pending':attention,'confirmed_unmet_requirements':[],'qualifications_verified':False,'baseline_sha256':hashlib.sha256((ROOT/'resume-xuewu.cai.pdf').read_bytes()).hexdigest()}
 packet.pop('format_reference',None);packet.pop('resume_version',None);packetfile.write_text(json.dumps(packet,indent=2,ensure_ascii=False)+'\n')
 match='\n## Step 1 refresh and local preparation — 2026-11-02\n\n'+fit+'\n\n### Supported candidate evidence\n\nFreddie Mac Director, Financial Engineering/Inv&Capital Market (May 2014–present): CRT modeling, enterprise forecasting, CECL/capital planning/DFAST, portfolio risk and transaction economics. Campbell: Java/Portware/FIX trading platforms, market data/database integration, Monte Carlo/bootstrapping, volatility/correlation forecasting and SEC/CFTC/OPERA reporting. Aquilent: Java/Linux integration and visualization portals. Degrees and factual scope preserved from the updated baseline.\n\n### Requirements needing confirmation\n\n'+'\n'.join('- '+x for x in attention)+'\n\n### Confirmed unmet requirements\n\nNone established from affirmative user evidence. Unknown experience/credentials remain unverified. This is preparation, not a verified agency eligibility determination.\n\n### Exact qualification and education clauses\n\n'+plain(jp.get('qualifications',''))+'\n\n'+plain(jp.get('educationRequirements',''))+'\n\n### Preparation and tailoring\n\nGenerated one current unversioned Markdown/PDF pair in the restored two-page layout. Summary themes and Freddie Mac bullet order emphasize only baseline-supported concepts present in this announcement. No requirement is copied as a new claim. Preserved prior PDF versions and approval evidence; no new v2/compact alternative created. Neutral PDF title/author; no editing or targeting labels. Candidate hours/week, exact days, GPA/transcripts, hiring status and declarations remain pending where required. No application selected, uploaded or submitted.\n'
 with (folder/'match.md').open('a') as f:f.write(match)
 ledger('update',{'artifacts':artifacts,'artifact_versions':versions,'resume_status':packet['resume_status'],'resume_review':packet['resume_review'],'baseline_sha256':packet['baseline_sha256'],'qualifications_verified':False},id)
 all_outcomes.append({'id':id,'control':control,'new':id not in starting,'employer':employer,'title':title,'location':job['location'],'close_date':close,'status':status,'track':track,'artifacts':artifacts,'attention':attention,'prior_artifacts':previous})
 (RUN/'outcomes.json').write_text(json.dumps(all_outcomes,indent=2,ensure_ascii=False)+'\n')
for r in cards:
 if screen[r['control']]:screened.append({'control':r['control'],'title':r['title'],'reason':screen[r['control']]})
(RUN/'screened-candidates.json').write_text(json.dumps(screened,indent=2)+'\n')
print(json.dumps({'prepared':len(all_outcomes),'new':sum(o['new'] for o in all_outcomes),'existing':sum(not o['new'] for o in all_outcomes),'screened':len(screened)},indent=2))
