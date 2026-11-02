# Search coverage and integrations

Search federal government agency jobs only. Verify the employing agency on the official announcement; private employers, contractors, GSEs (including Fannie Mae and Freddie Mac), and state/local governments are excluded even if the work serves a federal client.

| Source | Entry point / role |
|---|---|
| USAJOBS | usajobs.gov — primary federal discovery source; search each track in DC, Maryland and Virginia |
| Federal agency careers | Official agency careers pages — supplement USAJOBS, including direct agency hiring announcements; verify federal employment |
| Agency application systems | Follow official announcement links for requirements, posting dates, open status and application destination |
| General job boards / search engines | Supplemental discovery of federal agency announcements only; verify every result on an official federal source |

Paginate available results and log queries, filters, pages, counts and access limits. Coverage is not exhaustive merely because a few indexed results were found. Record unavailable sources and continue accessible official sources. Preserve the existing two-calendar-month window and all other matching criteria. Record federal announcement number, series/grade, hiring path, specialized experience, education, citizenship, clearance and required documents when stated. Assess mandatory eligibility against verified candidate evidence; leave unsupported eligibility unresolved.

## Query families

Search each family independently with relevant synonyms; do not require financial-sector keywords for all IT, SDE or AI results. Apply these functional/title synonyms within federal agencies; use agency terminology such as IT specialist, computer scientist, financial analyst and operations research analyst as appropriate.

| Focus | Example queries / title variants |
|---|---|
| Fintech / finance | financial engineering director; quantitative engineering lead; fintech engineering; financial technology |
| Mortgage | mortgage analytics; credit risk transfer; STACR; structured finance valuation; MBS analytics |
| Banking | bank technology; quantitative risk director; capital planning; CECL; enterprise forecasting |
| Funds | hedge fund engineer; investment technology; asset management software engineer; portfolio risk analytics; quantitative developer; trading systems |
| IT | enterprise technology; platform engineer; cloud engineer; engineering manager; technology director |
| SDE | Software Development Engineer; SDE; software engineer; senior/staff/principal software engineer; backend engineer; Java developer; Python developer |
| AI FDE | AI Forward Deployed Engineer; forward deployed engineer; forward deployed software engineer; applied AI deployment engineer |
| AI engineer | AI engineer; applied AI engineer; generative AI engineer; LLM engineer; AI software engineer |

The terms expand discovery, not the candidate's claimed qualifications. Evaluate required experience individually, especially production AI systems and customer-facing deployment. Include both engineering leadership and suitable senior individual-contributor roles.

Geography confirmed by the user on 2026-11-01: Washington DC, Maryland and Virginia only. Exclude surrounding communities outside these jurisdictions. Search DMV offices and remote roles that explicitly allow working from Maryland/DMV. Multi-location roles qualify when a DMV office is an offered location. Do not search nationwide on-site/hybrid roles or assume relocation. Use source date filters plus official announcement date verification; when only a one-month filter exists, search an additional older slice to cover the full two-month window.

## Tools reviewed at setup (2026-11-01)

- Built-in web search: public discovery and source verification, not authenticated form submission.
- TinyFish: plugin directory returned an available, unconnected cloud browser integration supporting navigation and form filling. Suggested to the user; NOT installed or connected at setup. Use only after connection is verified, and enforce per-application final confirmation. Do not send an open-ended “apply to everything” task to an external browser agent; require a stop before Submit.
- Official Playwright skill: https://github.com/openai/skills/blob/main/skills/.curated/playwright/SKILL.md — browser navigation/form filling when local prerequisites and site access are available. Reviewed, not installed.
- Official PDF skill: https://github.com/openai/skills/blob/main/skills/.curated/pdf/SKILL.md — document generation and visual review. Reviewed, not installed.

No external plugin is required for local tracking or tailoring. Recheck available tools each run instead of assuming these connection states remain current. Prefer a connected service integration; if none can operate the application portal, leave a manual-ready packet. Do not store applicant resumes in public repositories or upload them to unrelated third parties.
