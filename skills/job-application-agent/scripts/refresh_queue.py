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
  'Eligible and unapplied':[], 'Unverified and unapplied — prepare with attention items':[], 'Selected / preparation in progress':[],
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
   'Selected / preparation in progress' if j['id'] in selected and s in ('eligible','draft','discovered','needs_verification') else
   'Eligible and unapplied' if s=='eligible' else
   'Unverified and unapplied — prepare with attention items' if s=='needs_verification' else
   'Needs verification / blocked / skipped / closed without application')
  groups[category].append(j)
 current=datetime.datetime.now(ZoneInfo('America/New_York'))
 now=current.strftime('%Y-%m-%d %H:%M:%S %Z')
 month=current.year*12+current.month-1-2; year,mi=divmod(month,12)
 start=datetime.date(year,mi+1,min(current.day,calendar.monthrange(year,mi+1)[1]))
 lines=['# Selectable job queue','',f'Last refresh: {now}. Ledger is authoritative. Discovery window: {start}–{current.date()} (inclusive).','',
 'Scope: federal government agency jobs only in Maryland, Virginia and Washington DC. Prepare plausible jobs even when qualifications or dates are unverified; keep unknown facts explicit. Only clear evidenced exclusions stop preparation. Step 2 requires user selection and final submission confirmation. See [all unsubmitted jobs and attention items](unsubmitted-jobs.md).','',
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
 summary=['# Unsubmitted jobs — review and attention items','',f'Last refresh: {now}. Verification status is preserved; unknown qualifications or dates do not block preparation.','']
 pending=[j for j in jobs if j['status'] not in ('applied','rejected','withdrawn') and not j.get('submitted_at') and not j.get('receipt_evidence')]
 summary += [f'{len(pending)} unsubmitted position(s). Existing exclusion decisions must be rechecked under the current preparation policy on the next Step 1.','']
 def review_group(j):
  if j['status'] in ('submitting','submission_unknown'):return 0,'Uncertain submissions — reconcile first'
  if j['status'] in ('skipped','closed'):return 2,'Recorded exclusions — recheck evidence'
  return 1,'Preparation candidates'
 previous_group=None
 for j in sorted(pending,key=lambda x:(review_group(x)[0],x['employer'],x['title'])):
  group=review_group(j)[1]
  if group!=previous_group:summary+=['## '+group,''];previous_group=group
  s=j['status'];pdf=j.get('artifacts',{}).get('resume_pdf',{}).get('path')
  if s in ('submitting','submission_unknown'):action='Reconcile the uncertain submission before any new attempt.'
  elif s in ('skipped','closed'):action='Review recorded exclusion evidence; retain only clear exclusions under current policy.'
  elif not pdf:action='Prepare the missing Markdown/PDF resume and local packet at the next Step 1; keep uncertainties explicit.'
  elif s in ('awaiting_confirmation','approved'):action='Review the exact packet and current approval before any submission.'
  else:action='Complete remaining independent preparation; user selection is required for Step 2.'
  summary += [f'### {j["employer"]} — {j["title"]}', '',f'- Stable ID: `{j["id"]}`',f'- Location: {j.get("location") or "Unknown"}',f'- Role / supported fit: {j.get("role_summary") or j.get("fit") or "See job description and assessment."}',f'- Deadline: {j.get("close_date") or "Unknown — needs attention"}',f'- Status: {s}; resume: {j.get("resume_status") or "Not recorded"}',f'- Current resume: '+(f'[PDF](../{pdf})' if pdf else 'Not generated yet — preparation remains outstanding.'),f'- Attention: {j.get("gaps") or "No additional issues recorded."}',f'- Next action: {action}',f'- [Official job]({j["canonical_url"]})','']
 if not pending:summary+=['No unsubmitted positions.','']
 (ROOT/'tracking/unsubmitted-jobs.md').write_text('\n'.join(summary))
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
