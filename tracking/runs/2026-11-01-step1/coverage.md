# Step 1 search coverage — 2026-11-01

Window: September 1–November 1, 2026 inclusive. Baseline hash unchanged. All work is local discovery/tailoring; no Step 2 actions.

The user narrowed geography during this run to Maryland, Virginia, DC and nearby commutable communities. Initial nationwide results are retained as evidence; distant-office-only records were marked skipped. Remote roles must permit working from Maryland. The four eligible jobs all offer a DMV office.

## Board query audit

`per-source-search.json` contains exact finance/technology queries, date, page number (one search-index page per query), emitted result counts and access limits for each of LinkedIn, Indeed, Glassdoor, ZipRecruiter, Monster, CareerBuilder, Dice, eFinancialCareers, Built In and Wellfound. These 20 queries emitted 42 result records, including irrelevant/stale/category pages; this is not a count of unique jobs. `source-audit.json` records ten additional dated cross-track queries (September 1–November 1), which returned no results. No-result indexing does not mean no available jobs.

Initial queries used site restrictions and synonyms for financial engineering, mortgage/CRT, bank risk, portfolio/trading technology, Java/Python SDE, IT leadership and AI/FDE. Additional direct employer queries included Fannie Mae, Freddie Mac, Capital One, Guild Mortgage, AmeriSave, Citi, BlackRock, Wells Fargo, NinjaOne, Accellor, Barclays, Point72 and Two Sigma. Saved search groups: search0/search4, direct0/direct4, targets, capital, morecapital and canonical1. `dmv-search.json` saves the final four dated regional searches covering mortgage/finance, funds/trading, IT/SDE and AI/FDE. Query results are discovery leads only, not posting-date proof.

## Native pages, pagination and limitations

| Source | Pages / returned listing evidence | Limitation |
|---|---|---|
| LinkedIn / Indeed / Glassdoor | Public index queries only; emitted results saved per query | Native filters, authenticated views and pagination not covered; some snippets stale |
| ZipRecruiter | Mortgage Software Engineer and Mortgage AI Automation category pages surfaced | Syndication, no verified employer dates for those leads |
| Monster | Public searches attempted; direct Maryland senior-engineer search failed fetch | No native result total verified |
| CareerBuilder | Java developer page 1: displays 1,001 results; Accellor detail read | Page 2 fetch failed; displayed total is not assessed coverage |
| Dice | Virginia Java developer page: displays 298 results; Virginia FDE page: 123; AI/ML McLean detail | Only visible first-page listings; full native pagination/date filters not covered |
| eFinancialCareers | Query attempts; Point72 London and expired Aflac lead surfaced | London outside location; Aflac October 8 close date passed; no eligible job from this source |
| Built In | Remote Java category page 1 and three details read | Employer original dates required; NinjaOne reposts actually July 29/August 25 |
| Wellfound | Public search results include several FDE roles; Arize/Pallet details surfaced | Arize/Pallet postings outside window or production AI requirements; native board failed fetch |
| Capital One | Technology index pages 1 and 2, three full employer details | 50 pages advertised; remaining pages unassessed; each req distinct, overlapping descriptions flagged |
| Fannie Mae | Three public Workday description records; canApply=true, posted=true | Senior financial engineer requires undocumented Tableau; modeling director needs product-management evidence |
| Freddie Mac | Indexed technology page (11–20 of 25) surfaced | Direct page fetches failed; actual job dates/open status not verified |
| Guild Mortgage | Indexed employer lead | Live employer page unsupported-browser shell; date/open status/full text unverified |
| BlackRock | Public Workday job description/date/open status retrieved | Required technologies unverified; New York office-only excluded after location update |
| Barclays | Full employer description, date live October 29 | Mandatory transaction-execution scope unverified; distant office excluded after location update |
| Point72 | Employer URL returned general careers landing page; current description not verified | No verified original employer posting date; NY/Stamford excluded after location update |
| Citi | Full employer description dated October 19 | Anticipated October 23 close date passed; mandatory production ADK/MCP/Kubernetes unsupported; NJ office excluded |

Coverage is partial, not exhaustive. No CAPTCHA, login, access restriction or rate limit was bypassed. Remaining queries/cursors are explicit in continuation.json; use the updated DMV scope on continuation.

## Reconciliation and result counts

14 unique requisitions created; 0 pre-existing ledger jobs or prior applications. Four eligible local resumes (each two pages) generated, text checked and visually reviewed. Four records need verification and six are skipped after date/location reconciliation. Board aliases are saved against their existing stable IDs; no separate application identities were created for mirrors. Unknown dates stay out of eligibility. No application selected, uploaded or submitted.
