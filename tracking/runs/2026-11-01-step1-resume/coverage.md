# Continued Step 1 — 2026-11-01

Resumed the saved checkpoint e616885. Window September 1–November 1 inclusive; confirmed DMV/nearby commuting scope preserved. No portal preparation, uploads or submissions.

## Work completed

- All 10 major board sources queried across each of eight track families: 80 exact dated query attempts in [board-search-audit.json](board-search-audit.json). Twenty groups emitted 240 result records/URLs, including categories, irrelevant, stale and non-job pages. These are discovery leads, not 240 confirmed jobs. Combined response counts are per group of four queries; native-board totals are not implied. [board-leads.json](board-leads.json) preserves returned URLs for triage.
- Fannie Mae native public index offsets 0/20/40: 55 unique advertised requisitions screened. 25 potentially relevant full public Workday descriptions assessed; nonmatching specialties and out-of-window details recorded in [triage inventory](triage-inventory.json). API total was 55 on offset 0 and 0 on later offsets despite returning 20/15 results; pagination used the initial total and actual returned records.
- Capital One native technology page 3: 15 displayed roles; 13 technical descriptions assessed, 2 sales/DBA titles screened. Four new eligible roles, remaining details have unsupported specialized tenure/production ML or distant office requirements. Pages 4–50 and earlier page 2 details remain incomplete; no hidden match cap.
- T. Rowe Price native Software search offsets 0/20: 27 displayed results screened. 20 full descriptions assessed including quantitative-investment analyst. Investment risk SWE, multi-asset SWE, fixed-income technology analyst and associate SWE eligible; mandatory production AI/agent frameworks, named Azure/AWS tooling or optimization requirements remain explicit gaps for others. Oracle/architecture postings outside window excluded.
- Freddie Mac JR17471 full employer JobPosting schema recovered, dated October 19, McLean. Current employees directed to internal career site; baseline says current employee, so external submission destination must not be used without reconciliation in selected Step 2.
- Accellor 5C44EACEF1 source blocker resolved using employer's public Workable description endpoint: published October 22, state published, Maryland remote location. Still needs verification for Cursor, Spring/cloud tenure, Azure tooling and publication history.

## Source limitations

CareerBuilder page 2 returned HTTP 403; no access restriction bypassed. Campbell public careers page linked ADP, whose public board returned a supported-browser shell. Guild employer page still returns unsupported-browser shell. Randstad 1345736 and Allegis 2318 returned HTTP 410, so indexed snippets are not treated as open jobs. Blue Origin R71045 and older T. Rowe Price 82285 detail returned HTTP 403. Every attempted fetch records URL, effective URL, time and outcome in `*-fetch.json`. Public JSON description endpoints were read-only; no application forms were filled or documents uploaded.

Board search indexing and native pagination remain partial. Remaining queries/cursors and unresolved sources are in [continuation](continuation.json).

## Local results and validation

40 new unique ledger records: 13 eligible, 23 needs_verification, 4 skipped. One existing Accellor record refreshed; Fannie JR2899 existing ID recognized while screening. No applied or uncertain submission records exist; no history reset or duplicate application created. Overall ledger: 54 records, 17 eligible, 27 needs_verification, 10 skipped.

13 new two-page resumes produced, with editable Markdown, full employer descriptions, evidence/gaps assessments and manifests containing final SHA-256 hashes. All 26 new PDF pages rendered and visually checked: no clipping, overlap or blank pages. All 17 eligible resumes pass text checks for each of the 20 baseline experience bullets, complete degrees/history, and scoped financial metrics. Baseline PDF unchanged. Every ledger status and artifact hash agrees with its packet manifest. [Validation record](validation.json).

Anaplan associate, whole-loan trader and associate SWE are marked lower priority due to scope/pay relative to current Director; no user salary floor inferred. All specialty gaps remain visible. Coverage is not exhaustive; Step 2 remains unstarted.
