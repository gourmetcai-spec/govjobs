from pathlib import Path
import ast,json,re,sqlite3,subprocess
ROOT=Path.cwd();RUN=Path(__file__).resolve().parent;CLI=ROOT/'skills/job-application-agent/scripts/ledger.py'
module=ast.parse((RUN/'prepare.py').read_text());flags=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='flags' for t in n.targets))
acronyms={'CPIC','FITARA','OMB','TBM','NIST','CISSP','GPA','OCR','ETL','SAP'}
with sqlite3.connect(ROOT/'tracking/jobs.sqlite3') as c:jobs=[json.loads(r[0]) for r in c.execute('select data from jobs')]
companions=json.loads((RUN/'possible-companion-routes.json').read_text());related={i:[x for x in group if x!=i] for group in companions for i in group}
# Read clean qualification text from saved per-job source, preserving original evidence.
from html.parser import HTMLParser
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,d):self.parts.append(d+' ')
def clean(s):
 p=Text();p.feed(s);return re.sub(r'\s+',' ',''.join(p.parts)).strip()
notes={};publics={}
for j in jobs:
 id=j['id'];control=j['control_number'];jp=json.loads((RUN/'announcements'/(control+'.json')).read_text());raw=(RUN/'announcements'/(control+'.txt')).read_text();q=clean(jp.get('qualifications','')+' '+jp.get('educationRequirements',''));attention=[]
 clarification=re.search(r'Clarification from the agency\s*(.{0,1400})',raw,re.S)
 public=any('public' in x.lower() for x in j.get('hiring_paths',[])) or bool(clarification and re.search(r'all\s+(?:U\.?\s*S\.?|United States)\s+citizens',clarification.group(1),re.I))
 publics[id]=public
 if not public:attention.append('Hiring-path eligibility unverified: '+', '.join(j.get('hiring_paths',[]))+'. Confirm qualifying status before application; absence from baseline is not proof of ineligibility.')
 for token,label in flags:
  matched=bool(re.search(r'\b'+re.escape(token)+r'\b',q,re.I)) if token in acronyms else token.lower() in q.lower()
  if matched:attention.append('Verify '+label+' against the exact qualification clause; not established by the baseline alone.')
 if 'recent graduate' in j['title'].lower() or any('graduate' in h.lower() for h in j.get('hiring_paths',[])):attention.append('Confirm graduate/student hiring-path dates and eligibility; degree completion dates are not in the baseline.')
 if not attention:attention.append('Confirm the announcement-specific specialized experience, grade-equivalent scope and mandatory conditions against your actual work history.')
 attention.append('Hours worked per week and exact employment days, when required, need your confirmation; do not invent them.')
 if 'own words' in raw and 'artificial intelligence' in raw.lower():attention.append('Any own-words/no-AI essay certification must be answered personally; no such essays drafted.')
 if control=='759326100':attention.append('Official September 1 posting date is confirmed. This existing record is retained although it predates today’s September 2 new-discovery cutoff. GPA and CIA screening requirements remain unverified.')
 if id in related:attention.append('Possible companion hiring-route announcement(s): '+', '.join(related[id])+'. Reconcile before submission; do not submit twice to the same vacancy.')
 patch={'requirements_unverified':attention,'gaps':' '.join(attention),'public_hiring_route_evidence':public}
 p=RUN/'attention-patch.json';p.write_text(json.dumps(patch));subprocess.run(['python3',str(CLI),'update',id,str(p)],check=True,capture_output=True)
 folder=ROOT/j['application_directory'];p=folder/'application.json';d=json.loads(p.read_text());d.update(patch);d['required_answers_pending']=attention;p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
 p=folder/'match.md';s=p.read_text();marker='### Requirements needing confirmation\n\n';pos=s.rfind(marker);assert pos>=0;s=s[:pos]+s[pos:].replace(s[pos+len(marker):s.index('\n\n### Confirmed unmet requirements',pos)],'\n'.join('- '+x for x in attention),1);p.write_text(s)
 notes[id]=attention;j.update(patch)
# Update the already-written daily snapshot in place before its first commit.
p=ROOT/'tracking/daily-updates/2026-11-02/2026-11-02-step1-175625.md';s=p.read_text()
for id,attention in notes.items():
 marker=' — '+id+'\n';pos=s.find(marker)
 if pos<0:continue
 a=s.index('- Mandatory requirements needing verification:\n',pos)+len('- Mandatory requirements needing verification:\n');b=s.index('- Preferred requirements:',a);s=s[:a]+''.join('  - '+x+'\n' for x in attention)+s[b:]
p.write_text(s)
for filename in ['outcomes.json','response-rows.json']:
 p=RUN/filename;rows=json.loads(p.read_text())
 for r in rows:
  if 'attention' in r and isinstance(r['attention'],list):r['attention']=notes[r['id']]
  elif filename=='response-rows.json':
   words=[];text=' '.join(notes[r['id']]).lower()
   if not publics[r['id']]:words.append('hiring status')
   for key,label in [('cpic','CPIC'),('sharepoint','SharePoint'),('accounting','accounting'),('economics coursework','economics credits'),('qualifying coursework','course credits'),('production','production experience'),('machine learning','ML scope'),('gpa','GPA'),('omb/federal','federal budget'),('document extraction','document extraction'),('pl/sql','PL/SQL'),('examiner commission','examiner commission')]:
    if key in text:words.append(label)
   r['attention']=', '.join(words[:3]) or 'specialized experience'
 p.write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
# Fix the generation source too; no PDFs are regenerated by this correction.
p=RUN/'prepare.py';s=p.read_text().replace("if token.lower() in qtext:attention.append", "if re.search(r'\\b'+re.escape(token)+r'\\b',qtext,re.I):attention.append");p.write_text(s)
subprocess.run(['python3',str(ROOT/'skills/job-application-agent/scripts/refresh_queue.py')],check=True)
print('Verified acronym boundaries for requirement flags; current report/packets updated without changing PDFs.')
