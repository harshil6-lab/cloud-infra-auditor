# Cloud Infrastructure Auditor & Cost Optimizer

A production-grade Command Line Interface (CLI) tool built for DevOps and FinOps teams to identify cloud resource waste, optimize infrastructure costs, and enforce cloud hygiene across AWS environments.

---

## Overview

Cloud Infrastructure Auditor scans AWS accounts and identifies:

* Unattached EBS Volumes
* Unassociated Elastic IPs
* Underutilized EC2 Instances
* Idle Resources
* Infrastructure Cost Optimization Opportunities

The tool generates detailed reports and provides safe cleanup recommendations through a controlled execution workflow.

---

## Features

### Resource Auditing

* Scan AWS accounts across multiple regions
* Detect unattached EBS volumes
* Detect unassociated Elastic IPs
* Identify low-utilization EC2 instances using CloudWatch metrics

### Reporting

* Interactive terminal reports using Rich
* Export findings as JSON
* Export findings as CSV
* Cost-saving summaries

### Safe Cleanup

* Dry-run mode
* Confirmation-based execution
* Resource cleanup recommendations

### Engineering Standards

* Modular architecture
* Unit-tested components
* AWS SDK (Boto3)
* Production-ready logging
* Extensible provider architecture

---

## Tech Stack

| Component     | Technology              |
| ------------- | ----------------------- |
| Language      | Python 3.11+            |
| CLI Framework | Typer                   |
| Terminal UI   | Rich                    |
| AWS SDK       | Boto3                   |
| Serialization | JSON, PyYAML            |
| Testing       | Pytest, Moto            |
| Packaging     | Setuptools, PyInstaller |

---

## Project Structure

```text
cloud-infra-auditor/
├── auditor/
├── tests/
├── config/
├── reports/
├── docs/
└── README.md
```

---

## Development Status

Current Phase: Day-0 (Repository Initialization)

Planned Timeline:

* Week 1: CLI Architecture & Authentication
* Week 2: Audit Scanners
* Week 3: Reporting & Cleanup
* Week 4: Testing & Packaging

---

## Contributors

* Harshil kalsariya – Architecture & AWS Integration
* Rifaz G – Reporting & Documentation
* Sravya M – Resource Scanners
* Prakash Bhanu – Testing & QA

---

## License

MIT License
