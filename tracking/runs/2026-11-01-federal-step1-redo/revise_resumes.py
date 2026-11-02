"""Create concise v2 resumes from supported baseline facts, retaining v1 artifacts."""
from pathlib import Path
import datetime,hashlib,json,re,subprocess
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from pypdf import PdfReader
ROOT=Path.cwd();RUN=Path(__file__).resolve().parent;CLI=ROOT/'skills/job-application-agent/scripts/ledger.py'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ref=json.loads((ROOT/'candidate/preferences.json').read_text())['resume_output_policy']['format_reference']
NAVY=colors.HexColor('#1c2e48');BLUE=colors.HexColor('#285b8b')
styles={
 'name':ParagraphStyle('name',fontName='Helvetica-Bold',fontSize=20,leading=22,textColor=NAVY,spaceAfter=2),
 'tag':ParagraphStyle('tag',fontName='Helvetica-Bold',fontSize=9.2,leading=11,textColor=BLUE,spaceAfter=2),
 'contact':ParagraphStyle('contact',fontName='Helvetica',fontSize=7.9,leading=9.8,spaceAfter=4),
 'body':ParagraphStyle('body',fontName='Helvetica',fontSize=8.7,leading=10.8,spaceAfter=3),
 'skill':ParagraphStyle('skill',fontName='Helvetica',fontSize=8.5,leading=10.4,spaceAfter=1.5),
 'role':ParagraphStyle('role',fontName='Helvetica-Bold',fontSize=9,leading=11),
 'date':ParagraphStyle('date',fontName='Helvetica',fontSize=8.3,leading=11,alignment=2,textColor=colors.HexColor('#444444')),
 'sub':ParagraphStyle('sub',fontName='Helvetica-Oblique',fontSize=8.3,leading=10.1,spaceAfter=3,textColor=colors.HexColor('#444444')),
 'bullet':ParagraphStyle('bullet',fontName='Helvetica',fontSize=8.7,leading=10.8,leftIndent=8,firstLineIndent=-6,spaceAfter=2.3),
 'head':ParagraphStyle('head',fontName='Helvetica-Bold',fontSize=9.4,leading=12,textColor=NAVY,spaceBefore=6,spaceAfter=2)}
class Rule(Flowable):
 def __init__(self,width,color):Flowable.__init__(self);self.width=width;self.height=3;self.color=color
 def draw(self):self.canv.setStrokeColor(self.color);self.canv.setLineWidth(.5);self.canv.line(0,2,self.width,2)
def para(t,key='body'):return Paragraph(escape(t),styles[key])
common_freddie=[
 'Direct development of modeling tools combining prepayment/default models, AWS and IBM Symphony computing, and Intex valuation analytics to assess bond performance and transaction economics.',
 'Own an enterprise forecasting platform for income statements, balance sheets and CECL estimates, supporting business planning, capital planning and DFAST stress testing.',
 'Lead engineering projects for STACR bond issuance and ACIS reinsurance within a CRT program protecting more than $1.6 trillion in mortgage loans.',
 'Deliver RPL and synthetic-structure deal memorandum, capital, economics and ROE analytics; use Copilot and harness engineering to support delivery.',
 'Manage the LIBOR-to-SOFR transition within CRT modeling tools and analytics.'
]
common_aquilent='Built Java/Linux sensor integration systems with embedded Linux, JNI, serial communications and dynamic sensor discovery; developed Apache/Tomcat visualization portals and server-side satellite data components.'
variants={
 'a5af83ea7ba6d744':dict(tag='Enterprise Applications & Workflow Delivery | Java, Python, AWS | Financial Analytics',summary='Financial engineering director and technology leader with more than 20 years of experience delivering enterprise financial platforms, quantitative analytics and trading systems. Leads modeling and forecasting delivery on AWS and IBM Symphony, with hands-on Java, Python and C/C++ expertise. Uses Copilot and other generative AI tools to streamline engineering workflows, while connecting financial requirements with practical software implementation.',skills=[('Applications & Data','Java, Python, C/C++, MATLAB, SQL, Oracle, SQL Server, Spring Boot, Docker'),('Platforms & Integration','AWS, IBM Symphony, database connectivity, time-series infrastructure, market data feeds'),('Business Delivery','enterprise forecasting, financial model implementation, multi-project delivery, technical leadership'),('Finance & AI Tools','CRT, CECL, capital planning, DFAST; Copilot, Amazon Q, harness engineering')],freddie=[common_freddie[i] for i in [0,1,3,2,4]],campbell=[
 'Led architecture and development of a multithreaded, fault-tolerant Java/Portware/FIX trading platform supporting concurrent strategies, orders and multiple asset classes; supported more than $3 billion in capital and helped save tens of millions in slippage costs.',
 'Built a Java-based intraday cash equity trading system on Caché and market data/time-series infrastructure in MFC/C++; unified MATLAB access to Oracle, SQL Server, Caché and QADirect through a Java connectivity layer.',
 'Designed risk reporting for Investment Committee decisions and produced SEC, CFTC and OPERA reporting using MATLAB, Java/StyleReport and Panopticon.']),
 'fa28275048f3ce60':dict(tag='Data Engineering & Analytics Platforms | Java, Python, SQL | AWS & Distributed Computing',summary='Technology and financial engineering leader with more than 20 years across data-intensive financial platforms, quantitative research and trading systems. Built time-series infrastructure, market data feeds and Java database connectivity, and leads large-scale modeling analytics on AWS and IBM Symphony. Combines hands-on Java, Python, C/C++ and SQL database skills with technical leadership and enterprise model implementation.',skills=[('Programming & Databases','Java, Python, C/C++, MATLAB, SQL, Oracle, SQL Server, Snowflake, MongoDB'),('Data & Integration','time-series infrastructure, market data feeds, database connectivity, financial model implementation'),('Cloud & Platforms','AWS, IBM Symphony, Docker, Spring Boot; large-scale computing and enterprise analytics'),('Delivery & Analysis','technical leadership, multi-project delivery, scenario analysis, forecasting; Copilot and Amazon Q')],freddie=[common_freddie[i] for i in [0,1,2,3,4]],campbell=[
 'Built time-series data infrastructure and market data feeds in MFC/C++, alongside a Java-based intraday cash equity trading system using the Caché database.',
 'Designed a Java connectivity layer unifying MATLAB access to production databases including Oracle, SQL Server, Caché and QADirect.',
 'Led a multithreaded, fault-tolerant Java/Portware/FIX trading platform; developed volatility/correlation forecasting models and risk reports using daily, intraday and tick data.']),
 '4e066be541ca1382':dict(tag='Quantitative Research & Decision Support | Monte Carlo, Forecasting & Risk | MATLAB, Python, Java',summary='Financial engineering director with more than 20 years in quantitative research, financial modeling, forecasting and decision support. Applies Monte Carlo simulation, bootstrapping, statistical analysis and scenario-based risk measurement. Leads enterprise forecasting, capital planning and stress testing platform delivery, with experience translating analytical findings into Investment Committee reporting and transaction economics.',skills=[('Quantitative Methods','Monte Carlo simulation, bootstrapping, volatility/correlation forecasts, scenario and stress analysis'),('Decision Support','portfolio risk, factor analysis, capital planning, CECL, DFAST, transaction economics, ROE'),('Programming & Computing','MATLAB, Python, Java, C/C++, SQL, AWS, IBM Symphony, QuantLib'),('Leadership & Reporting','technical leadership, multi-project delivery, financial model implementation, SEC/CFTC/OPERA reporting')],freddie=[common_freddie[i] for i in [1,0,2,3,4]],campbell=[
 'Developed volatility and correlation forecasting models in MATLAB using daily, intraday, implied-volatility and tick data.',
 'Applied statistical methods, Monte Carlo simulation and bootstrapping to investigate market stress, portfolio drawdowns, regime changes and correlation breakdowns using MATLAB, C/C++ and Java.',
 'Designed risk reporting on factor analysis, scenarios, stress tests, duration and margin for Investment Committee decisions; built an FX options pricing, simulation and risk engine using Visual C++, Boost and QuantLib.'])}
jobs=json.loads(subprocess.check_output(['python3',str(CLI),'list'],text=True));out=[]
for j in jobs:
 if j['id'] not in variants:continue
 assert j['status'] not in {'applied','approved','submitting','submission_unknown'},'Reconcile approval before revision'
 v=variants[j['id']];folder=ROOT/j['application_directory'];old=json.loads((folder/'application.json').read_text())
 base=Path(j['artifacts']['resume_pdf']['path']).stem.replace('__v1','__v2');md=folder/(base+'.md');pdf=folder/(base+'.pdf');assert not md.exists() and not pdf.exists()
 story=[];lines=[];width=524
 def add(t,key='body',prefix=''):
  story.append(para(t,key));lines.append(prefix+t)
 def head(t):
  add(t,'head','## ');story.append(Rule(width,BLUE))
 def role(title,date,sub):
  table=Table([[para(title,'role'),para(date,'date')]],colWidths=[414,110]);table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]));story.append(table);lines.extend(['### '+title+' | '+date,sub]);story.append(para(sub,'sub'))
 def bullet(t):add('• '+t,'bullet','- ')
 add('XUEWU CAI','name','# ');add(v['tag'],'tag');add('Clarksville, MD | 410-446-6815 | gourmetcai@gmail.com | linkedin.com/in/xuewu-cai-a8069664 | U.S. citizen','contact');story.append(Rule(width,NAVY))
 head('PROFESSIONAL SUMMARY');add(v['summary'])
 head('CORE COMPETENCIES')
 for label,text in v['skills']:
  story.append(Paragraph('<b>'+escape(label)+':</b> '+escape(text),styles['skill']));lines.append('**'+label+':** '+text)
 head('PROFESSIONAL EXPERIENCE')
 role('Director, Financial Engineering — Freddie Mac','May 2014 – Present','McLean, VA | Credit Risk Transfer (STACR / ACIS)')
 for text in v['freddie']:bullet(text)
 story.append(Spacer(1,4));role('Campbell & Company | Research Engineer and Engineering Roles','Mar 2003 – Apr 2014','Washington, DC–Baltimore Area')
 add('Research Engineer, Portfolio and Risk Team (2009–2014); Quantitative Finance Engineer (2006–2008); Senior Software Engineer (2003–2006).','sub')
 for text in v['campbell']:bullet(text)
 story.append(Spacer(1,4));role('Senior Software Engineer — Aquilent','Jun 1999 – Feb 2003','Java/Linux integration and data systems');bullet(common_aquilent)
 head('EDUCATION & PROFESSIONAL DEVELOPMENT')
 for t in ['Master’s Degree, Computer Science — University of Maryland Baltimore County','M.S., Computer Science & Engineering — Shanghai Jiao Tong University','Bachelor’s Degree, Applied Mathematics — Dalian University of Technology','Professional development: CAIA (Chartered Alternative Investment Analyst) Level I']:add(t,'skill')
 head('LANGUAGES');add('Chinese: native or bilingual proficiency | English: full professional proficiency','skill')
 def footer(c,d):
  c.setFont('Helvetica',7);c.setFillColor(colors.HexColor('#444444'));c.drawRightString(568,21.6,'XUEWU CAI | Page '+str(d.page))
 SimpleDocTemplate(str(pdf),pagesize=(612,792),leftMargin=44,rightMargin=44,topMargin=30,bottomMargin=35,title='Xuewu Cai — '+j['title'],author='Xuewu Cai').build(story,onFirstPage=footer,onLaterPages=footer)
 md.write_text('\n\n'.join(lines).replace('- • ','- ')+'\n');reader=PdfReader(pdf);assert len(reader.pages)==1,'Concise layout overflow'
 text=reader.pages[0].extract_text();assert all(t in text for t in ['Freddie Mac','Campbell & Company','Aquilent','CAIA','2014','1999','Dalian'])
 (RUN/(j['id']+'-v2-text.txt')).write_text('\n'.join(x.rstrip() for x in text.splitlines()).rstrip()+'\n')
 versions=old.get('artifact_versions',[{'version':1,'artifacts':old['artifacts'],'resume_review':old.get('resume_review')}]);art={k:{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for k,p in [('resume_markdown',md),('resume_pdf',pdf)]};versions.append({'version':2,'artifacts':art,'format_reference':ref})
 patch={'artifacts':art,'artifact_versions':versions,'resume_version':2,'resume_status':'draft_missing_required_facts','resume_review':'One page, selectable text; extraction passed; visual review pending. Candidate hours/week and applicable eligibility facts remain unverified.','format_reference':ref}
 old.update(patch);(folder/'application.json').write_text(json.dumps(old,indent=2,ensure_ascii=False)+'\n')
 tmp=RUN/'ledger-update.json';tmp.write_text(json.dumps(patch));subprocess.run(['python3',str(CLI),'update',j['id'],str(tmp)],check=True,capture_output=True)
 with (folder/'match.md').open('a') as f:f.write('\n## Concise revision v2 — 2026-11-01\n\nUses the user’s CFTC PDF as a format reference: one page, compact summary/competencies, right-aligned dates and selected experience. Condenses baseline-supported project descriptions; omits lower-relevance bullets and exhaustive tools to reduce repetition. All employers, official titles, periods and education retained. $1.6T remains CRT program coverage. Does not import reference-only claims about audit response, governance, control testing, disaster recovery, full-time schedules or production agentic systems. No claim is made that all 20 baseline bullets are reproduced. Required hours/week and job-specific evidence remain unresolved; this is a local draft. Original v1 source/PDF and hashes preserved in artifact_versions.\n')
 out.append({'id':j['id'],'title':j['title'],'pages':1,'artifacts':art,'version':2})
(RUN/'resume-outcomes.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
