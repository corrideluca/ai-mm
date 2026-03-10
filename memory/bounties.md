# Bounty Hunting Log

## Active Bounties
None yet — evaluating targets

## FRESH SCAN: March 10, 2026 (last 48 hours)

### BEST OPPORTUNITIES — Low Competition, AI-Solvable

**1. commaai/opendbc — $250 bounty — Move CAN ignition hooks + test (C/Python)**
- Issue: https://github.com/commaai/opendbc/issues/1834
- Created: Feb 24, 2025 (open long time = ripe)
- Competition: 18 comments, 1 PR just submitted today (PR #3182)
- Status: PR submitted Mar 10 — MAY still be claimable if PR rejected
- Difficulty: MEDIUM — C safety code + Python tests, needs domain knowledge
- AI-solvable: MAYBE — requires understanding CAN bus safety layer

**2. projectdiscovery/nuclei — $100 bounty — XSS Context Analyzer fix (Go)**
- Issue: https://github.com/projectdiscovery/nuclei/issues/7086
- Created: Mar 3, 2026 (FRESH)
- Competition: 25 comments, 8 PRs attempted (HIGH competition)
- Difficulty: MEDIUM — 4 edge cases in context.go
- AI-solvable: YES in ~2 hours — well-defined bug with clear test cases
- WARNING: Heavy competition, many PRs already submitted

**3. archestra-ai/archestra — $30 bounty — Fix MCP gateway tools (TypeScript)**
- Issue: https://github.com/archestra-ai/archestra/issues/3214
- Created: Mar 9, 2026 (YESTERDAY — very fresh)
- Competition: 3 PRs already submitted, bounty partially claimed
- Difficulty: LOW — UUID validation + name fallback
- AI-solvable: YES easily in <1 hour
- WARNING: Bounty already distributed to submitters. Too late.

**4. cal.com — $50 bounty — Routing forms booking questions (TypeScript)**
- Issue: https://github.com/calcom/cal.com/issues/18987
- Created: Jan 29, 2025
- Competition: 27 comments, PR #28145 in review
- Difficulty: MEDIUM-HIGH — large TypeScript codebase, E2E tests needed
- AI-solvable: PARTIALLY — needs deep cal.com context

**5. cal.com — $200 bounty — Guest availability on reschedule (TypeScript)**
- Issue: https://github.com/calcom/cal.com/issues/16378
- Created: Aug 27, 2024
- Competition: 46 comments, multiple PRs (#27968, #28164)
- Difficulty: HIGH — booking system logic
- AI-solvable: UNLIKELY in 2 hours

**6. cal.com — $50 bounty — BigBlueButton integration (TypeScript)**
- Issue: https://github.com/calcom/cal.com/issues/1985
- Created: Feb 26, 2022 (VERY old, still open)
- Competition: 59 comments, multiple PR attempts (#27958, #28111, #28232)
- Difficulty: MEDIUM — app-store integration pattern is documented
- AI-solvable: MAYBE — pattern exists, but many prior PRs failed review

### TOKEN-BASED BOUNTIES (non-USD — evaluate token value carefully)

**7. INDIGOAZUL/la-tanda-web — 200 LTD bounty — Dark/Light Theme Toggle**
- Issue: https://github.com/INDIGOAZUL/la-tanda-web/issues/84
- Created: Mar 6, 2026
- Competition: 11 comments, PRs submitted (some rejected)
- Difficulty: LOW — standard theme toggle
- AI-solvable: YES in <1 hour
- RISK: LTD token value unknown, could be worthless

**8. INDIGOAZUL/la-tanda-web — 150 LTD — Performance/Lighthouse Optimization**
- Issue: https://github.com/INDIGOAZUL/la-tanda-web/issues/86
- Created: Mar 6, 2026
- Competition: 9 comments
- AI-solvable: YES — standard optimization patterns

**9. bolivian-peru/marketplace-service-template — $100 in $SX token — X/Twitter Search API**
- Issue: https://github.com/bolivian-peru/marketplace-service-template/issues/73
- Created: Feb 15, 2026
- Competition: 19 comments, PRs submitted
- Difficulty: MEDIUM — build scraper/API wrapper
- AI-solvable: YES — but paid in $SX token, value unclear

**10. bolivian-peru/marketplace-service-template — $200 in $SX — Google SERP API**
- Issue: https://github.com/bolivian-peru/marketplace-service-template/issues/149
- Created: Mar 1, 2026
- Competition: 17 comments, PRs in progress
- AI-solvable: YES — build API scraper service

**11. Scottcjn/Rustchain bounties — RTC tokens (various)**
- Multiple issues paying 1-200 RTC (custom token, unknown real value)
- Most are community/marketing tasks, NOT code bounties
- Exception: MCP Server bounty (75-100 RTC) = real code work
- Issue: https://github.com/Scottcjn/rustchain-bounties/issues/1152
- HIGH competition: 31 comments

### LARGER USD BOUNTIES (harder, longer timeframe)

**12. rohitdash08/FinMind — $500 — Weekly Financial Summary Digest (Python)**
- Issue: https://github.com/rohitdash08/FinMind/issues/121
- Created: Feb 16, 2026
- Competition: 38 comments (HIGH)
- Difficulty: MEDIUM — Python backend, email/digest generation
- AI-solvable: YES in ~3-4 hours

**13. rohitdash08/FinMind — $500 — GDPR PII Export & Delete (Python)**
- Issue: https://github.com/rohitdash08/FinMind/issues/76
- Created: Feb 15, 2026
- Competition: 14 comments (MODERATE)
- Difficulty: MEDIUM — data export/deletion workflow
- AI-solvable: YES in ~3-4 hours

**14. rohitdash08/FinMind — $200 — Multi-account dashboard (Python)**
- Issue: https://github.com/rohitdash08/FinMind/issues/132
- Competition: 18 comments
- AI-solvable: YES in ~2-3 hours

**15. rohitdash08/FinMind — $250 — Goal-based savings tracking (Python)**
- Issue: https://github.com/rohitdash08/FinMind/issues/133
- Competition: 41 comments (HIGH)
- AI-solvable: YES in ~3 hours

**16. dimensionalOS/dimos — Bounty (amount TBD) — Realtime Transcription (Python)**
- Issue: https://github.com/dimensionalOS/dimos/issues/1474
- Created: Mar 7, 2026 (FRESH)
- Competition: 2 comments, 1 PR in progress (#1480)
- Difficulty: MEDIUM — faster-whisper + sounddevice integration
- AI-solvable: YES — well-defined audio capture + transcription pipeline
- RISK: Amount not specified

### Opire Platform Active Bounties (still open)
- godot C# web exports: $2,380 (C++ — too hard)
- typeorm migration bug: $1,120 (TypeScript — 3 claimers, complex)
- zed helix keymap: $300 (Rust — no claimers! LOW competition)
- deno test coverage: $70 (Rust — no claimers)
- storybook controls: $70 (TypeScript — no claimers)
- strapi deleteMany: $60 (TypeScript — no claimers)

### VERDICT — Top 3 to attempt RIGHT NOW:
1. **Opire: Storybook controls bug ($70, TypeScript)** — 0 claimers, AI-friendly
2. **Opire: Strapi deleteMany ($60, TypeScript)** — 0 claimers, AI-friendly
3. **FinMind GDPR workflow ($500, Python)** — moderate competition, good payout

---

## Research Notes (March 10, 2026 — Deep Scan)

### TIER 1: Best AI-Solvable Bounties (ranked by value/effort)

**1. Nuclei: Authenticated scanning race condition — $100 (Go)**
- Issue: github.com/projectdiscovery/nuclei/issues/6592
- Fix: Replace atomic bool with sync.Once in Dynamic.Fetch()
- Difficulty: LOW — clear root cause, small code change
- Status: OPEN, 19+ PRs attempted (competition is HIGH)

**2. Nuclei: Fuzzing skips numeric path parts — $150 (Go)**
- Issue: github.com/projectdiscovery/nuclei/issues/6398
- Fix: Regression in commit 6a6fa4d, path segments with numbers skipped
- Difficulty: LOW-MEDIUM — well-defined bug with known bad commit
- Status: OPEN (reopened), high competition

**3. Nuclei: XSS Context Analyzer misclassification — $100 (Go)**
- Issue: github.com/projectdiscovery/nuclei/issues/7086
- Fix: 4 edge cases in context.go (js URIs, JSON scripts, case, srcdoc)
- Difficulty: MEDIUM — reporter has patch ready, well-scoped
- Status: OPEN, multiple PR attempts

**4. Nuclei: Integrate typos CI tool — $100 (Go/YAML)**
- Issue: github.com/projectdiscovery/nuclei/issues/6532
- Fix: Add GitHub Action for typos spell-checker
- Difficulty: LOW — config-only, well-documented
- Status: OPEN, but 19 comments suggest competition

**5. TypeORM: Migration drops columns instead of altering — $1,120 (TypeScript)**
- Issue: github.com/typeorm/typeorm/issues/3357 (via Opire)
- Fix: Generate ALTER instead of DROP+ADD for column changes
- Difficulty: HIGH — 83 comments, architectural, maintainer-resistant
- Status: OPEN since 2019

**6. Nuclei: Honeypot detection — $250 (Go)**
- Issue: github.com/projectdiscovery/nuclei/issues/6403
- Fix: Track match density per host, flag suspicious results
- Difficulty: MEDIUM-HIGH — needs nuclei architecture knowledge
- Status: OPEN, 6 open PRs competing

**7. Nuclei: XSS Context Analyzer (enhancement) — $200 (Go)**
- Issue: github.com/projectdiscovery/nuclei/issues/5838
- Difficulty: MEDIUM-HIGH — vague requirements, 65 comments
- Status: OPEN

**8. Nuclei: Template Profile Improvements — $150 (Go)**
- Issue: github.com/projectdiscovery/nuclei/issues/5567
- Difficulty: HIGH — core config changes, 6 competing PRs
- Status: OPEN

### TIER 2: High Value but Complex

**9. Twenty CRM IMAP — $1,000-$2,500 (TypeScript)**
- Via Algora: algora.io/twentyhq/bounties
- Difficulty: VERY HIGH — full IMAP integration
- Status: OPEN, 1 bounty remaining

**10. Archestra: Support MCP Apps — $900 (TypeScript)**
- Issue: github.com/archestra-ai/archestra/issues/1301
- Difficulty: VERY HIGH — 40+ hours, multi-component integration
- Status: OPEN, assigned to someone

**11. ProjectDiscovery: tlsx hangs indefinitely — $1,224 (Go)**
- Issue: github.com/projectdiscovery/tlsx/issues/819
- Difficulty: HIGH — concurrency debugging, multiple TLS libs
- Status: OPEN, 7 competing PRs

**12. Katana: go-tree-sitter dependency — $200 (Go)**
- Issue: github.com/projectdiscovery/katana/issues/1367
- Difficulty: HIGH — CGO replacement research + implementation
- Status: OPEN

### TIER 3: IssueHunt Bounties (older, may be stale)

- Boostnote browser extension: $155 (JavaScript)
- Boostnote Evernote integration: $147 (JavaScript)
- Boostnote git sync: $105 (JavaScript)
- Ant Design datepicker year format: $336 (TypeScript)
- Boostnote multiple notes selection: $80 (JavaScript)

### Closed/Already Solved (skip these)
- Golem Cloud MCP Server ($3,500) — CLOSED, already completed
- Nuclei: Replace panic with error handling ($100) — CLOSED
- Storybook controls select bug ($70) — CLOSED
- Remotion bounties — none currently open
- Daytona bounties — all under $50

### Platforms to monitor:
- Algora (algora.io/bounties) — best for $500+ bounties, active
- Opire (opire.dev) — smaller bounties $50-300
- IssueHunt (oss.issuehunt.io) — many stale, check freshness
- ProjectDiscovery — consistent $100-250 Go bounties via Algora

## Submitted PRs
1. **FinMind GDPR PII Export & Delete ($500)** — https://github.com/rohitdash08/FinMind/pull/357
   - Submitted: March 10, 2026
   - Status: OPEN, awaiting review
   - 3 endpoints, 18 tests, 449 lines added

## Completed
<!-- Bounties claimed and paid -->

## Total Earnings: $0
