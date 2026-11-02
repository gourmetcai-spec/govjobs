# Job application agent — conversation and recreation summary

## Purpose and authoritative inputs

Create a reusable agent skill for Xuewu Cai's daily incremental job search and selected applications. Use `resume-xuewu.cai.pdf` as the authoritative resume baseline; preserve the original. This is a skill-driven workflow invoked in an agent session, not a standalone installed service. No daily scheduler has been configured.

Workspace: `/Volumes/WD512x2/home/gourmetcai/project/govjobs`.
GitHub: `git@github.com:gourmetcai-spec/govjobs.git`, remote `origin`, branch `main` tracking `origin/main`.

Resume format preference (2026-11-01): use `Xuewu-Cai-Resume-CFTC-Systems-Risk-Analyst-889991400.pdf` as a compact one-page layout/concision reference. Keep `resume-xuewu.cai.pdf` as the factual baseline; select supported relevant bullets and retain versions. Reference-only claims do not establish new candidate facts. Current tailored documents use v2; read the live ledger/queue for current job counts and status.

## User requirements

- Search major job sites for jobs posted within the past two months that match the candidate's background. Interpret this as two calendar months, inclusive, in America/New_York.
- Focus on fintech, finance, mortgage, banking, funds, IT, SDE/software engineering, AI FDE (AI Forward Deployed Engineer), and AI engineer roles. Technology and AI roles need not be at financial employers.
- Customize a truthful resume for each verified eligible match, save editable and PDF versions with meaningful employer/role/job-specific filenames, and log work in append-only `joblog.md`.
- Persist tracking across daily runs and prevent duplicate applications across sources, sessions and batches. Warn “Already applied” and skip an already-submitted job, including a previously rejected or withdrawn application.
- Automate supported application preparation, but always obtain explicit final confirmation immediately before the action that sends each application to the employer.
- Commit workflow changes and push to the designated GitHub repository at every checkpoint, including configuration updates.

## Two independent steps

### Step 1: discover, tailor and track

Search the full rolling window on each run to catch delayed indexing. Verify employer requisition identity, actual posting dates, open status and requirements. Deduplicate against all history, record evidence and gaps, prepare local tailored resumes, update the SQLite ledger, human-readable job queue and log, then commit and push. Present stable job IDs for selection and stop. Do not fill portal forms, upload to application sites or submit during this step.

### Step 2: apply only to user-selected jobs

Accept one job ID or a group of IDs. Persist a uniquely identified batch and per-job progress. Recheck duplicates, availability, eligibility and current application materials. Prepare selected jobs through the final review screen when browser tools permit. Show exact final packets and pause for confirmation. Initial selection is permission to prepare, not final approval to submit.

The user can confirm one completed packet or an explicitly enumerated group of completed packets. Store the approval reference/time and approved packet hash separately for each job. Material changes invalidate approval. Submit confirmed jobs one at a time and save evidence immediately. Step 2 can be repeated for different selections without rerunning Step 1. Resume a saved batch only on user instruction; do not reapply completed jobs.

Persist `submitting` before the external action. Set `applied` only with success evidence. On an ambiguous result use `submission_unknown`; reconcile portal status before retrying. A crash leaving `submitting` also requires reconciliation. A failed push is never a reason to repeat a submission.

## Baseline and matching rules

The resume describes financial engineering leadership, mortgage/CRT and structured finance, quantitative risk and forecasting, trading technology, Java/Python/C/C++, AWS, and documented AI tooling use. Assess each requirement against resume evidence. Never invent tools, projects, production AI systems, metrics, years, titles or credentials. Copilot usage does not establish production LLM/RAG, model-training or forward-deployment experience. CAIA Level I is not a full CAIA charter; CRT program size is not personally managed assets.

Current scope: federal government agency employment only in Washington DC, Maryland and Virginia. Exclude private employers, federal contractors, GSEs and state/local governments. Remote roles must permit working from Maryland/DMV without regular distant-office attendance; multi-location roles need a genuine offered DC/MD/VA work location. No salary floor is set. Do not infer relocation, clearance, demographic or sponsorship form answers.

Coverage targets: USAJOBS and official federal agency careers/announcement pages. General boards and search engines may supplement federal-only discovery; verify each result against its official announcement. Log query/page coverage and access limits.

## Files to recreate or restore

| Path | Purpose |
|---|---|
| `AGENTS.md` | Routes job tasks to the skill; preserves tracking, confirmation and Git checkpoint requirements |
| `skills/job-application-agent/SKILL.md` | YAML frontmatter (`name: job-application-agent`, scoped description) and complete workflow instructions |
| `skills/job-application-agent/references/search-and-tools.md` | Source coverage, query families and optional tools |
| `skills/job-application-agent/scripts/ledger.py` | Python stdlib SQLite CLI: `list`, `add job.json`, `update ID patch.json`; optional `--db` |
| `candidate/baseline.txt` | Extracted source resume text |
| `candidate/preferences.json` | Baseline hash, targets, confirmed federal/DMV scope, confirmation rules and Git settings |
| `tracking/jobs.sqlite3` | Authoritative jobs table and append-only change-event history |
| `tracking/job-queue.md` | Derived selectable queue with stable IDs, statuses, fit/gaps and artifact links |
| `tracking/batches/<timestamp>__<unique-suffix>.json` | Created per Step 2 selection; selected IDs, request reference, progress, approvals and outcomes |
| `applications/YYYY-MM-DD__employer__role__ledger-id/` | Per-job evidence and tailored documents |
| `joblog.md` | Append-only run/checkpoint history, counts, gaps and outcomes |

Per-job artifacts: `job.md`, `match.md`, `application.json`, and `resume-xuewu-cai__employer__role__req-or-id__v1.md` plus the same basename `.pdf`. Preserve revisions and reviewed hashes. PDFs must contain selectable text and pass extraction and visual layout checks.

Ledger identity prefers employer plus requisition ID, otherwise canonical URL. Strip tracking parameters but preserve identity-bearing URL fields and ATS tenants. Manually reconcile cross-board aliases, employer variations and ambiguous reposts. Keep all historical submissions even after the discovery window expires. The helper enforces several status/approval checks; semantic matching, truthful evidence and portal approval boundaries also depend on the skill instructions.

The skill is under `skills/` because this session initially prohibited writing `.agents/`. Root `AGENTS.md` supplies workspace routing. Restore this arrangement when recreating; do not assume global skill installation.

## Git checkpoints and permissions

Commit and push at Step 1 completion/interruption; Step 2 batch creation; each prepared packet awaiting confirmation; saved approval and pre-submission state; each submitted/uncertain/skipped/blocked result; and Step 2 completion/interruption. Also checkpoint skill/configuration updates.

Finish local writes and close SQLite writers before staging; handle WAL checkpoints if used. Review and stage only intended workflow files. Never commit credentials, browser sessions or secret-bearing artifacts. Verify destination and upstream; do not force-push, discard state or silently merge conflicting SQLite ledgers. If commit or push fails, preserve state and pause further portal actions until synchronized or the user changes that requirement. No empty commits are needed when unchanged; verify/push pending commits instead.

Initial Git failures were caused by sandbox denial of `.git/index.lock` and restricted network access. Normal directory ownership was already correct (`gourmetcai`, UID 501; group `staff`, GID 20); chmod/chown was not the fix. After permission changes, approved escalated Git commands succeeded. Do not assume future sessions inherit these approvals; request scoped escalation when required, rather than repeatedly reporting a sandbox failure if escalation is available.

Verified successful checkpoint before this summary: `1e304e1` (`jobs: configure GitHub checkpoint destination`) pushed to `origin/main`; local and remote-tracking hashes matched and the tree was clean. Git author configuration observed: Vivian Cai; this is commit metadata, not proof of the SSH-authenticated GitHub identity.

## Tools and validation

The skill-creator skill guided creation; plugin-management was used for discovery. Local Python had `pypdf` and `reportlab` available at setup. Recheck dependencies in a new environment.

TinyFish was suggested as an optional browser integration, but connection was not confirmed. Official Playwright and PDF skills were reviewed, not installed. Browser automation requires a working tool and authenticated site access; otherwise retain a manual-ready packet without claiming submission. Use secure login flows rather than logging credentials.

Skill validation passed. Isolated ledger checks covered cross-board duplicates, distinct requisitions, missing approval/receipt rejection, changed-packet rejection and uncertain-submission retry prevention. On 2026-11-01, the user requested removal of copied non-government job history. All 54 imported jobs and their related events, application folders and discovery runs were removed; the ledger and queue are empty. No applications had been submitted. Do not restore copied records or resume old non-government discovery tasks. Preserve new federal job history across future runs.

## Exact invocation prompts

Step 1 (paste into the agent session; this is a natural-language prompt, not a shell command):

```text
Run Step 1 using skills/job-application-agent/SKILL.md. Search for new matching jobs from the past two months, tailor resumes, update tracking/job-queue.md, the ledger and joblog.md, then commit and push to GitHub. Stop before Step 2.
```

Step 2:

```text
Run Step 2 for job IDs <id-1>, <id-2>, and <id-3>. Prepare their applications and show me the final review packets. Stop for my final confirmation before submission. Commit and push at every checkpoint.
```

After reviewing final packets:

```text
Submit the reviewed applications for <id-1> and <id-2>.
```

Resume:

```text
Resume Step 2 batch <batch-id>. Check saved progress and reconcile uncertain submissions before continuing.
```

## Recreation request

Use this summary, the original PDF, and any saved Git/tracking history to recreate the files above as a workspace skill. Preserve the two-step separation, user-selected batches, exact-packet final confirmation, truthful tailoring, permanent duplicate prevention, and Git checkpoints. Validate the skill and any regenerated helper behavior. Do not run job discovery, submit applications, create a scheduler or invent prior history merely as part of recreation.
