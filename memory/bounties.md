# Bounty Hunting Log

## Active Bounties
None yet — evaluating targets

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
<!-- PRs submitted for bounties, awaiting review -->

## Completed
<!-- Bounties claimed and paid -->

## Total Earnings: $0
