# Job application log

## 2026-11-01 — Workflow setup

- Created the job application skill at [skills/job-application-agent/SKILL.md](skills/job-application-agent/SKILL.md) and workspace routing in AGENTS.md.
- Extracted resume-xuewu.cai.pdf into candidate/baseline.txt; recorded its SHA-256 and provisional search preferences in candidate/preferences.json. Original resume preserved.
- Initialized persistent SQLite job ledger with append-only change events. No historical application data was provided; previously submitted applications outside this workspace must be imported/reconciled before applying to those roles.
- Search tracks: financial engineering leadership, mortgage/CRT and structured finance, quantitative risk, portfolio analytics, and trading technology.
- Provisional geography: U.S.; prioritize remote and DC/MD/Northern Virginia. Salary unrestricted pending user preference. No inferred federal-employer exclusion.
- Reviewed official Playwright and PDF skills; neither installed. TinyFish browser plugin found available and suggested; connection not confirmed.
- Site coverage plan saved in skills/job-application-agent/references/search-and-tools.md. This setup run did not search job listings or generate job-specific resumes; no job-search coverage is claimed.
- Applications prepared: 0. Submitted: 0. Pending submission confirmations: 0.
- Scheduling: not configured. Daily workflow instructions and persistent state are ready for invoked runs.
- Next run: read preferences, reconcile any prior applications, search the rolling two-calendar-month window, verify dates/open status, record unique matches, produce tailored packets, and request final confirmation before each submission.
- Validation: skill validator passed. Isolated ledger checks passed for cross-board duplicate detection, distinct requisitions, missing approval/receipt rejection, changed-packet approval rejection, and uncertain-submission retry prevention. Test records were not added to the real ledger.
- Workspace restriction: `.agents` is read-only in this session; skill stored under `skills/` and loaded through root AGENTS.md instead.

## 2026-11-01 — Search focus update

- Updated skill, search query families and candidate preferences to focus on fintech, finance, mortgage, banking, funds, IT, SDE, AI FDE (AI Forward Deployed Engineer), and AI engineer roles.
- Include suitable technology and AI roles outside finance; assess all matches against baseline evidence. AI tooling usage must not be rewritten as unverified production AI experience.
- This was a configuration update; no job searches or applications were performed.

## 2026-11-01 — Final submission checkpoint clarified

- Updated the skill and preferences to automatically prepare supported applications through the final review screen, then pause immediately before the last submission action for explicit user confirmation for that job.
- Covers Submit, Apply, Send, Finish and equivalent actions, including portals without separate review screens. No applications submitted in this update.

## 2026-11-01 — Two-step workflow update

- Step 1 now discovers new matching jobs, creates local tailored resumes, reconciles tracking and updates the selectable queue; it stops before portal preparation.
- Step 2 accepts one or multiple user-selected job IDs, prepares those applications, requests final confirmation of completed packets, and submits confirmed jobs. It may be repeated independently with different selections.
- Added persistent batch manifests, per-job outcomes, queue refresh rules and explicit “Already applied” warnings with skipped duplicate applications. Rejected/withdrawn applications retain submission history; uncertain submissions require reconciliation before retry.
- Updated candidate preferences and AGENTS.md to route future runs through these two steps. Initialized tracking/job-queue.md from the empty ledger (0 jobs); no discovery or submission performed.
- Validation: skill validator passed; reviewed both steps for selection boundaries, group confirmation, duplicate prevention and incremental continuation.

## 2026-11-01 — Git checkpoints required

- Updated skill, preferences and workspace instructions to commit and push at Step 1 completion/interruption and each Step 2 batch, preparation, pre-submission, outcome and end checkpoint; configuration updates also checkpoint.
- Git synchronization failures preserve local progress and pause further portal actions; application submission confirmation remains required.
- Current setup blocker: this workspace is not a Git repository, so no commit or GitHub push was possible. A GitHub repository destination and local Git initialization/upstream setup are needed. No destination was invented.

## 2026-11-01 — Git setup retry

- Confirmed the workspace is now a Git repository on main with origin git@github.com:gourmetcai-spec/nongovjobs.git.
- Existing commit e2a73fd already contains the skill, candidate files and tracking artifacts. Prior Git initialization blocker is resolved.
- Checkpoint: commit this log update and push main to origin, establishing its upstream; report the verified outcome in the session response.
- Retry outcome: local commit blocked by session filesystem permissions (`.git/index.lock`: Operation not permitted). Push of the existing main commit also failed because this session could not resolve github.com. No new commit or successful push is claimed. The log update remains saved locally; Git writes and GitHub network access are needed to finish synchronization.

## 2026-11-01 — GitHub destination saved

- Saved the user-designated repository git@github.com:gourmetcai-spec/nongovjobs.git in the skill and candidate preferences, using origin and the current intended branch (currently main).
- Added destination verification and missing-upstream setup instructions. Existing remote matches; session Git write and network restrictions remain unresolved.

## 2026-11-01 — Conversation summary saved

- Created summary.md with requirements, two-step operation, file layout, candidate matching rules, tracking/approval safeguards, Git destination and checkpoint policy, permission troubleshooting, tool status and recreation instructions.
- Prior Git checkpoint 1e304e1 was successfully pushed; initial Git sandbox failures were resolved through approved escalation for those commands.
- This documentation checkpoint does not perform job discovery or submit applications.

## 2026-11-01 — Customized resume PDF/folder requirement

- Configuration checkpoint 2026-11-01T19:26:32.126761-05:00. User explicitly requires a PDF for every customized resume in a meaningfully named folder. Updated the skill and candidate output policy to require a matching PDF for every source/revision, descriptive employer/role folders, preserved versions, final hashes, and incomplete status when PDF generation or review is blocked.
- Queue refresh now also builds [PDF index](applications/resume-index.md) with direct links to all saved resume versions and their named job folders. Application statuses/history preserved. No new discovery or Step 2 work performed.
- Prior checkpoint 9c68e58 was successfully pushed and its GitHub main SHA verified. Commit and push this configuration checkpoint to designated origin/main; report actual result in response.

## 2026-11-01 — Federal government and DMV search scope update

- User requested federal government jobs only in Washington DC, Maryland and Virginia; all other search criteria retained. Updated skill, official-source search guidance, saved preferences and queue scope notice. Excluded contractors, GSEs, private employers and state/local governments; surrounding communities outside DC/MD/VA no longer qualify. Existing remote eligibility rules, role/sector interests, two-month window and confirmation safeguards retained.
- Historical ledger and application artifacts preserved. Legacy statuses will be reconciled at the next Step 1; Step 2 now explicitly checks employer/geographic scope before preparation. No discovery or portal actions performed.
- Git destination mismatch: configured origin is gourmetcai-spec/govjobs, while saved policy specifies gourmetcai-spec/nongovjobs. Preserve local checkpoint and pause pushing/portal actions pending destination confirmation. Unrelated untracked .gitattributes and .gitignore left untouched.

## 2026-11-01 — Git destination confirmed

- User explicitly changed the destination to git@github.com:gourmetcai-spec/govjobs.git. Updated skill, candidate preferences and workspace summary; existing origin fetch/push URLs already match. This resolves the preceding destination mismatch.
- Includes the pending federal-only DC/MD/VA scope update. Skill validation and queue regeneration passed. Preserve unrelated untracked .gitattributes and .gitignore. Commit and push this configuration checkpoint to origin/main and verify remote SHA.

## 2026-11-01 — Copied non-government job history removed

- User explicitly requested removal of the non-government history copied into this federal-job workspace. This one-time cleanup supersedes normal history preservation for the imported non-government records only.
- Removed 54 non-government jobs, their 172 ledger events, associated application folders and tailored documents, and both copied discovery-run directories (including continuation cursors). No submitted or uncertain applications existed. Removed imported discovery sections from this log; workflow configuration history remains. Prior Git commits retain recovery copies.
- Kept the SQLite schema, baseline resume and extracted candidate facts, preferences, federal-only DC/MD/VA search rules, and application confirmation safeguards. Regenerated an empty queue and resume index; future run logs remain append-only. No discovery or portal actions performed.
- Previous configuration checkpoint 56b6a3e was pushed and verified on origin/main. Commit and push this cleanup checkpoint to the same confirmed govjobs repository.

## 2026-11-01 — Step 1 federal DMV discovery

- Checkpoint time 2026-11-01T19:55:28.492351-05:00; discovery window September 1–November 1 inclusive. Baseline SHA-256 unchanged; empty starting ledger after the user-requested cleanup. Prior cleanup ca94228 was pushed and remote SHA verified. Federal agencies only in DC/MD/VA; no imported non-government records restored.
- Performed 55 search-index query attempts across all eight role/sector tracks; tried USAJOBS native search/pagination and direct federal agency sources. Full source coverage remains partial due HTTP 403 and empty/inaccessible native search rendering. FHFA Current Openings reports no listings; FDIC careers is blocked. Exact [queries/audit](tracking/runs/2026-11-01-federal-step1/search-audit.json), [coverage](tracking/runs/2026-11-01-federal-step1/coverage.md) and [continuation](tracking/runs/2026-11-01-federal-step1/continuation.json) saved.
- Added 11 unique federal records: 1 eligible (FEMA IT Specialist APPSW, a5af83ea7ba6d744), 8 needs_verification, 2 skipped for restricted agency hiring paths. CIA mirrors reconciled to one control-number identity. No previously applied or uncertain submissions; no duplicates created. Unverified posting dates and mandatory education/experience remain explicit; details in match.md and the [queue](tracking/job-queue.md).
- Generated three tailored Markdown/PDF draft resumes for FEMA, CIA Data Engineer fa28275048f3ce60 and ICE Operations Research Analyst 4e066be541ca1382. All six pages rendered and visually reviewed; all 20 original experience bullets and artifact hashes validated; SQLite integrity OK. Drafts still need verified federal resume facts (including hours/week), CIA GPA and ICE course credits/calculus/date evidence as applicable. [Resume index](applications/resume-index.md) rebuilt.
- Missing candidate facts requested during this run; no answer received before this checkpoint. No assumptions were inserted. No Step 2 selections, application form filling, uploads, essays, assessments or submissions performed.
- Commit and push this Step 1 checkpoint to verified origin/main (gourmetcai-spec/govjobs); report actual commit and verified synchronization in the response.

## 2026-11-01 — Step 1 redo using concise CFTC format

- Checkpoint 2026-11-01T20:19:53.107014-05:00; window September 1–November 1. Baseline hash unchanged. Inspected user-provided Xuewu-Cai-Resume-CFTC-Systems-Risk-Analyst-889991400.pdf visually and by text/font extraction; saved its hash and format-only role in candidate preferences and skill. Prior checkpoint 85fe348 was pushed and remote SHA verified.
- Refreshed all 11 existing jobs; performed 16 new search-index queries and native/agency-source attempts across established tracks. Added 4 unique federal DMV records: CFTC f720af72449c48a0, USSC 16f54e578b2089d3, BEA 48ee9a40e142e566 (needs_verification), SSA b6f24c3fd93797f0 (skipped for restricted hiring path). USDA outside-DMV, BEA restricted companion and closed FDIC lead screened without duplicate records. Final counts: 15 jobs, 1 eligible, 11 needs_verification, 3 skipped. Coverage remains partial; [audit and coverage](tracking/runs/2026-11-01-federal-step1-redo/coverage.md) and [continuation](tracking/runs/2026-11-01-federal-step1-redo/continuation.json) saved.
- Revised FEMA, CIA and ICE resumes to concise one-page v2 drafts using the supplied layout. Selected supported bullets and condensed summaries/competencies; preserved all original v1 files byte-for-byte and retained version hashes. Avoided unsupported claims from the reference. All three pages visually reviewed, extracted-text/hash checks passed; baseline/reference unchanged and SQLite integrity OK. Missing required candidate facts and eligibility evidence remain blockers; no portal-ready claim. [Resume index](applications/resume-index.md) and [queue](tracking/job-queue.md) regenerated.
- No user selections, portal forms, uploads, assessments or submissions. Commit and push this Step 1/configuration checkpoint to confirmed govjobs origin/main; report actual result in response.
