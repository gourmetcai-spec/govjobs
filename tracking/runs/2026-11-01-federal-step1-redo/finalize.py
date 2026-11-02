from pathlib import Path
import json,sqlite3,hashlib,datetime,subprocess
from zoneinfo import ZoneInfo
from pypdf import PdfReader
ROOT=Path.cwd();RUN=Path(__file__).resolve().parent;CLI=ROOT/'skills/job-application-agent/scripts/ledger.py';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
jobs=json.loads(subprocess.check_output(['python3',str(CLI),'list'],text=True));validation=[]
for j in jobs:
 if j.get('resume_version')!=2:continue
 folder=ROOT/j['application_directory'];packetfile=folder/'application.json';packet=json.loads(packetfile.read_text());review='One selectable-text page; all pages rendered with PDFKit and visually compared with the CFTC template. No clipping, overlap or blank pages; original v1 files and hashes preserved. Draft pending required candidate facts and applicable eligibility evidence.'
 assert packet['artifacts']==j['artifacts'];assert len(packet['artifact_versions'])==2
 for version in packet['artifact_versions']:
  for artifact in version['artifacts'].values():assert sha(ROOT/artifact['path'])==artifact['sha256']
 pdf=ROOT/packet['artifacts']['resume_pdf']['path'];reader=PdfReader(pdf);assert len(reader.pages)==1
 text=reader.pages[0].extract_text();assert len(text.split())<650
 for term in ['Freddie Mac','Campbell & Company','Aquilent','2014','2003','1999','CAIA','Dalian']:
  assert term in text,term
 for term in ['audit-ready','control testing','disaster recovery','Full-time','cross-agency']:
  assert term not in text,term
 # Prior reviewed resume files must be byte-identical to the preceding Git checkpoint.
 for artifact in packet['artifact_versions'][0]['artifacts'].values():
  prior=subprocess.check_output(['git','show','HEAD:'+artifact['path']]);assert hashlib.sha256(prior).hexdigest()==artifact['sha256']
 packet['resume_review']=review;packetfile.write_text(json.dumps(packet,indent=2,ensure_ascii=False)+'\n')
 patch=RUN/'review-patch.json';patch.write_text(json.dumps({'resume_review':review}));subprocess.run(['python3',str(CLI),'update',j['id'],str(patch)],check=True,capture_output=True)
 previous=ROOT/packet['artifact_versions'][0]['artifacts']['resume_pdf']['path'];oldtext=' '.join(p.extract_text() for p in PdfReader(previous).pages)
 validation.append({'id':j['id'],'v1_pages':2,'v2_pages':1,'v1_words':len(oldtext.split()),'v2_words':len(text.split()),'v1_unchanged':True,'hashes_valid':True,'visual_review':'passed; v2-contact-sheet.png','format_reference_hash':packet['format_reference']['sha256']})
prefs=json.loads((ROOT/'candidate/preferences.json').read_text());assert sha(ROOT/prefs['baseline'])==prefs['baseline_sha256'];ref=prefs['resume_output_policy']['format_reference'];assert sha(ROOT/ref['path'])==ref['sha256']
with sqlite3.connect(ROOT/'tracking/jobs.sqlite3') as c:
 assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
 assert c.execute('select count(*) from jobs').fetchone()[0]==15
 assert not any(j['status'] in {'applied','submitting','submission_unknown'} for j in jobs)
(RUN/'validation.json').write_text(json.dumps({'baseline_unchanged':True,'reference_unchanged':True,'sqlite_integrity':'ok','resumes':validation,'portal_actions':0},indent=2)+'\n')
print(json.dumps(validation,indent=2))
now=datetime.datetime.now(ZoneInfo('America/New_York')).isoformat()
coverage=f'''# Step 1 redo — concise CFTC format

Run: {now}. Window: September 1–November 1, 2026 inclusive. Federal agencies only, DC/MD/VA; all other criteria retained. Baseline and format-reference hashes unchanged. The reference PDF is used for layout and concision only; its unverified controls/governance/audit and work-schedule claims are not adopted.

## Search and reconciliation

16 search-index query attempts across all eight established tracks plus date/lead checks. See query-audit.json for exact queries/filters. Each query used one returned result set. Batch outputs can be bounded at 40,000 characters and do not provide reliable per-query counts; only saved visible records are assessed. Refreshed all 11 existing official announcements, retaining stable IDs and statuses. Assessed CFTC 889991400, USSC 888547100 and prior continuation leads 890500200, 889752600, 889753100 and 889254700. FDIC 887093300 was screened as already closed. See saved official source text, job-outcomes.json and screened-out.json.

Native USAJOBS APPSW/Maryland and finance/Washington page 1 were attempted; no reliable pagination exhaustion or complete vacancy list was established. FHFA/FDIC careers pages were retried. Source access/rendering and index coverage remain partial; no exhaustive coverage is claimed. Prior broader 55-query run remains available as history rather than being represented as fresh queries.

Existing 11 records refreshed; 4 unique records added: CFTC Systems Risk Analyst, USSC Software Engineering and Data Automation Specialist, BEA IT Specialist (Policy and Planning), SSA Head of Tech Finance. First three need mandatory-experience and date verification. SSA has restricted Civil Service/SES eligibility and was skipped. USDA lead is outside DMV; BEA merit-promotion companion was screened separately from the public route; FDIC role is closed/restricted. No duplicate records or applications created.

Final ledger: 15 records — 1 eligible (FEMA IT Specialist), 11 needs_verification, 3 skipped. Existing required facts remain unresolved, including hours/week; CIA GPA and course/identity/date evidence and ICE coursework/calculus/date evidence as applicable. No candidate answer was received during this redo.

## Resume changes and validation

Rebuilt the three existing tailored resumes as one-page v2 Markdown/PDF drafts in the same named job folders. Original v1 Markdown/PDF bytes and hashes preserved; artifact_versions stores both versions, with current manifests/ledger pointing to v2. The template’s short summary, grouped competencies, blue rules, right-aligned dates and compact education/language sections were reproduced. Selected nine experience bullets per resume replace exhaustive baseline duplication. Claims were reviewed against the original factual baseline; no unsupported experience added. The drafts remain incomplete for portal use pending required facts.

All three v2 pages were rendered with PDFKit and visually compared with the supplied template. No clipping, overlap or blank pages. Hashes, one-page count, selectable text, original v1 preservation, baseline/reference hashes and SQLite integrity passed. See validation.json for before/after word counts and v2-contact-sheet.png for visual evidence.

No selections, portal preparation, uploads or submissions. Step 2 requires a new user selection and final completed-packet confirmation.
'''
(RUN/'coverage.md').write_text(coverage)
remaining={'step':1,'window':['2026-09-01','2026-11-01'],'remaining':['Resume native USAJOBS pagination when usable; no source exhausted cursor established.','Complete current official FDIC/OCC/SEC agency vacancy enumeration and repeat all search tracks across DC/MD/VA.','Resolve mandatory requirements and original posting dates for new CFTC/USSC/BEA leads and existing needs_verification roles.','Confirm missing candidate hours/week, exact employment days where required, CIA GPA and ICE qualifying coursework; regenerate later resume versions only when verified facts arrive.'],'current_resume_version':2,'preserve_v1':True,'portal_actions':0};(RUN/'continuation.json').write_text(json.dumps(remaining,indent=2)+'\n')
with (ROOT/'joblog.md').open('a') as f:f.write(f'''\n## 2026-11-01 — Step 1 redo using concise CFTC format\n\n- Checkpoint {now}; window September 1–November 1. Baseline hash unchanged. Inspected user-provided Xuewu-Cai-Resume-CFTC-Systems-Risk-Analyst-889991400.pdf visually and by text/font extraction; saved its hash and format-only role in candidate preferences and skill. Prior checkpoint 85fe348 was pushed and remote SHA verified.\n- Refreshed all 11 existing jobs; performed 16 new search-index queries and native/agency-source attempts across established tracks. Added 4 unique federal DMV records: CFTC f720af72449c48a0, USSC 16f54e578b2089d3, BEA 48ee9a40e142e566 (needs_verification), SSA b6f24c3fd93797f0 (skipped for restricted hiring path). USDA outside-DMV, BEA restricted companion and closed FDIC lead screened without duplicate records. Final counts: 15 jobs, 1 eligible, 11 needs_verification, 3 skipped. Coverage remains partial; [audit and coverage](tracking/runs/2026-11-01-federal-step1-redo/coverage.md) and [continuation](tracking/runs/2026-11-01-federal-step1-redo/continuation.json) saved.\n- Revised FEMA, CIA and ICE resumes to concise one-page v2 drafts using the supplied layout. Selected supported bullets and condensed summaries/competencies; preserved all original v1 files byte-for-byte and retained version hashes. Avoided unsupported claims from the reference. All three pages visually reviewed, extracted-text/hash checks passed; baseline/reference unchanged and SQLite integrity OK. Missing required candidate facts and eligibility evidence remain blockers; no portal-ready claim. [Resume index](applications/resume-index.md) and [queue](tracking/job-queue.md) regenerated.\n- No user selections, portal forms, uploads, assessments or submissions. Commit and push this Step 1/configuration checkpoint to confirmed govjobs origin/main; report actual result in response.\n''')
