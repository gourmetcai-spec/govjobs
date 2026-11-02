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

## 2026-11-01 — Step 1 discovery and DMV location update

- Checkpoint time: 2026-11-01T18:35:54.063282-05:00; window September 1–November 1, 2026 inclusive. Baseline SHA-256 unchanged. Previous checkpoint a6e0cdf was already synchronized at start.
- User confirmed geography: Maryland, Virginia, Washington DC and surrounding commutable areas. Updated skill, search guidance and candidate preferences. Remote roles require Maryland/DMV eligibility; multi-location roles require an offered DMV office. Distant required-office roles reconciled to skipped without deleting history. Work arrangement and salary preferences remain unresolved.
- Sources: all ten major boards queried for finance and technology synonyms; 20 per-source queries emitted 42 result records (including categories/irrelevant/stale results), ten dated cross-track queries returned zero. Supplemented direct employers and four final DMV-specific query families. Detailed queries, filters, pages, counts and limitations: [coverage](tracking/runs/2026-11-01-step1/coverage.md), [audit](tracking/runs/2026-11-01-step1/per-source-search.json). Public-index coverage is partial, not exhaustive; [remaining queries/cursors](tracking/runs/2026-11-01-step1/continuation.json) saved for continuation.
- Ledger: 14 new unique requisitions, 0 previously tracked jobs, 0 historical duplicate applications; final counts 4 eligible, 4 needs_verification, 6 skipped. Mirrors reconciled as aliases. NinjaOne original dates July 29/August 25 excluded despite recent repost labels; Citi anticipated close date passed. Fannie Mae employer date overrides conflicting board date.
- Tailored local Markdown/PDF resumes and complete job/match/application records created for 4 eligible jobs: Fannie Mae JR2927 (4ca4ebfe5bc74f14), Capital One R1001301 (850269b52b84dff8), R1004789 (bb73fca27d43900b), R1004785 (c7bfa65609f82cce). Each PDF has 2 selectable-text pages; all 8 rendered and visually reviewed without clipping, overlap or blank pages. Paths and SHA-256 hashes saved in packet manifests and ledger.
- Gaps retained: Capital One mandatory cloud tenure needs confirmation; Fannie Mae JR2899 Tableau and JR2677 product-team experience unverified; Guild/Accellor source verification blocked. Source documents and all local outcomes preserved.
- Rebuilt [selectable queue](tracking/job-queue.md). Added queue regeneration helper and corrected ledger CLI path in skill. No Step 2 batch, form filling, uploads, confirmations or submissions performed.
- Git checkpoint: commit these Step 1 and workflow-configuration artifacts and push main to the verified designated origin; report actual SHA and remote synchronization result in the response.

## 2026-11-01 — Step 1 resumed after interruption

- Timestamp 2026-11-01T19:01:44.765414-05:00; rolling window September 1–November 1 inclusive; confirmed Maryland/Virginia/DC and commutable surroundings retained. Baseline hash unchanged. Prior commit e616885 successfully pushed and GitHub SHA verified at the preceding checkpoint.
- Resumed saved source/query tasks. Queried all 10 major sources across all 8 tracks (80 dated search-index query attempts; 240 emitted records including category/non-job/irrelevant results). Fannie Mae native index all 55 displayed requisitions screened over offsets 0/20/40; 25 relevant descriptions assessed. T. Rowe Price Software search all 27 displayed results screened over offsets 0/20; 20 descriptions including quantitative analyst assessed. Capital One page 3 reviewed with 13 technical descriptions.
- Created 40 unique new records: 13 eligible, 23 needs_verification, 4 skipped; refreshed existing Accellor cf3386db14e68153 without changing identity. Overall ledger 54 records: 17 eligible, 27 needs_verification, 10 skipped. Fannie JR2899 recognized as existing; no duplicate application or submission history changes.
- New eligible packets include Freddie Mac JR17471, Fannie Mae JR2945/JR2961/JR2963/JR2965, Capital One R1001156/R1004638/R1004791/R1004711, T. Rowe Price 82379/82649/83573/83767. Full IDs and PDF links in [queue](tracking/job-queue.md); per-run outcomes in [outcomes](tracking/runs/2026-11-01-step1-resume/outcomes.json).
- Generated 13 tailored Markdown/PDF resumes; all 26 new PDF pages rendered and visually checked. Text verification confirms all 20 baseline experience bullets in each of 17 eligible resumes; original employers/titles/dates/degrees preserved, no production AI or Palantir experience invented. Lower-scope/pay roles explicitly flagged. Final artifact hashes and ledger/packet agreement validated; SQLite integrity ok.
- Source blockers: CareerBuilder 403; Guild and Campbell ADP unsupported-browser shell; Randstad/Allegis 410; Blue Origin/older T. Rowe detail 403. No restriction bypass. Accellor date/open status now verified but mandatory skills unverified. Freddie current employee internal application route flagged for future selected Step 2.
- [Coverage and limits](tracking/runs/2026-11-01-step1-resume/coverage.md) and [remaining work/cursors](tracking/runs/2026-11-01-step1-resume/continuation.json) saved. Board pagination/search indexing remain partial; no exhaustive coverage claimed. Queue regenerated from ledger. No Step 2 selections, uploads, form filling or submissions.
- Checkpoint: commit and push resumed Step 1 artifacts to designated origin/main; report actual SHA and verified remote outcome in response.

## 2026-11-01 — Customized resume PDF/folder requirement

- Configuration checkpoint 2026-11-01T19:26:32.126761-05:00. User explicitly requires a PDF for every customized resume in a meaningfully named folder. Updated the skill and candidate output policy to require a matching PDF for every source/revision, descriptive employer/role folders, preserved versions, final hashes, and incomplete status when PDF generation or review is blocked.
- Verified all 17 existing customized resumes already have two-page, selectable-text PDFs beside their Markdown files in date/employer/role/ledger-ID folders. All recorded paths and SHA-256 hashes match both the ledger and packet manifests. Existing visual reviews remain valid; no resume content or PDF bytes changed. No missing PDF needed backfilling.
- Queue refresh now also builds [PDF index](applications/resume-index.md) with direct links to all saved resume versions and their named job folders. Application statuses/history preserved. No new discovery or Step 2 work performed.
- Prior checkpoint 9c68e58 was successfully pushed and its GitHub main SHA verified. Commit and push this configuration checkpoint to designated origin/main; report actual result in response.

## 2026-11-01 — Federal government and DMV search scope update

- User requested federal government jobs only in Washington DC, Maryland and Virginia; all other search criteria retained. Updated skill, official-source search guidance, saved preferences and queue scope notice. Excluded contractors, GSEs, private employers and state/local governments; surrounding communities outside DC/MD/VA no longer qualify. Existing remote eligibility rules, role/sector interests, two-month window and confirmation safeguards retained.
- Historical ledger and application artifacts preserved. Legacy statuses will be reconciled at the next Step 1; Step 2 now explicitly checks employer/geographic scope before preparation. No discovery or portal actions performed.
- Git destination mismatch: configured origin is gourmetcai-spec/govjobs, while saved policy specifies gourmetcai-spec/nongovjobs. Preserve local checkpoint and pause pushing/portal actions pending destination confirmation. Unrelated untracked .gitattributes and .gitignore left untouched.

## 2026-11-01 — Git destination confirmed

- User explicitly changed the destination to git@github.com:gourmetcai-spec/govjobs.git. Updated skill, candidate preferences and workspace summary; existing origin fetch/push URLs already match. This resolves the preceding destination mismatch.
- Includes the pending federal-only DC/MD/VA scope update. Skill validation and queue regeneration passed. Preserve unrelated untracked .gitattributes and .gitignore. Commit and push this configuration checkpoint to origin/main and verify remote SHA.
