## Quick Start

```bash
git clone https://github.com/harshil6-lab/cloud-infra-auditor.git

cd cloud-infra-auditor

python -m venv venv

# Windows
venv\Scripts\activate

pip install -e ".[dev]"

aws configure
For detailed AWS credential setup and IAM configuration, see:
- **[AWS Configuration Guide](docs/AWS_CONFIG.md)**

cloud-auditor scan ebs
```