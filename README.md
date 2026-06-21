# cloud-infra-auditor

> Production-grade AWS infrastructure auditing and cost optimization CLI for DevOps and FinOps teams.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Tests](https://img.shields.io/badge/tests-pytest%20%2B%20moto-green.svg)]()
[![AWS](https://img.shields.io/badge/AWS-boto3-orange.svg)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

----

## What It Does

Scans AWS accounts for resource waste and surfaces actionable cost-saving recommendations — without touching anything unless you explicitly confirm.

**Detects:**
- Unattached EBS volumes
- Unassociated Elastic IPs
- Underutilized EC2 instances (via CloudWatch metrics)
- Idle and orphaned resources across regions

**Outputs:**
- Rich terminal report (interactive, color-coded)
- JSON and CSV exports for downstream ingestion
- Cost-saving summary with per-resource estimates

**Execution model:** dry-run by default, confirmation-gated cleanup. Nothing is deleted silently.

----

## Requirements

- Python 3.11+
- AWS credentials configured (`~/.aws/credentials` or environment variables)
- IAM permissions: `ec2:Describe*`, `cloudwatch:GetMetricStatistics`, `ec2:ReleaseAddress`, `ec2:DeleteVolume` *(cleanup only)*

---

## Installation

```bash
git clone https://github.com/harshil6-lab/cloud-infra-auditor.git
cd cloud-infra-auditor
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

---

## Usage

```bash
# Full audit — all resource types, us-east-1
auditor scan

# Target specific region and resource type
auditor scan --region ap-south-1 --resource ebs

# Export findings
auditor scan --output json --report-path ./reports/

# Cleanup with dry-run (default)
auditor cleanup --dry-run

# Cleanup with confirmation prompt
auditor cleanup --confirm
```

Run `auditor --help` or `auditor <command> --help` for full option reference.

---

## Project Structure

```
cloud-infra-auditor/
├── auditor/
│   ├── cli.py              # Typer entrypoint, command definitions
│   ├── auth.py             # AWS session management, credential resolution
│   ├── scanners/
│   │   ├── base.py         # Abstract scanner interface
│   │   ├── ebs.py          # Unattached volume detection
│   │   ├── eip.py          # Unassociated Elastic IP detection
│   │   └── ec2.py          # Underutilization via CloudWatch
│   ├── reporters/
│   │   ├── terminal.py     # Rich-based interactive output
│   │   ├── json_reporter.py
│   │   └── csv_reporter.py
│   ├── cleanup/
│   │   ├── engine.py       # Dry-run / confirmation workflow
│   │   └── handlers.py     # Per-resource cleanup actions
│   └── utils/
│       ├── logging.py
│       └── cost.py         # Pricing estimates
├── tests/
│   ├── unit/
│   └── integration/        # Moto-backed AWS mocks
├── config/
│   └── defaults.yaml       # Thresholds, regions, metric windows
├── reports/                # Generated output (gitignored)
├── docs/
└── README.md
```

---

## Tech Stack

| Layer | Choice | Rationale |
|---|---|---|
| CLI | [Typer](https://typer.tiangolo.com/) | Type-safe commands, auto-generated help |
| Terminal UI | [Rich](https://rich.readthedocs.io/) | Tables, progress bars, color output |
| AWS SDK | [Boto3](https://boto3.amazonaws.com/) | Official SDK, full service coverage |
| Config | PyYAML | Human-editable threshold config |
| Testing | Pytest + [Moto](https://docs.getmoto.org/) | AWS service mocking, no real infra needed |
| Packaging | Setuptools + PyInstaller | Editable installs + standalone binary |

---

## Development

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest --cov=auditor --cov-report=term-missing

# Lint and format
ruff check . && ruff format .
```

**Adding a new scanner:** Subclass `auditor/scanners/base.py`, implement `scan() -> list[Finding]`, register in `cli.py`. Follow the pattern in `ebs.py`.

**Adding a new reporter:** Implement the `Reporter` protocol in `auditor/reporters/`. No base class required — duck typing.

---

## Configuration

Default thresholds live in `config/defaults.yaml`. Override per-run with `--config`:

```yaml
ec2:
  cpu_threshold_percent: 5
  evaluation_window_days: 14
  minimum_data_points: 10

ebs:
  include_states: [available]

regions:
  default: [us-east-1, ap-south-1, eu-west-1]
```

---

## Roadmap

| Week | Scope |
|------|-------|
| 1 | CLI architecture, AWS auth, session management |
| 2 | EBS, EIP, and EC2 scanners |
| 3 | Reporters (terminal, JSON, CSV), cleanup engine |
| 4 | Test coverage, packaging, PyInstaller binary |

**Backlog (post-v1):** RDS idle instance detection, S3 lifecycle analysis, multi-account assume-role support, Slack/PagerDuty alerting.

---

## Contributors

| Name | Scope |
|------|-------|
| Harshil Kalsariya | Architecture, AWS integration, CLI |
| Rifaz G | Reporting pipeline, documentation |
| Sravya M | Resource scanners |
| Bhanu Prakash | Testing, QA, Moto coverage |

---

## License

[MIT](./LICENSE)
