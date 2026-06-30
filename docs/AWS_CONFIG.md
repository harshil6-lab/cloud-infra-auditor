# AWS Configuration Guide

This guide explains how to configure AWS credentials for **Cloud Infrastructure Auditor**.

The application uses the **AWS CLI** and **Boto3 credential provider chain**, which means **no AWS credentials are stored inside the application**.

---

# Prerequisites

Before configuring AWS credentials, ensure you have:

- An AWS Account
- AWS CLI v2 installed
- Python 3.11+
- Internet connection

Verify the AWS CLI installation:

```bash
aws --version
```

Example:

```text
aws-cli/2.27.0 Python/3.13 Windows/11 exe/AMD64
```

---

# Step 1 — Create an IAM User

> **Recommended:** Do **NOT** use your AWS root account.

1. Sign in to the AWS Management Console.
2. Open **IAM**.
3. Navigate to:

```
IAM → Users → Create User
```

4. Enter a username.

Example:

```
cloud-auditor
```

5. Click **Next**.

---

# Step 2 — Grant Permissions

For scanning only, attach a **read-only policy** with permissions such as:

- EC2 Describe
- CloudWatch GetMetricStatistics

Example policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:Describe*",
                "cloudwatch:GetMetricStatistics"
            ],
            "Resource": "*"
        }
    ]
}
```

If you want to use cleanup commands, also allow:

```text
ec2:DeleteVolume
ec2:ReleaseAddress
```

> **Follow the Principle of Least Privilege.** Only grant permissions required for the features you intend to use.

---

# Step 3 — Create Access Keys

Navigate to:

```
IAM
→ Users
→ Your User
→ Security Credentials
→ Access Keys
→ Create Access Key
```

Choose:

```
Command Line Interface (CLI)
```

AWS will provide:

```
Access Key ID

Secret Access Key
```

**Important**

The Secret Access Key is shown only once.

Store it securely.

---

# Step 4 — Configure AWS CLI

Run:

```bash
aws configure
```

Example:

```text
AWS Access Key ID [None]:
AKIA****************

AWS Secret Access Key [None]:
********************************

Default region name [None]:
us-east-1

Default output format [None]:
json
```

---

# Step 5 — Verify Credentials

Run:

```bash
aws sts get-caller-identity
```

Example output:

```json
{
    "UserId": "AIDAxxxxxxxxxxxx",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/cloud-auditor"
}
```

If this command succeeds, your credentials are configured correctly.

---

# Using AWS Profiles

If you work with multiple AWS accounts, create named profiles.

Example:

```bash
aws configure --profile personal
```

```bash
aws configure --profile production
```

List configured profiles:

```bash
aws configure list-profiles
```

Example:

```text
default
personal
production
```

---

# Selecting a Profile

If your application supports profile selection:

```bash
cloud-auditor auth profile personal
```

or

```bash
cloud-auditor scan ebs --profile personal
```

> Use the command that matches your project's CLI.

---

# Credential Storage

AWS CLI stores credentials in:

### Windows

```text
C:\Users\<username>\.aws\
```

Files:

```
credentials
config
```

### Linux / macOS

```text
~/.aws/
```

Files:

```
credentials
config
```

Example:

```
credentials

[default]
aws_access_key_id = AKIA...
aws_secret_access_key = xxxxxxxxx

[personal]
aws_access_key_id = AKIA...
aws_secret_access_key = xxxxxxxxx
```

---

# How Cloud Infrastructure Auditor Authenticates

The application relies on **Boto3's default credential provider chain**.

Credentials are resolved in the following order:

1. Environment Variables
2. AWS CLI Profile
3. Shared Credentials File
4. IAM Role (EC2)
5. ECS Task Role
6. AWS SSO (if configured)

No credentials are hardcoded or stored by the application.

---

# Verify the CLI

After configuring AWS:

```bash
cloud-auditor --help
```

Example scan:

```bash
cloud-auditor scan ebs
```

Example cleanup preview:

```bash
cloud-auditor cleanup ebs --dry-run
```

---

# Common Errors

## Unable to locate credentials

```text
Unable to locate credentials
```

Solution:

```bash
aws configure
```

or

```bash
aws configure --profile <profile-name>
```

---

## AccessDenied

```text
AccessDenied
```

Cause:

The IAM user does not have sufficient permissions.

Grant the required EC2 and CloudWatch permissions.

---

## Expired Token

```text
ExpiredToken
```

Cause:

Temporary credentials have expired.

Refresh your credentials or log in again if using AWS SSO.

---

## InvalidClientTokenId

```text
InvalidClientTokenId
```

Cause:

The Access Key ID or Secret Access Key is incorrect.

Run:

```bash
aws configure
```

again.

---

# Security Best Practices

- Never commit AWS credentials to Git.
- Never hardcode credentials in source code.
- Use IAM users or IAM roles instead of the AWS root account.
- Rotate access keys regularly.
- Grant only the minimum permissions required.
- Add `.aws/` and credential files to `.gitignore` if needed.

---

# Additional Resources

- AWS CLI Documentation: https://docs.aws.amazon.com/cli/
- IAM Documentation: https://docs.aws.amazon.com/IAM/
- Boto3 Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

---

Happy Auditing! 🚀