# Contributing to Cloud Infrastructure Auditor & Cost Optimizer

Thank you for your interest in contributing to Cloud Infrastructure Auditor & Cost Optimizer.

Contributions of all sizes are welcome. Whether you're fixing a bug, improving documentation, optimizing performance, or implementing support for additional AWS services, your contributions are appreciated.

---

## Before You Start

Before making significant changes, please open an Issue to discuss your proposal. This helps avoid duplicated work and ensures that the planned implementation aligns with the project's roadmap.

For small bug fixes or documentation improvements, feel free to submit a Pull Request directly.

---

## Development Setup

### 1. Fork the Repository

Fork the repository and clone your fork.

```bash
git clone https://github.com/<your-username>/cloud-infra-auditor.git
cd cloud-infra-auditor
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Or install in editable mode:

```bash
pip install -e .
```

---

## Project Structure

```
auditor/
├── aws/
├── cleanup/
├── cli/
├── reports/
├── scanners/
├── ui/
├── utils/
└── ...
```

Each module has a single responsibility.

- **aws/** – AWS session management and region discovery
- **scanners/** – AWS resource scanners
- **cleanup/** – Safe cleanup operations
- **reports/** – Report generation and export
- **cli/** – Typer command definitions
- **ui/** – Rich terminal output
- **utils/** – Shared utilities

---

## Running Tests

Run all tests before opening a Pull Request.

```bash
pytest
```

---

## Code Formatting

Format code using Black.

```bash
black .
```

Lint using Ruff.

```bash
ruff check .
```

---

## Commit Messages

Use clear, descriptive commit messages.

Examples:

```
feat: add RDS scanner
fix: handle AWS throttling exception
refactor: simplify parallel scanning utility
docs: improve installation guide
test: add scanner unit tests
```

---

## Pull Request Checklist

Before submitting a Pull Request, ensure that:

- Code follows the existing project structure.
- New functionality includes tests where appropriate.
- Existing tests continue to pass.
- Documentation has been updated if necessary.
- README is updated when introducing user-facing features.
- CHANGELOG is updated for significant changes.

---

## Coding Guidelines

Please keep the following principles in mind:

- Write readable and maintainable code.
- Prefer reusable functions over duplicated logic.
- Keep modules focused on a single responsibility.
- Handle AWS API exceptions gracefully.
- Follow existing naming conventions.
- Avoid breaking backward compatibility unless necessary.

---

## Feature Requests

Feature requests are welcome.

Examples include:

- Additional AWS service support
- Performance improvements
- New report formats
- Security checks
- Cost optimization recommendations
- CLI usability improvements

Please open an Issue before beginning major feature development.

---

## Reporting Bugs

When reporting a bug, include:

- Operating system
- Python version
- AWS CLI version (if relevant)
- Command executed
- Error message
- Steps to reproduce

Providing this information helps reproduce and resolve issues more efficiently.

---

## Security

If you discover a security-related issue, please avoid creating a public issue containing sensitive information.

Instead, contact the maintainers privately so the issue can be investigated and resolved responsibly.

---

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping improve Cloud Infrastructure Auditor & Cost Optimizer.
