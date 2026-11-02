#!/usr/bin/env python3
"""Regenerate the readable queue from the authoritative SQLite ledger."""
import calendar,datetime,json,sqlite3
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[3]
def main():
 with sqlite3.connect(ROOT/'tracking/jobs.sqlite3') as conn:
  jobs=[json.loads(row[0]) for row in conn.execute('SELECT data FROM jobs ORDER BY id')]
 groups={
  'Eligible and unapplied':[], 'Selected / preparation in progress':[],
  'Awaiting final confirmation':[], 'Submitting / submission uncertain':[],
  'Previously applied (including rejected / withdrawn)':[],
  'Needs verification / blocked / skipped / closed without application':[]}
 selected=set()
 for f in (ROOT/'tracking/batches').glob('*.json'):
  d=json.loads(f.read_text());selected.update(d.get('selected_job_ids',[]))
 for j in jobs:
  s=j['status']
  category=('Previously applied (including rejected / withdrawn)' if s in ('applied','rejected','withdrawn') else
   'Submitting / submission uncertain' if s in ('submitting','submission_unknown') else
   'Awaiting final confirmation' if s in ('awaiting_confirmation','approved') else
   'Selected / preparation in progress' if j['id'] in selected and s in ('eligible','draft','discovered') else
   'Eligible and unapplied' if s=='eligible' else
   'Needs verification / blocked / skipped / closed without application')
  groups[category].append(j)
 current=datetime.datetime.now(ZoneInfo('America/New_York'))
 now=current.strftime('%Y-%m-%d %H:%M:%S %Z')
 month=current.year*12+current.month-1-2; year,mi=divmod(month,12)
 start=datetime.date(year,mi+1,min(current.day,calendar.monthrange(year,mi+1)[1]))
 lines=['# Selectable job queue','',f'Last refresh: {now}. Ledger is authoritative. Discovery window: {start}–{current.date()} (inclusive).','',
 'Scope: federal government agency jobs only in Maryland, Virginia and Washington DC; exclude private employers, contractors, GSEs and state/local government. Historical rows retain their recorded statuses pending reconciliation at the next Step 1; scope must be rechecked before Step 2. Geography: Maryland, Virginia and Washington DC only; remote roles must permit working from Maryland/DMV. Selection and final confirmation are required before submission. Eligible means substantial supported responsibilities and no known disqualifier; unresolved requirements remain explicit. Capital One mandatory cloud tenure requires confirmation before preparation.','',
 '| Category | Count |','|---|---:|']
 lines += [f'| {k} | {len(v)} |' for k,v in groups.items()]
 lines += ['',f'Total: {len(jobs)} unique requisitions. Select jobs using the full stable ledger IDs below. Step 2 requires a separate user request.','']
 def cell(s):return str(s or 'Not disclosed').replace('|',' / ').replace('\n',' ')
 for category,rows in groups.items():
  lines += ['## '+category,'']
  if not rows:lines+=['None.',''];continue
  lines+=['| Stable ledger ID | Employer / role | Location / arrangement | Posted | Fit / gaps | Status | Links |','|---|---|---|---|---|---|---|']
  for j in sorted(rows,key=lambda x:(x.get('priority')=='lower',x['employer']!='Fannie Mae',x['employer'],x['title'])):
   folder=j.get('application_directory');pdf=j.get('artifacts',{}).get('resume_pdf',{}).get('path')
   links=f'[Job]({j["canonical_url"]})'
   if folder:links+=f' · [Assessment](../{folder}/match.md)'
   if pdf:links+=f' · [Resume PDF](../{pdf})'
   gaps=j.get('gaps','')
   if len(gaps)>230:gaps=gaps[:227]+'…'
   priority=' Lower-priority scope/pay.' if j.get('priority')=='lower' else ''
   lines.append(f'| `{j["id"]}` | {cell(j["employer"])} — {cell(j["title"])} | {cell(j.get("location"))}; {cell(j.get("remote_restrictions"))} | {cell(j.get("posted_date") or "Unknown")} | {cell(j.get("fit"))}{priority} Gaps: {cell(gaps)} | {j["status"]} | {links} |')
  lines+=['']
 reports=sorted((ROOT/'tracking/runs').glob('*/coverage.md'))
 if reports:
  report=reports[-1].parent.relative_to(ROOT/'tracking')
  lines+=['## Coverage and continuation','',f'Coverage remains partial. Employer evidence overrides repost/index dates. See [latest run coverage]({report}/coverage.md) and [continuation]({report}/continuation.json).','']
 lines+=['Location preference confirmed by user on 2026-11-01. Work arrangement and salary preferences remain unresolved. See current assessments for baseline validation and eligibility gaps.','']
 (ROOT/'tracking/job-queue.md').write_text('\n'.join(lines))
 resume_lines=['# Customized resume PDFs','',f'Last refreshed: {now}. Each PDF is stored beside its editable source in the named employer/role folder.','',
  '| Employer | Role / requisition | Stable ledger ID | Status | Resume files |','|---|---|---|---|---|']
 resume_count=0
 for j in sorted(jobs,key=lambda x:(x['employer'],x['title'])):
  if not j.get('application_directory'):continue
  folder=ROOT/j['application_directory']
  for md in sorted(folder.glob('resume-xuewu-cai__*.md')):
   pdf=md.with_suffix('.pdf');relative_md=md.relative_to(ROOT/'applications')
   source=f'[Markdown]({relative_md})'
   document=f'[PDF]({pdf.relative_to(ROOT/"applications")})' if pdf.is_file() else '**PDF missing — incomplete tailoring**'
   resume_lines.append(f'| {cell(j["employer"])} | {cell(j["title"])} / {cell(j.get("requisition_id"))} | `{j["id"]}` | {j["status"]} | {document} · {source} |')
   resume_count+=1
 resume_lines+=['',f'{resume_count} customized resume version(s). See [job queue](../tracking/job-queue.md) for fit, gaps and selection status.','']
 (ROOT/'applications/resume-index.md').write_text('\n'.join(resume_lines))
 print({k:len(v) for k,v in groups.items()})
if __name__=='__main__':main()
