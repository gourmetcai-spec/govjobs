# Job application workspace

For daily job discovery, resume tailoring, application preparation, or application status work, read `skills/job-application-agent/SKILL.md` and follow it. The baseline is `resume-xuewu.cai.pdf`. Preserve `tracking/jobs.sqlite3`, application artifacts, and the append-only `joblog.md` across runs. Submission always requires the user's final confirmation for the exact application.

Use the two-step workflow: Step 1 discovers jobs and updates local resumes, the ledger, job queue and log; Step 2 prepares and submits only user-selected jobs or batches, with final confirmation. Step 2 is repeatable independently. Warn and skip jobs already applied to; reconcile uncertain submissions before retrying.

At every Step 1 and Step 2 checkpoint, and after workflow configuration updates, commit the changed workflow artifacts and push to the configured GitHub branch. Follow the Git checkpoint section of the skill. Preserve local outcomes and report missing Git setup or synchronization failures; pause further portal actions until synchronized.
