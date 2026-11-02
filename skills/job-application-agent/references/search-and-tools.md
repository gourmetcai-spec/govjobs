# Search coverage and integrations

Search source matrix each run (adapt to verified geographic preferences):

| Source | Entry point / role |
|---|---|
| LinkedIn Jobs | linkedin.com/jobs — title variants and locations |
| Indeed | indeed.com — title variants and locations |
| Glassdoor | glassdoor.com/Job — verify mirrored roles against employer |
| ZipRecruiter | ziprecruiter.com — deduplicate syndicated listings |
| Monster | monster.com — check availability and redirects each run |
| CareerBuilder | careerbuilder.com — check availability and redirects each run |
| Dice | dice.com — engineering, quant and finance technology |
| eFinancialCareers | efinancialcareers.com — quant, risk, structured finance |
| Built In | builtin.com/jobs — finance technology and leadership |
| Wellfound | wellfound.com/jobs — relevant startup roles |
| Employer careers / ATS | Authoritative requisitions, posting dates, open status and application destination; Greenhouse, Lever, Workday, iCIMS and employer-specific sites |

These are coverage targets, not a guarantee that all listings can be accessed or every market is covered. Log redirects/retired sources rather than inventing results. Supplement with regional/specialist boards when useful. Include direct employer searches for fintech firms, financial institutions, mortgage companies, banks, hedge funds, investment funds, asset managers, IT companies and AI companies. Do not exclude Freddie Mac or other GSEs based on directory name.

## Query families

Search each family independently with relevant synonyms; do not require financial-sector keywords for all IT, SDE or AI results.

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

Geography confirmed by the user on 2026-11-01: Maryland, Virginia, Washington DC and nearby commutable surrounding communities. Search DMV offices and remote roles that explicitly allow working from Maryland/DMV. Multi-location roles qualify when a DMV office is an offered location. Do not search nationwide on-site/hybrid roles, assume relocation, or include all of a neighboring state merely because it borders the region. Use board date filters plus employer date verification; when only a one-month filter exists, search an additional older slice to cover the full two-month window.

## Tools reviewed at setup (2026-11-01)

- Built-in web search: public discovery and source verification, not authenticated form submission.
- TinyFish: plugin directory returned an available, unconnected cloud browser integration supporting navigation and form filling. Suggested to the user; NOT installed or connected at setup. Use only after connection is verified, and enforce per-application final confirmation. Do not send an open-ended “apply to everything” task to an external browser agent; require a stop before Submit.
- Official Playwright skill: https://github.com/openai/skills/blob/main/skills/.curated/playwright/SKILL.md — browser navigation/form filling when local prerequisites and site access are available. Reviewed, not installed.
- Official PDF skill: https://github.com/openai/skills/blob/main/skills/.curated/pdf/SKILL.md — document generation and visual review. Reviewed, not installed.

No external plugin is required for local tracking or tailoring. Recheck available tools each run instead of assuming these connection states remain current. Prefer a connected service integration; if none can operate the application portal, leave a manual-ready packet. Do not store applicant resumes in public repositories or upload them to unrelated third parties.
