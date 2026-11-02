#!/usr/bin/env python3
"""One-time builder for the initial 2026-11-01 discovery checkpoint.

Uses the ledger CLI for all job mutations; never accesses application forms.
Do not rerun against a populated ledger: reconcile existing IDs with ledger.py.
"""
import datetime, hashlib, html, json, re, subprocess
from pathlib import Path
from html.parser import HTMLParser
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[3]
RUN=ROOT/'tracking/runs/2026-11-01-step1'
CLI=ROOT/'skills/job-application-agent/scripts/ledger.py'
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
class Plain(HTMLParser):
 def __init__(self): super().__init__(); self.parts=[]
 def handle_starttag(self,t,a):
  if t in ('p','li','h2','br'):self.parts.append('\n')
 def handle_data(self,d):self.parts.append(d)
def plain(s):
 p=Plain();p.feed(s);return re.sub(r'\n\s*\n+', '\n\n',''.join(p.parts)).strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ledger(command,*args):
 return json.loads(subprocess.check_output(['python3',str(CLI),command,*map(str,args)],cwd=ROOT,text=True))
def mutate(command,data,jobid=None):
 p=RUN/'ledger-input.json';p.write_text(json.dumps(data,indent=2))
 out=ledger(command,*([jobid] if jobid else []),p);p.unlink();return out
def slug(s):return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')

freddie=[
'Lead financial engineering projects supporting STACR bond issuance and ACIS reinsurance within Freddie Mac’s CRT program, which protects more than $1.6 trillion in mortgage loans against credit losses.',
'Direct development of modeling tools that combine prepayment and default models, large-scale computing on AWS and IBM Symphony, and Intex valuation analytics to assess bond performance and transaction economics, including return on committed capital.',
'Oversee portfolio execution and risk analytics covering duration, convexity, option-adjusted spread (OAS), key rate durations (KRDs), capital benefits, post-transaction capital, and return on equity across the CRT portfolio.',
'Own an enterprise forecasting platform for income statements, balance sheets, and CECL estimates, supporting annual business planning, risk appetite assessment, capital planning, and DFAST stress testing.',
'Delivered deal memorandum, capital, economics, and ROE analytics for new RPL and synthetic structures, using Copilot and harness engineering to support delivery.',
'Use generative AI tools, including Copilot, extensively to streamline engineering workflows and improve delivery efficiency.',
'Manage the transition from LIBOR to SOFR within CRT modeling tools and analytics.',
'Apply hands-on expertise in STACR, senior/subordinate structures, ACIS reinsurance, and IntexCalc, DealMaker, and CDI structures to support valuation and model implementation.'
]
research=[
'Developed volatility and correlation forecasting models in MATLAB using daily, intraday, implied volatility, and tick data.',
'Applied statistical methods, Monte Carlo simulation, and bootstrapping to investigate indicators of market stress, portfolio drawdowns, regime changes, and correlation breakdowns using MATLAB, C/C++, and Java.',
'Designed and implemented internal risk reporting covering factor analysis, scenarios, stress tests, duration, and margin to support Investment Committee decisions.',
'Produced regulatory and industry reporting for SEC, CFTC, and OPERA requirements, as well as marketing and compliance analyses, using MATLAB, Java/StyleReport, and Panopticon.'
]
quant=[
'Led development of a Java-based intraday cash equity trading system using the Caché database; built time-series data infrastructure and market data feeds in MFC/C++.',
'Designed a Java connectivity layer that unified MATLAB access to production databases, including Oracle, SQL Server, Caché, and QADirect.',
'Built an FX options pricing, simulation, and risk engine using Visual C++, Boost, and QuantLib.'
]
senior=[
'Led architecture and development of a multithreaded, fault-tolerant electronic trading platform using Java, Portware, and FIX, supporting concurrent strategies, orders, and multiple asset classes.',
'Supported more than $3 billion in capital on the trading platform and helped save tens of millions of dollars in slippage costs.'
]
aquilent=[
'Built Java/Linux sensor integration systems, including embedded Linux deployments, JNI hardware interfaces, serial communications, XML instrument definitions, and dynamic sensor discovery.',
'Designed server-side satellite data management and visualization components, XML data models, and a JavaScript-based model equation engine.',
'Developed Apache/Tomcat visualization portals, session administration tools, and an RMI socket solution enabling callbacks through enterprise firewalls.'
]
tech='Java, Python, MATLAB, C/C++, AWS, IBM Symphony, Docker, IntexCalc, DealMaker, QuantLib, FIX, Oracle, SQL Server, Snowflake, MongoDB, Spring Boot, PyTorch, JSON, VS Code, Amazon Q, Copilot, and harness engineering.'
finance='Credit risk transfer (CRT), structured finance, mortgage analytics, portfolio risk, capital planning, ROE, CECL, DFAST, derivatives pricing, scenario analysis, and stress testing. Mortgage products: MBS, TBA, agency debt, and CMO; hedge accounting.'
lead='People management, technical leadership, multi-project delivery, financial model implementation, and investment decision support.'
summary_fin='Financial engineering director with more than 20 years of experience across mortgage finance, quantitative research, risk management, and trading systems. Leads CRT valuation and portfolio risk analytics and owns an enterprise forecasting platform supporting income statements, balance sheets, CECL, capital planning, and DFAST. Combines mortgage and structured finance expertise with hands-on engineering and large-scale analytics on AWS and IBM Symphony.'
summary_eng='Financial engineering director and technology leader with more than 20 years of experience across financial platforms, quantitative research, risk management, and trading systems. Combines technical leadership and hands-on Java, Python, and C/C++ expertise with large-scale analytics on AWS and IBM Symphony. Experience spans fault-tolerant trading architecture, enterprise forecasting, database integration, and the use of generative AI tools to streamline engineering delivery.'

def resume(folder,base,financial,req):
 title='FINANCIAL ENGINEERING & MORTGAGE ANALYTICS LEADER' if financial else 'FINANCIAL ENGINEERING & SOFTWARE TECHNOLOGY LEADER'
 sections=[('# XUEWU CAI',None),(title,None),('Clarksville, MD | 410-446-6815 | gourmetcai@gmail.com',None),('linkedin.com/in/xuewu-cai-a8069664 | U.S. citizen',None),('## PROFESSIONAL SUMMARY',None),(summary_fin if financial else summary_eng,None),('## CORE EXPERTISE',None)]
 for a,b in ([('Finance & risk',finance),('Leadership & delivery',lead),('Technology',tech)] if financial else [('Technology',tech),('Leadership & delivery',lead),('Finance & risk',finance)]):sections.append((a+': '+b,None))
 sections += [('## PROFESSIONAL EXPERIENCE',None),('### Freddie Mac | Director, Financial Engineering',None),('May 2014 – Present | McLean, VA',None)]
 order=[3,0,1,2,4,7,6,5] if financial else [1,3,4,5,0,2,6,7]
 sections += [(freddie[i],'bullet') for i in order]
 sections += [('', 'page'),('## PROFESSIONAL EXPERIENCE — CONTINUED',None),('### Campbell & Company | Research Engineer and Engineering Roles',None),('March 2003 – April 2014 | Washington, DC–Baltimore Area',None),('### Research Engineer, Portfolio and Risk Team | 2009 – 2014',None)]
 sections += [(s,'bullet') for s in research]
 sections += [('### Quantitative Finance Engineer | 2006 – 2008',None)]+[(s,'bullet') for s in quant]
 sections += [('### Senior Software Engineer | 2003 – 2006',None)]+[(s,'bullet') for s in senior]
 sections += [('### Aquilent | Senior Software Engineer',None),('June 1999 – February 2003',None)]+[(s,'bullet') for s in aquilent]
 sections += [('## EDUCATION & PROFESSIONAL DEVELOPMENT',None),('University of Maryland Baltimore County — Master’s Degree, Computer Science',None),('Shanghai Jiao Tong University — M.S., Computer Science & Engineering',None),('Dalian University of Technology — Bachelor’s Degree, Applied Mathematics',None),('Professional development: CAIA (Chartered Alternative Investment Analyst) Level I',None),('## LANGUAGES',None),('Chinese: native or bilingual proficiency | English: full professional proficiency',None)]
 md=folder/(base+'.md');pdf=folder/(base+'.pdf')
 md.write_text('\n\n'.join(('<!-- page break -->' if k=='page' else '- '+s if k=='bullet' else s) for s,k in sections)+'\n')
 styles={
 'body':ParagraphStyle('body',fontName='Helvetica',fontSize=9.1,leading=11.6,spaceAfter=4),
 'bullet':ParagraphStyle('bullet',fontName='Helvetica',fontSize=9.1,leading=11.6,leftIndent=10,firstLineIndent=-7,spaceAfter=4),
 'h1':ParagraphStyle('h1',fontName='Helvetica-Bold',fontSize=19,leading=22,spaceAfter=5),
 'h2':ParagraphStyle('h2',fontName='Helvetica-Bold',fontSize=10,leading=13,spaceBefore=9,spaceAfter=5,textColor=colors.HexColor('#19394a')),
 'h3':ParagraphStyle('h3',fontName='Helvetica-Bold',fontSize=9.3,leading=12,spaceBefore=5,spaceAfter=3)}
 story=[]
 for s,k in sections:
  if k=='page':story.append(PageBreak());continue
  st='bullet' if k=='bullet' else 'h3' if s.startswith('### ') else 'h2' if s.startswith('## ') else 'h1' if s.startswith('# ') else 'body'
  story.append(Paragraph(('• ' if k=='bullet' else '')+escape(s.lstrip('# ')),styles[st]))
 def footer(c,d):
  c.setFont('Helvetica',8);c.setFillColor(colors.grey);c.drawString(40,24,'Xuewu Cai | Financial Engineering & Technology');c.drawRightString(572,24,str(d.page))
 SimpleDocTemplate(str(pdf),pagesize=(612,792),rightMargin=40,leftMargin=40,topMargin=32,bottomMargin=38,title='Xuewu Cai - '+req,author='Xuewu Cai').build(story,onFirstPage=footer,onLaterPages=footer)
 reader=PdfReader(pdf);extracted='\n'.join(p.extract_text() for p in reader.pages)
 for needle in ['Freddie Mac','Campbell & Company','Aquilent','CAIA','1.6 trillion','March 2003','June 1999','Dalian']:
  assert needle in extracted,needle
 assert len(reader.pages)==2, f'Unexpected pagination: {len(reader.pages)}'
 (folder/'resume-text-check.txt').write_text(extracted)
 return md,pdf

common_strengths='Baseline: Freddie Mac Director (May 2014–present) leads multi-project financial engineering; AWS/IBM Symphony modeling and enterprise forecasting. Campbell (2003–2014) documents Java trading architecture, database integration, C++ pricing, and risk reporting. Computer science master’s degrees and applied mathematics bachelor’s degree support degree requirements. Baseline core skills name Python, Docker, Spring Boot, SQL databases and MongoDB.'
common_gaps='Baseline does not establish exact AWS/cloud tenure (2 years required for Engineer 4; 3 for Engineer 5). Confirm before application preparation; do not infer duration from employer tenure. Preferred frontend framework tenure, open-source contributions, CI/CD/IaC tenure, Kubernetes operations and observability are not documented. Multiple language experience exists, but language-specific durations are not claimed. No production LLM/agent experience is claimed.'
def main():
 existing=ledger('list'); assert not any(j.get('status') in ('submitting','submission_unknown') for j in existing),'Reconciliation required'
 jobs=[]
 for key in ['capital5','capital-ai4','capital-mlx5']:
  meta=json.loads((RUN/(key+'-metadata.json')).read_text());s=json.loads(meta['jsonld'][0]);req=s['identifier']['value']
  jobs.append(dict(employer='Capital One',title=s['title'],requisition_id=req,canonical_url=s['url'],application_url=next(x for x in meta['application_links'] if '/apply' in x),posted_date=s['datePosted'],posted_date_evidence='Employer page visible posted date and JobPosting.datePosted match.',location='McLean, VA; additional U.S. offices listed in job.md',remote_restrictions='Not advertised as remote; confirm office cadence. No relocation assumed.',salary='$197,300–$225,100 McLean base' if key=='capital-ai4' else '$229,900–$262,400 McLean base',description=plain(s['description']),target='eligible',fit='Strong engineering/platform overlap; confirm required cloud tenure.',gaps=common_gaps,strengths=common_strengths,financial=False,open_evidence='Live employer detail page with Apply destination and current listing index; no expired deadline displayed.'))
 for key,financial,target,gaps in [('fannie-director',True,'eligible','Mortgage forecasting and risk overlap is strong. Baseline does not separately document specified-pool trading, financing-cost attribution, forecast-to-actual processes or team size. Confirm scope and office cadence; no CFA/FRM or full CAIA charter claimed.'),('fannie-job',True,'needs_verification','Mandatory Tableau dashboard development/support is not documented. Confirm experience before treating this as eligible. R is preferred and not evidenced.'),('fannie-modeling',False,'needs_verification','Mandatory 5+ years leading product teams, product strategy/investment priorities, and product management/agile/value realization expertise are not established by the financial engineering leadership baseline. Confirm scope first.')]:
  s=json.loads((RUN/(key+'.json')).read_text())['jobPostingInfo']
  jobs.append(dict(employer='Fannie Mae',title=s['title'],requisition_id=s['jobReqId'],canonical_url=s['externalUrl'],application_url=s['externalUrl']+'/apply',posted_date=s['startDate'],posted_date_evidence='Public employer Workday jobPostingInfo.startDate; '+s['postedOn']+'. JR2899 board alias said Oct 14; employer Oct 21 takes precedence.',location=s['location']+'; '+'; '.join(s.get('additionalLocations',[])),remote_restrictions='Flex / hybrid. Regular office attendance; cadence set by manager.',salary='$109,000–$142,000 base' if key=='fannie-job' else '$200,000–$269,000 base',description=plain(s['jobDescription']),target=target,fit='Strong mortgage/CRT forecasting, valuation, capital/ROE and analytical leadership match.' if key=='fannie-director' else 'Related financial analytics/platform leadership; mandatory experience needs verification.',gaps=gaps,strengths=common_strengths+' Freddie Mac baseline specifically documents prepayment/default modeling, duration, convexity, OAS/KRD, income/balance-sheet/CECL forecasting, CRT and RPL/synthetic economics.',financial=financial,open_evidence='Public employer Workday data: posted=true, canApply=true.'))
 for key,employer,req,title,url,date,target,gaps in [
 ('ninja','NinjaOne','oW2zAfwR','Staff Software Engineer, Java','https://jobs.jobvite.com/ninjaone/job/oW2zAfwR','2026-07-29','skipped','Employer JobPosting.datePosted is July 29, outside September 1–November 1. Built In reposted label does not reset original date.'),
 ('citi','Citi','261002851','Forward Deployed Engineer - Director','https://jobs.citi.com/job/jersey-city/forward-deployed-engineer-director/287/102161068528','2026-10-19','skipped','Anticipated posting close date October 23 has passed; not eligible without renewed open-status evidence. Mandatory production ADK/MCP, extensive Kubernetes operations and customer-facing FDE experience are also unsupported.'),
 ('guild','Guild Mortgage','LEADS018553','Lead, Software Engineer','https://recruiting.ultipro.com/gui1001/JobBoard/634382fd-6424-ec1b-8e37-2aa4ce4c10de/OpportunityDetail?opportunityId=e8888664-35ad-4592-8a84-4b823affbf3b','2026-10-05','needs_verification','Search-indexed employer date only; live page returns unsupported-browser shell. Full description and open status unavailable. Resume not prepared until verified.'),
 ('accellor','Accellor','5C44EACEF1','Senior Java Developer - Java J2EE, Cursor AI','https://apply.workable.com/accellor/j/5C44EACEF1/',None,'needs_verification','Employer public page is a JavaScript shell; source dates and full current requirements not verified. Cursor AI experience requested; baseline documents Copilot/Amazon Q, not Cursor.')]:
  jobs.append(dict(employer=employer,title=title,requisition_id=req,canonical_url=url,application_url=url,posted_date=date,posted_date_evidence='Employer JSON-LD datePosted' if key=='ninja' else 'Employer visible posted date' if key=='citi' else 'Unverified employer index date' if key=='guild' else 'Unknown; secondary Oct 21 not accepted as verified employer date.',location='U.S. remote (Maryland included)' if key=='ninja' else 'Jersey City, NJ (hybrid)' if key=='citi' else 'Remote U.S.' if key=='guild' else 'Silver Spring, MD / U.S. remote',remote_restrictions='See employer evidence; no relocation assumed.',salary='$200,000–$300,000 base in MD' if key=='ninja' else '$170,000–$300,000 base' if key=='citi' else None,description=(RUN/(key+'.txt')).read_text(),target=target,fit='Relevant software/leadership overlap; excluded or verification pending.',gaps=gaps,strengths=common_strengths,financial=False,open_evidence='See gaps; not counted eligible.'))
 outcomes=[]
 for j in jobs:
  target=j.pop('target');financial=j.pop('financial');desc=j.pop('description')
  j.update(retrieved_at=NOW,aliases=[],discovery_window=['2026-09-01','2026-11-01'],status='discovered')
  if j['requisition_id']=='JR2899':j['aliases']=['https://jobrise.io/en/jobs/listing/workday-fanniemae-fanniemaecareers-JR2899/']
  added=mutate('add',j);jid=added['id']
  if added['duplicate']:raise RuntimeError('Existing job detected; reconcile instead of overwriting '+jid)
  folder=ROOT/'applications'/('2026-11-01__'+slug(j['employer'])+'__'+slug(j['title'])+'__'+jid);folder.mkdir(parents=True,exist_ok=False)
  (folder/'job.md').write_text('# '+j['title']+'\n\n'+json.dumps(j,indent=2,ensure_ascii=False)+'\n\n## Retrieved job description\n\n'+desc+'\n')
  match='# Requirement assessment\n\n'+j['fit']+'\n\n## Supported evidence\n\n'+j['strengths']+'\n\n## Gaps and unresolved eligibility\n\n'+j['gaps']+'\n\n## Tailoring and factual boundaries\n\nSummary and expertise order emphasize '+('mortgage forecasting, valuation, CRT, capital and scenario analysis' if financial else 'Java/Python engineering, AWS platforms, trading architecture and technical delivery')+'. Freddie Mac bullets are reordered; original employer names, titles, dates, degrees and quantified claims retain their baseline scope. $1.6T is CRT program coverage, not personally managed assets. CAIA Level I remains professional development. No new experience or duration is added. Senior IC roles are considered on responsibilities and supported hands-on engineering, without changing official director title.\n'
  (folder/'match.md').write_text(match)
  packet={**j,'id':jid,'status':target,'step':1,'selected':False,'submitted':False,'artifacts':{},'resume_review':'not generated; verification required'}
  if target=='eligible':
   base='resume-xuewu-cai__'+slug(j['employer'])+'__'+slug(j['title'])+'__'+j['requisition_id']+'__v1'
   md,pdf=resume(folder,base,financial,j['requisition_id'])
   packet['artifacts']={k:{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for k,p in [('resume_markdown',md),('resume_pdf',pdf)]}
   packet['resume_review']='Text extraction passed; visual review pending. Required cloud duration confirmation remains for Capital One.' if j['employer']=='Capital One' else 'Text extraction passed; visual review pending.'
  (folder/'application.json').write_text(json.dumps(packet,indent=2,ensure_ascii=False)+'\n')
  patch={'status':target,'application_directory':str(folder.relative_to(ROOT)),'artifacts':packet['artifacts'],'resume_review':packet['resume_review']}
  mutate('update',patch,jid);outcomes.append({'id':jid,'employer':j['employer'],'title':j['title'],'status':target})
 (RUN/'outcomes.json').write_text(json.dumps(outcomes,indent=2)+'\n')
 print(json.dumps(outcomes,indent=2))
if __name__=='__main__':main()
