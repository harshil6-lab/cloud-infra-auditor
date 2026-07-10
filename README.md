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
  <a href="https://pypi.org/project/cloud-infra-auditor/"><img src="https://img.shields.io/pypi/v/cloud-infra-auditor.svg" alt="PyPI"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python 3.11+"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="MIT License"></a>
  <a href="https://github.com/harshil6-lab/cloud-infra-auditor/releases/tag/v1.1.0"><img src="https://img.shields.io/badge/release-v1.1.0-brightgreen.svg" alt="Release v1.1.0"></a>
  <img src="https://img.shields.io/badge/tests-pytest%20%2B%20moto-green.svg" alt="Tests">
  <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg" alt="Platform">
</p>

**Package:** `cloud-infra-auditor` · **CLI entry point:** `cloud-auditor` · **Python:** 3.11+ · **License:** MIT · **Platforms:** macOS, Linux, Windows

---

## What it does

Cloud accounts accumulate waste quietly — unattached volumes, orphaned Elastic IPs, instances running at 2% CPU for months. Most teams discover this on the billing page.

`cloud-infra-auditor` connects to your AWS account, scans for unused and underutilized resources, and surfaces findings as a Rich terminal report, a JSON export, or a CSV. It follows a deliberate **scan → analyze → report → review → cleanup** workflow. Nothing is deleted unless you explicitly confirm it.

As of **v1.1.0**, multi-region scans run in parallel via a shared `ThreadPoolExecutor`-backed utility, cutting typical scan time from **~60–65 seconds down to ~8–10 seconds**.

---

## Installation

Install from PyPI:

```bash
pip install cloud-infra-auditor
```

Verify the install:

```bash
cloud-auditor --help
```

### Configure AWS credentials

`cloud-infra-auditor` uses boto3's standard credential chain — no credentials are stored or read by the application itself.

```bash
aws configure
aws sts get-caller-identity
```

See [AWS Configuration Guide](docs/AWS_CONFIG.md) for IAM setup details.

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

Cleanup additionally requires `ec2:ReleaseAddress` and `ec2:DeleteVolume`, invoked only after explicit `--execute` confirmation.

----

## Quick Start

```bash
# 1. Authenticate
aws sts get-caller-identity

# 2. Scan
cloud-auditor scan ec2
cloud-auditor scan ebs
cloud-auditor scan eip

# 3. Export a report
cloud-auditor report export --format json

# 4. Clean up (dry-run first, always)
cloud-auditor cleanup ebs --dry-run
cloud-auditor cleanup ebs --execute
```

Multi-region scans run in parallel by default, with a live Rich progress bar and a summary panel printed at the end of each scan.

-----

## Features

**Infrastructure Auditing**
- Unattached EBS volume detection
- Unassociated Elastic IP detection
- Underutilized EC2 instance detection, backed by CloudWatch CPU metrics
- Parallel multi-region scanning

**Reporting**
- Rich terminal tables
- JSON export
- CSV export

**Cleanup**
- Dry-run preview by default
- Explicit `--execute` flag required — nothing is deleted silently

**Developer Experience**
- Typer-based CLI with auto-generated `--help`
- Rich progress bar and post-scan summary panel
- Configurable retry logic for AWS API calls

**Performance**
- Shared `ThreadPoolExecutor`-backed scanning utility across all scanners
- Region scans execute concurrently instead of sequentially

**Architecture**
- Clear separation between CLI, AWS access, scanning, reporting, and cleanup layers
- Each scanner is independently testable against mocked AWS services

---

## Performance

Prior to v1.1.0, each AWS region was scanned sequentially, one after another. v1.1.0 introduces a shared scanning utility (`auditor/utils/parallel.py`) built on `ThreadPoolExecutor`, so all scanners run region scans concurrently instead of duplicating their own threading logic.

| | Before (sequential) | After (parallel, v1.1.0) |
|---|:---:|:---:|
| Typical multi-region scan | ~60–65 sec | ~8–10 sec |

Actual timing depends on account size, region count, and API throttling.

---

## CLI Preview

### Help Command

<!-- Screenshot -->

### Scan EC2

<!-- Screenshot -->

### Scan EBS

<!-- Screenshot -->

### Scan EIP

<!-- Screenshot -->

### Report Export (JSON / CSV)

<!-- Screenshot -->

### Cleanup

<!-- Screenshot -->

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CLI  (Typer)                            │
│        auditor/cli/main.py  ←  scan / report / cleanup       │
│        auditor/cli/scan.py  |  auditor/cli/report.py         │
│        auditor/cli/cleanup.py  |  auditor/cli/auth.py        │
│        auditor/cli/aws.py                                    │
└──────────────────────────┬────────────────────────────────────┘
                           │
          ┌────────────────▼────────────────┐
          │         AWS Layer               │
          │  auditor/aws/session.py         │
          │  auditor/aws/auth.py            │
          │  auditor/aws/regions.py         │
          │  auditor/aws/cloudwatch.py      │
          └────────────────┬────────────────┘
                           │
          ┌────────────────▼────────────────┐
          │   Parallel Scan Utility         │
          │  auditor/utils/parallel.py      │
          │  (ThreadPoolExecutor, shared     │
          │   across all scanners)          │
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
          │          UI Layer               │
          │  auditor/ui/summary.py          │
          │  (Rich progress bar + summary   │
          │   panel)                        │
          └────────────────┬────────────────┘
                           │
          ┌────────────────▼────────────────┐
          │       Cleanup Layer             │
          │  auditor/cleanup/dry_run.py     │
          │  auditor/cleanup/ebs_cleanup.py │
          │  auditor/cleanup/eip_cleanup.py │
          └─────────────────────────────────┘
```

Each layer has a single responsibility: the CLI parses commands and delegates; the AWS layer manages sessions, auth, and region resolution; the parallel scan utility fans work out across regions; scanners detect findings; the reports layer aggregates and transforms those findings into terminal, JSON, or CSV output; and the cleanup layer executes changes only behind an explicit confirmation gate.

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
│   │   ├── ebs_cleanup.py            # EBS volume deletion
│   │   └── eip_cleanup.py            # Elastic IP release
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
│   ├── ui/
│   │   └── summary.py                # Rich progress bar + scan summary panel
│   ├── utils/
│   │   ├── exceptions.py             # Custom exceptions
│   │   ├── helpers.py                # Shared utilities
│   │   ├── logger.py                 # Logging configuration
│   │   ├── retry.py                  # AWS API retry logic
│   │   └── parallel.py               # Shared ThreadPoolExecutor scanning utility
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
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── LICENSE
```

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
cloud-auditor report export --format csv
cloud-auditor report export --format json
```

### Cleanup

```bash
# Preview only — no changes made
cloud-auditor cleanup ebs --dry-run
cloud-auditor cleanup eip --dry-run

# Execute after confirmation
cloud-auditor cleanup ebs --execute
cloud-auditor cleanup eip --execute
```

### Auth

```bash
cloud-auditor auth identity
cloud-auditor auth profiles
```

### AWS

```bash
cloud-auditor aws regions
```

### Help

```bash
cloud-auditor --help
cloud-auditor scan --help
cloud-auditor cleanup --help
cloud-auditor report --help
```

---

## Security

- **Read-only by default.** `scan` requires only `Describe*` and `GetMetricStatistics`. No write permissions needed.
- **Explicit execution gate.** `--dry-run` shows what would be affected; `--execute` is required to act, and prompts per resource. Cleanup never runs implicitly from a scan.
- **No credential storage.** The tool delegates entirely to boto3's credential chain — no secrets are read, copied, or logged by the application.
- **Least privilege.** The minimum IAM policy for a read-only audit is documented above. Write permissions should be granted only when cleanup is required.

---

## Technology Stack

**Core**
| Technology | Version |
|---|:---:|
| Python | 3.11+ |
| CLI Framework — Typer | 0.16+ |
| Terminal UI — Rich | 14.0+ |
| Concurrency — ThreadPoolExecutor | stdlib |

**AWS**
| Technology | Version |
|---|:---:|
| Boto3 | 1.40+ |
| AWS CLI | v2 |
| Services covered | EC2, EBS, Elastic IP, CloudWatch |

**Testing**
| Technology | Version |
|---|:---:|
| Pytest | 9.1+ |
| Moto | 5.1+ |
| unittest.mock | stdlib |

**Packaging**
| Technology | Version |
|---|:---:|
| setuptools + build | 68+ |
| Distribution | Wheel + source dist (PEP 427) |
| Config format | TOML — `pyproject.toml` (PEP 621) |

**Developer Tools**
| Technology | Version |
|---|:---:|
| Black | 25.1+ |
| Ruff | 0.12+ |
| CI | GitHub Actions |

---

## Testing

All tests run against Moto-mocked AWS services — no live AWS account or credentials required.

```bash
# Full test suite
pytest

# With terminal coverage summary
pytest --cov=auditor --cov-report=term-missing

# HTML coverage report
pytest --cov=auditor --cov-report=html
```

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

## Design Decisions

**Why Typer?**
Type-annotated commands, minimal boilerplate, and auto-generated `--help` that stays accurate without manual maintenance.

**Why Rich?**
Tables, progress bars, and summary panels that degrade cleanly in CI environments, without custom rendering code.

**Why a shared `auditor/utils/parallel.py`?**
Each scanner originally implemented its own threading logic for multi-region scans. Consolidating this into a single `ThreadPoolExecutor`-backed utility removed duplicated code and made concurrency behavior consistent and independently testable across all scanners.

**Why separate `report_transformer.py` from `report_generator.py`?**
Generation and transformation are distinct responsibilities. `report_generator.py` aggregates raw findings; `report_transformer.py` shapes them for a specific output format. Keeping these separate makes each independently testable.

**Why dry-run by default?**
Audit tools carry asymmetric risk. Scanning is always safe; deletion is not. The default posture is read-only, and cleanup requires `--execute` explicitly.

**Why Moto for tests?**
Real AWS calls in tests are slow, costly, and non-deterministic. Moto provides accurate service simulation, so tests run offline with no live account required.

---

## Roadmap

- [R&D] RDS auditing
- [R&D] S3 lifecycle analysis
- [R&D] Security Group auditing
- [R&D] IAM auditing
- [ ] Cost insights and estimated savings
- [ ] HTML report output
- [ ] Multi-account support via assume-role
- [ ] Configurable worker count for parallel scans
- [ ] Additional AWS service coverage

---

## Contributing

Contributions are welcome. Please open an issue before submitting large changes.

---

## Releases

**Latest release: v1.1.0**

- Published on [GitHub Releases](https://github.com/harshil6-lab/cloud-infra-auditor/releases/tag/v1.1.0)
- Published on [PyPI](https://pypi.org/project/cloud-infra-auditor/)

---

## Author

**Harshil Kalsariya**
[github.com/harshil6-lab](https://github.com/harshil6-lab)

**Sravya Maddipati**
[github.com/sravya-77](https://github.com/sravya-77)

---

## License

[MIT](./LICENSE)
