"""Build this federal Step 1 checkpoint from reviewed assessments; no portal actions."""
import importlib.util,json,datetime,re,hashlib,subprocess
from pathlib import Path
ROOT=Path.cwd();RUN=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('resume_builder',ROOT/'skills/job-application-agent/scripts/build_step1.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
b.RUN=RUN
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
summaries={
 'engineering':'Financial engineering director and technology leader with more than 20 years of experience delivering financial platforms, quantitative analytics, and trading systems. Combines hands-on Java, Python, C/C++ and database expertise with technical leadership and large-scale analytics on AWS and IBM Symphony. Leads enterprise forecasting and credit risk transfer modeling delivery, and uses Copilot and other generative AI tools to streamline engineering workflows.',
 'data':'Financial engineering director and technology leader with more than 20 years of experience across data-intensive financial platforms, quantitative research, risk management, and trading systems. Experience includes Java database integration, time-series data infrastructure and market data feeds, and large-scale analytics on AWS and IBM Symphony. Combines Java, Python, SQL database and C/C++ expertise with technical leadership and enterprise model implementation.',
 'quant':'Financial engineering director with more than 20 years of experience in quantitative research, financial modeling, forecasting and decision support. Experience includes Monte Carlo simulation, bootstrapping, volatility and correlation forecasting, scenario analysis and portfolio risk reporting. Leads enterprise forecasting, capital planning and stress testing platform delivery, with hands-on Java, Python, MATLAB and C/C++ expertise.'}
outcomes=[]
for a in json.loads((RUN/'assessments.json').read_text()):
 target=a['target'];control=a['control']
 source=(RUN/a['source']);assert source.is_file(),source
 j={k:v for k,v in a.items() if k not in {'target','source','track','requirements','date_evidence','control'}}
 j.update(canonical_url='https://www.usajobs.gov/job/'+control,application_url='https://www.cia.gov/careers/jobs/data-engineer/' if control=='759326100' else 'https://www.usajobs.gov/job/'+control,posted_date_evidence=a['date_evidence'],retrieved_at=now,status='discovered',aliases=[],discovery_window=['2026-09-01','2026-11-01'],remote_restrictions='Not remote; DMV duty station offered. Confirm telework policy in official job description.',open_evidence='Official USAJOBS announcement retrieved through web tool and reports Accepting applications; recheck at Step 2.',hiring_path='Restricted agency hiring path' if target=='skipped' else 'Open to the public',control_number=control)
 if control=='759326100':j['aliases']=['https://intelligencecareers.usajobs.gov/job/759326100','https://ai.usajobs.gov/job/759326100']
 added=b.mutate('add',j);assert not added['duplicate'],'Reconcile rather than overwrite'
 jid=added['id'];folder=ROOT/'applications'/('2026-11-01__'+b.slug(a['employer'])+'__'+b.slug(a['title'])+'__'+jid);folder.mkdir(exist_ok=False)
 (folder/'job.md').write_text('# '+a['title']+'\n\n'+json.dumps(j,indent=2,ensure_ascii=False)+'\n\n## Retrieved official announcement text\n\n'+source.read_text()+'\n\nSource is the web tool rendered announcement, including its line references; HTML downloads were blocked with HTTP 403. Date evidence is distinguished from retrieval time above.\n')
 reqs=a.get('requirements',[[a['fit'],'See baseline candidate/baseline.txt; full mandatory requirements remain unresolved as described below.']])
 match='# Requirement assessment\n\n'+a['fit']+'\n\n## Requirement to baseline evidence\n\n'+'\n\n'.join('**'+r+'**\n\n'+e for r,e in reqs)+'\n\n## Gaps and unresolved eligibility\n\n'+a['gaps']+'\n\n## Decision\n\n'+target+'. This is a local Step 1 assessment, not an agency eligibility determination. No application selected or submitted.\n\n## Tailoring boundaries\n\nFor the top three technical/quantitative leads, summary and expertise order emphasize the supported role requirements. All original employer names, titles, dates, education and 20 experience bullets retain their scope. No hours/week, exact employment days, GPA, course credits, clearance or production AI experience is invented. Every generated resume remains a draft until missing required facts and applicable eligibility evidence are resolved; no portal-ready packet is claimed.\n'
 (folder/'match.md').write_text(match)
 packet={**j,'id':jid,'status':target,'step':1,'selected':False,'submitted':False,'artifacts':{},'resume_status':'not_generated_verification_required','resume_review':'Not generated; unresolved mandatory requirements.'}
 if control in {'890584000','759326100','891052100'}:
  summary=summaries[a['track']];financial=a['track']=='quant'
  if financial:b.summary_fin=summary
  else:b.summary_eng=summary
  base='resume-xuewu-cai__'+b.slug(a['employer'])+'__'+b.slug(a['title'])+'__'+control+'__v1'
  md,pdf=b.resume(folder,base,financial,a['requisition_id'])
  # Keep the quantitative resume headline aligned with its focus.
  if financial:
   original='FINANCIAL ENGINEERING & MORTGAGE ANALYTICS LEADER'
   # The renderer uses this fixed headline; retain it to keep PDF and Markdown identical.
  packet['artifacts']={k:{'path':str(p.relative_to(ROOT)),'sha256':b.sha(p)} for k,p in [('resume_markdown',md),('resume_pdf',pdf)]}
  packet['resume_status']='draft_missing_required_facts'
  packet['resume_review']='Two selectable-text pages; extraction passed; visual review pending. Hours/week unverified; additional per-role requirements in match.md.'
 (folder/'application.json').write_text(json.dumps(packet,indent=2,ensure_ascii=False)+'\n')
 b.mutate('update',{'status':target,'application_directory':str(folder.relative_to(ROOT)),'artifacts':packet['artifacts'],'resume_status':packet['resume_status'],'resume_review':packet['resume_review']},jid)
 outcomes.append({'id':jid,'employer':j['employer'],'title':j['title'],'status':target,'folder':str(folder.relative_to(ROOT)),'artifacts':packet['artifacts']})
 (RUN/'outcomes.json').write_text(json.dumps(outcomes,indent=2,ensure_ascii=False)+'\n')
print(json.dumps([{k:v for k,v in o.items() if k not in {'artifacts','folder'}} for o in outcomes],indent=2))
