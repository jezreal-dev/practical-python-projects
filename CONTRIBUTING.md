# Contributing to Practical Python Projects

Thank you for your interest in contributing. This repository is an open-source collection of 10 progressive Python projects built with test-driven development and clean software architecture.

We welcome bug fixes, documentation improvements, additional unit tests, and stretch feature implementations.

---

## Code Standards

Every contribution must follow these four core principles:

1. **Separation of Concerns**: Keep calculation and business logic pure. Never place `input()`, `print()`, or terminal formatting inside domain functions in `utils.py`. All user interaction belongs in `main.py`.
2. **Accurate Arithmetic**: Always use `Decimal` for currency and financial calculations. Never use binary `float` types for monetary values.
3. **Explicit Validation**: Validate function arguments at boundaries. Raise specific exceptions (`ValueError`, custom domain exceptions) when inputs break rules.
4. **Automated Test Coverage**: Every change or new feature must include automated `pytest` unit tests covering both valid inputs and error conditions.

---

## Local Development Setup

### 1. Fork and Clone
```bash
git clone https://github.com/jezreal-dev/python_practice_projects.git
cd python_practice_projects
```

### 2. Configure Python Environment
Python 3.12 or newer is required.

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the environment
# On Linux / macOS / WSL:
source .venv/bin/activate
# On Windows PowerShell:
# .venv\Scripts\Activate.ps1

# Install testing dependencies
pip install pytest
```

### 3. Run Existing Tests
Ensure all existing tests pass before writing new code:

```bash
pytest -v
```

---

## Pull Request Workflow

1. **Branch Naming**: Create a topic branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```
2. **Commit Messages**: Follow standard conventional commit format:
   - `feat(project_name): add feature description`
   - `fix(project_name): fix bug description`
   - `test(project_name): add unit test coverage`
   - `docs(project_name): update documentation`
3. **Verification**: Run `pytest` across the repository to verify that your changes introduce zero regressions.
4. **Open a PR**: Push your branch to your fork and submit a Pull Request against the `main` branch. Provide a brief summary of the change and test results in the description.

---

## Questions and Discussions

If you spot a bug or want to suggest a stretch feature, open an issue on the repository issue tracker with reproduction steps or design details.
