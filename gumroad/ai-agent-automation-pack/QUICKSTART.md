# Quick Start Guide

## Installation

No installation needed. Just download and run.

```bash
# Python 3.8+ required (check your version)
python --version

# Run any script directly
python scripts/08_port_scanner.py --common
```

## Most Useful Scripts First

### 1. Secret Scanner (run before every commit!)
```bash
python scripts/10_secret_scanner.py --dir .
# Scans for API keys, tokens, passwords
# Exit code 1 if secrets found — great for pre-commit hooks
```

Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python /path/to/10_secret_scanner.py --dir . || exit 1
```

### 2. Port Scanner (debug your dev stack)
```bash
python scripts/08_port_scanner.py --common
# Shows all common dev ports (Postgres, Redis, Node, etc.)

python scripts/08_port_scanner.py --range 3000-3010
# Scan a custom range
```

### 3. API Health Check (monitor your services)
```bash
python scripts/03_api_health_check.py \
  --urls http://localhost:3000/health,http://localhost:8000/ping
```

### 4. Env Validator (catch missing vars early)
```bash
python scripts/02_env_validator.py \
  --env .env \
  --required DATABASE_URL,API_KEY,SECRET_KEY
# Exit code 1 if any required var is missing
```

### 5. Git Summary (prep for standups)
```bash
python scripts/09_git_summary.py --days 7
# Shows commits, contributors, most changed files
```

## Use in CI/CD

```yaml
# GitHub Actions example
- name: Check for secrets
  run: python scripts/10_secret_scanner.py --dir .

- name: Validate environment
  run: python scripts/02_env_validator.py --env .env.example --strict
```

## All Scripts Have --help

```bash
python scripts/01_batch_rename.py --help
```
