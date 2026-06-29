```
   ________    ____  __  ______
  / ____/ /   / __ \/ / / / __ \
 / /   / /   / / / / / / / / / /
/ /___/ /___/ /_/ / /_/ / /_/ /
\____/_____/\____/\____/_____/
    ___   __  ______  ______________  ____
   /   | / / / / __ \/  _/_  __/ __ \/ __ \
  / /| |/ / / / / / // /  / / / / / / /_/ /
 / ___ / /_/ / /_/ // /  / / / /_/ / _, _/
/_/  |_\____/_____/___/ /_/  \____/_/ |_|

//  cloud-infra-auditor  |||  scan → audit → report → cleanup  //
```

# cloud-infra-auditor

> AWS infrastructure auditing and cost optimization — from the terminal.

<p align="left">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python 3.11+"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/tests-pytest%20%2B%20moto-green.svg" alt="Tests">
  <img src="https://img.shields.io/badge/linter-ruff-purple.svg" alt="Ruff">
  <img src="https://img.shields.io/badge/formatter-black-black.svg" alt="Black">
  <img src="https://img.shields.io/badge/CI-github%20actions-blue.svg" alt="GitHub Actions">
  <a href="https://boto3.amazonaws.com/v1/documentation/api/latest/index.html"><img src="https://img.shields.io/badge/AWS-boto3-orange.svg" alt="Boto3"></a>
</p>

---

## Overview

Cloud accounts accumulate waste quietly — unattached volumes, orphaned Elastic IPs, instances running at 2% CPU for months. Most teams discover this on the billing page.

`cloud-infra-auditor` connects to your AWS account, scans for unused and underutilized resources, and surfaces findings as a Rich terminal report, a JSON export, or a CSV. It follows a deliberate **scan → analyze → report → review → cleanup** workflow. Nothing is modified unless you explicitly confirm it.

---

## Features

| Category | Capability |
|---|---|
| **Scanning** | Unattached EBS volumes, unassociated Elastic IPs, underutilized EC2 instances |
| **Metrics** | CloudWatch-backed CPU utilization detection |
| **Multi-region** | Scan resources across multiple AWS regions |
| **Reporting** | Rich terminal tables, JSON export, CSV export |
| **Cleanup** | Dry-run preview; explicit `--execute` required — nothing deleted silently |
| **Retry** | Configurable retry logic for AWS API calls |
| **Testing** | Pytest + Moto + `unittest.mock` — no real AWS account needed |
| **CI** | GitHub Actions pipeline |
| **Packaging** | `pyproject.toml`, wheel + source dist, `cloud-auditor` entry point |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CLI  (Typer)                           │
│        auditor/cli/main.py  ←  scan / report / cleanup      │
│        auditor/cli/scan.py  |  auditor/cli/report.py        │
│        auditor/cli/cleanup.py  |  auditor/cli/auth.py       │
│        auditor/cli/aws.py                                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
          ┌────────────────▼────────────────┐
          │         AWS Layer               │
          │  auditor/aws/session.py         │
          │  auditor/aws/auth.py            │
          │  auditor/aws/regions.py         │
          │  auditor/aws/cloudwatch.py      │
          └────────────────┬────────────────┘
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
┌──────▼──────┐   ┌────────▼──────┐   ┌───────▼──────┐
│ ebs_scanner │   │ eip_scanner   │   │ ec2_scanner  │
│     .py     │   │     .py       │   │     .py      │
└──────┬──────┘   └────────┬──────┘   └───────┬──────┘
       │                   │                   │
       └───────────────────▼───────────────────┘
              auditor/models/findings.py
              auditor/models/resource.py
                           │
          ┌────────────────▼────────────────┐
          │       Reports Layer             │
          │  report_generator.py            │
          │  report_transformer.py          │
          │  rich_formatter.py              │
          │  json_exporter.py               │
          │  csv_exporter.py                │
          └────────────────┬────────────────┘
                           │
          ┌────────────────▼────────────────┐
          │       Cleanup Layer             │
          │  auditor/cleanup/dry_run.py     │
          │  auditor/cleanup/ebs_cleanup.py │
          │  auditor/cleanup/eip_cleanup.py │
          └─────────────────────────────────┘
```

---

## Project Structure

```
cloud-infra-auditor/
├── .github/                          # GitHub Actions CI workflows
├── auditor/
│   ├── aws/
│   │   ├── auth.py                   # AWS credential handling
│   │   ├── cloudwatch.py             # CloudWatch metric queries
│   │   ├── regions.py                # Region resolution
│   │   └── session.py                # Boto3 session management
│   ├── cli/
│   │   ├── main.py                   # Typer app entrypoint
│   │   ├── scan.py                   # scan command
│   │   ├── report.py                 # report command
│   │   ├── cleanup.py                # cleanup command
│   │   ├── auth.py                   # auth command
│   │   └── aws.py                    # aws command
│   ├── cleanup/
│   │   ├── dry_run.py                # Dry-run preview logic
│   │   ├── ebs_cleanup.py            # EBS volume deletion
│   │   └── eip_cleanup.py            # Elastic IP release
│   ├── models/
│   │   ├── findings.py               # Finding data model
│   │   └── resource.py               # Resource data model
│   ├── reports/
│   │   ├── report_generator.py       # Aggregates scan findings
│   │   ├── report_transformer.py     # Transforms findings for export
│   │   ├── rich_formatter.py         # Rich terminal output
│   │   ├── json_exporter.py          # JSON export
│   │   └── csv_exporter.py           # CSV export
│   ├── scanners/
│   │   ├── ebs_scanner.py            # Unattached EBS detection
│   │   ├── eip_scanner.py            # Unassociated EIP detection
│   │   └── ec2_scanner.py            # Underutilized EC2 detection
│   ├── utils/
│   │   ├── exceptions.py             # Custom exceptions
│   │   ├── helpers.py                # Shared utilities
│   │   ├── logger.py                 # Logging configuration
│   │   └── retry.py                  # AWS API retry logic
│   └── constants.py                  # Project-wide constants
├── tests/
│   ├── conftest.py
│   ├── test_cleanup.py
│   ├── test_csv_exporter.py
│   ├── test_ebs_scanner.py
│   ├── test_ec2_scanner.py
│   ├── test_eip_scanner.py
│   ├── test_json_exporter_.py
│   ├── test_regions.py
│   ├── test_report_generator.py
│   ├── test_report_transformer.py
│   └── test_session.py
├── config/                           # YAML thresholds and region defaults
├── docs/
├── audit_reports/                    # Runtime audit output (gitignored)
├── reports/                          # Generated exports (gitignored)
├── manual_testing/
├── dist/
│   ├── cloud_infra_auditor-1.0.0.tar.gz
│   └── cloud_infra_auditor-1.0.0-py3-none-any.whl
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── LICENSE
```

---

## Getting Started

### Prerequisites

| Requirement | Version |
|---|:---:|
| Python | 3.11+ |
| Git | Latest |
| AWS CLI | v2 |
| pip | Latest |

```bash
python --version
pip --version
git --version
aws --version
```

### Clone

```bash
git clone https://github.com/harshil6-lab/cloud-infra-auditor.git
cd cloud-infra-auditor
```

### Virtual Environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install

```bash
# Runtime only
pip install -r requirements.txt

# Development (recommended)
pip install -e ".[dev]"
```

The development install includes Pytest, Moto, Ruff, and Black.

### Verify

```bash
cloud-auditor --help
```

Expected output:

```
Usage: cloud-auditor [OPTIONS] COMMAND [ARGS]...

  Cloud Infrastructure Auditor & Cost Optimizer
```

---

## AWS Configuration

```bash
# Configure credentials interactively
aws configure

# Verify authentication
aws sts get-caller-identity
```

**Minimum IAM permissions for scanning (read-only):**

```json
{
  "Effect": "Allow",
  "Action": [
    "ec2:Describe*",
    "cloudwatch:GetMetricStatistics"
  ],
  "Resource": "*"
}
```

Cleanup operations additionally require `ec2:ReleaseAddress` and `ec2:DeleteVolume`. These are only invoked after explicit `--execute` confirmation.

---

## Usage

### Scan

```bash
cloud-auditor scan ebs
cloud-auditor scan eip
cloud-auditor scan ec2
```

### Report

```bash
cloud-auditor report json
cloud-auditor report csv
```

### Cleanup

```bash
# Preview — no changes made
cloud-auditor cleanup ebs --dry-run
cloud-auditor cleanup eip --dry-run

# Execute after confirmation
cloud-auditor cleanup ebs --execute
cloud-auditor cleanup eip --execute
```

### Auth

```bash
cloud-auditor auth
```

### AWS

```bash
cloud-auditor aws
```

### Help

```bash
cloud-auditor --help
cloud-auditor scan --help
cloud-auditor cleanup --help
cloud-auditor report --help
```

---

## Testing

All tests run against Moto-mocked AWS services. No live AWS account or credentials required.

```bash
# Full test suite
pytest

# With terminal coverage summary
pytest --cov=auditor --cov-report=term-missing

# HTML coverage report
pytest --cov=auditor --cov-report=html
# Open: htmlcov/index.html
```

**Test files:**

| File | Covers |
|---|---|
| `test_ebs_scanner.py` | EBS unattached volume detection |
| `test_eip_scanner.py` | Elastic IP unassociated detection |
| `test_ec2_scanner.py` | EC2 underutilization detection |
| `test_cleanup.py` | Dry-run and cleanup execution |
| `test_report_generator.py` | Report aggregation |
| `test_report_transformer.py` | Report transformation |
| `test_json_exporter_.py` | JSON export |
| `test_csv_exporter.py` | CSV export |
| `test_session.py` | Boto3 session management |
| `test_regions.py` | Region resolution |
| `conftest.py` | Shared fixtures |

---

## Code Quality

```bash
black .
ruff check .
```

---

## Build

```bash
python -m build
```

Artifacts generated in `dist/`:

```
dist/
├── cloud_infra_auditor-1.0.0.tar.gz
└── cloud_infra_auditor-1.0.0-py3-none-any.whl
```

---

## Technology Stack

| Category | Technology | Version |
|---|---|:---:|
| Language | Python | 3.11+ |
| CLI Framework | Typer | 0.16+ |
| Cloud SDK | Boto3 | 1.40+ |
| Terminal UI | Rich | 14.0+ |
| Testing | Pytest | 9.1+ |
| AWS Mocking | Moto | 5.1+ |
| Mock Library | unittest.mock | stdlib |
| Formatter | Black | 25.1+ |
| Linter | Ruff | 0.12+ |
| Packaging | setuptools + build | 68+ |
| Distribution | Wheel + source dist | PEP 427 |
| CI | GitHub Actions | — |
| Config Format | TOML (`pyproject.toml`) | PEP 621 |
| AWS Auth | AWS CLI | v2 |
| Cloud Services | EC2, EBS, Elastic IP, CloudWatch | AWS |

---

## Design Decisions

**Why Typer?**
Type-annotated commands, zero boilerplate, auto-generated `--help` that stays accurate without maintenance.

**Why Rich?**
Tables and progress output that degrade cleanly in CI environments. No custom rendering code.

**Why a `models/` layer?**
`findings.py` and `resource.py` define a shared schema consumed by scanners, the report pipeline, and cleanup. Adding a new exporter or scanner requires no structural changes elsewhere.

**Why `report_transformer.py` separate from `report_generator.py`?**
Generation and transformation are distinct responsibilities. `report_generator.py` aggregates raw findings; `report_transformer.py` shapes them for a specific output format. Keeping these separate makes each independently testable.

**Why dry-run by default?**
Audit tools carry asymmetric risk. Scanning is always safe; deletion is not. The default posture is read-only. Cleanup requires `--execute` explicitly.

**Why Moto for tests?**
Real AWS calls in tests are slow, costly, and non-deterministic. Moto provides accurate service simulation — tests run offline with no live account.

---

## Security

- **Read-only by default.** `scan` requires only `Describe*` and `GetMetricStatistics`. No write permissions needed.
- **Explicit execution gate.** `--dry-run` shows what would be affected; `--execute` prompts per resource before acting. Cleanup never runs from a scan.
- **No credential storage.** The tool delegates entirely to boto3's credential chain — no secrets are read, copied, or logged by the application.
- **Least privilege.** Minimum IAM policy for read-only audit is documented above. Write permissions should be granted only when cleanup is required.

---

## Roadmap

```
[x] AWS session management and credential resolution
[x] EBS unattached volume scanner
[x] Elastic IP unassociated scanner
[x] EC2 underutilization scanner (CloudWatch-backed)
[x] Rich terminal formatter
[x] JSON and CSV export
[x] Report generator and transformer
[x] Dry-run and confirmation-gated cleanup
[x] Pytest + Moto test coverage (11 test modules)
[x] GitHub Actions CI
[x] pyproject.toml packaging, wheel + source dist
[ ] Parallel scanning via ThreadPoolExecutor
[ ] RDS idle instance detection
[ ] S3 lifecycle analysis
[ ] Multi-account support via assume-role
[ ] HTML report output
[ ] Docker image
[ ] Slack / PagerDuty alerting integration
```

---

## Author

**Harshil Kalsariya**
[github.com/harshil6-lab](https://github.com/harshil6-lab)

**Sravya Maddipati**
[github.com/sravya-77](https://github.com/sravya-77)

---

## License

[MIT](./LICENSE)
