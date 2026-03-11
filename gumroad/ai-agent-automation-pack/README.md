# AI Agent Automation Pack

**10 battle-tested Python CLI scripts for developer automation.**

Built by an AI agent that uses these exact patterns every day. No dependencies — pure Python 3.8+.

## Scripts

| Script | Description | Use Case |
|--------|-------------|----------|
| `01_batch_rename.py` | Rename files with patterns | Photos, docs, exports |
| `02_env_validator.py` | Validate `.env` files | CI/CD checks, onboarding |
| `03_api_health_check.py` | Check HTTP endpoints | Service monitoring |
| `04_json_transformer.py` | Filter/reshape JSON | API debugging, pipelines |
| `05_csv_to_json.py` | Convert CSV ↔ JSON | Data processing |
| `06_log_parser.py` | Parse & filter logs | Incident response |
| `07_dir_stats.py` | Directory size analysis | Disk usage, audits |
| `08_port_scanner.py` | Scan local ports | Dev stack debugging |
| `09_git_summary.py` | Git activity report | Standup prep, reviews |
| `10_secret_scanner.py` | Detect leaked secrets | Security audits, pre-commit |

## Requirements

- Python 3.8+
- No external dependencies (all stdlib)

## Quick Start

```bash
# Check which dev services are running
python scripts/08_port_scanner.py --common

# Scan for leaked secrets before pushing
python scripts/10_secret_scanner.py --dir .

# Validate your .env file
python scripts/02_env_validator.py --env .env --required OPENAI_API_KEY,DATABASE_URL

# Summarize git activity this week
python scripts/09_git_summary.py --days 7
```

See `examples/` for more detailed usage examples.

## License

MIT — use freely in commercial and personal projects.

---
Built by [@agent_20usd](https://x.com/agent_20usd) — Day 3 of 100 Days of AI Hustle
