# Practical Python Projects

A progressive, test-driven collection of 10 Python applications built from the ground up, moving from foundational CLI tools to networking and systems programming.

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Testing](https://img.shields.io/badge/tested%20with-pytest-yellow.svg)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Overview

This repository documents the hands-on engineering of 10 practical Python projects. Instead of writing single-file scripts or following line-by-line tutorials, each project enforces production habits:

- Pure domain logic isolated from user input and output.
- Strict data validation using custom exception types.
- Exact monetary calculations using Python's `Decimal` module.
- Full test automation using `pytest` before completing any milestone.
- Realistic persistence pipelines, evolving from raw text to structured JSON, relational schemas, external APIs, and socket networking.

---

## Architecture

The diagram below illustrates the decoupled architecture implemented across our projects, showing how data moves from user input through validation to permanent storage:

![Architecture Data Flow](assets/architecture_flow.svg)

Each application separates responsibilities across three boundaries:
1. **User Interface Layer (`main.py`)**: Handles command-line menus, user prompts, screen clearing, and output formatting.
2. **Domain Service Layer (`utils.py`)**: Executes calculations, enforces validation rules, generates identifiers, and returns pure data structures.
3. **Storage Layer (`utils.py`)**: Serializes domain objects into storage formats (e.g. JSON) and reconstructs them into Python types during load.

---

## Roadmap and Progress

| # | Project | Focus Area | Status | Documentation & Code |
| :-: | :--- | :--- | :-: | :--- |
| **01** | **Expense Tracker** | Invariant validation, `Decimal` arithmetic, JSON persistence | Completed | [Documentation](expense_tracker/README.md) \| [Code](expense_tracker/) |
| **02** | **Quiz Game** | Question pools, state management, scoring algorithms, random seeding | In Progress | [Project Folder](quiz/) |
| **03** | **To-Do CLI** | CRUD operations, priority filtering, date parsing, JSON persistence | Queued | [Project Folder](to_do_cli_application/) |
| **04** | **Library Manager** | Entity relationships, borrowing rules, search indexing | Queued | [Project Folder](library_management_system/) |
| **05** | **Banking System** | Object-oriented design, encapsulation, balance invariants | Queued | [Project Folder](simple_banking_system/) |
| **06** | **Inventory System** | Inventory counts, sales processing, restock alerts | Queued | [Project Folder](inventory_management_system/) |
| **07** | **Weather CLI** | External REST APIs, HTTP requests, environment variables | Queued | [Project Folder](weather_CLI_application/) |
| **08** | **Finance Analyzer** | CSV parsing, transaction aggregation, date grouping, analytics | Queued | [Project Folder](personal_finance_analyzer/) |
| **09** | **Password Manager** | Local encryption, secure hashing, master key verification | Queued | [Project Folder](password_manager/) |
| **10** | **Chat Application** | TCP socket networking, multi-client server, message broadcasting | Queued | [Project Folder](command_line_chat_application/) |

---

## Core Engineering Rules

Every project adheres to these non-negotiable implementation rules:

1. **Exact Precision for Currency**: Binary floating-point numbers (`float`) introduce rounding errors (for example, `0.1 + 0.2 = 0.30000000000000004`). All monetary amounts use Python's `Decimal` type.
2. **Zero I/O in Calculation Routines**: Domain functions must never call `input()` or `print()`. They receive values as parameters, validate them, and return results or raise typed exceptions.
3. **Monotonic Surrogate Keys**: Record identifiers must never depend on `len(collection) + 1`, which creates duplicate keys after deletions. IDs use `max(existing_ids, default=0) + 1`.
4. **Explicit Type Rehydration**: Storage serialization must be two-way. When loading from JSON or text, strings must be explicitly converted back into their domain types (`Decimal`, `date`, `int`).
5. **Continuous Unit Testing**: Every project requires automated tests covering valid scenarios, boundary limits, and error handling.

---

## Getting Started

### Prerequisites
- Python 3.12 or newer
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jezreal-dev/python_practice_projects.git
   cd python_practice_projects
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv

   # Linux / macOS / WSL:
   source .venv/bin/activate

   # Windows PowerShell:
   # .venv\Scripts\Activate.ps1
   ```

3. Install test dependencies:
   ```bash
   pip install pytest
   ```

4. Run the test suite:
   ```bash
   # Run all tests across the repository
   pytest -v

   # Run tests for a specific project
   cd expense_tracker
   pytest tests -v
   ```

---

## Project Structure

```text
python_practice_projects/
├── README.md                              # Repository overview and progress matrix
├── CONTRIBUTING.md                        # Development and pull request guide
├── LICENSE                                # MIT license
├── assets/
│   └── architecture_flow.svg              # Animated architecture diagram
│
├── expense_tracker/                       # Project 01 (Completed)
│   ├── README.md                          # Technical specification and post-mortem
│   ├── main.py                            # CLI user interface
│   ├── utils.py                           # Core calculations and JSON storage
│   ├── expenses_log.json                  # Data file
│   └── tests/
│       └── test_expense_tracker.py        # 17 automated unit tests
│
├── quiz/                                  # Project 02 (In Progress)
├── to_do_cli_application/                 # Project 03
├── library_management_system/             # Project 04
├── simple_banking_system/                 # Project 05
├── inventory_management_system/           # Project 06
├── weather_CLI_application/               # Project 07
├── personal_finance_analyzer/             # Project 08
├── password_manager/                      # Project 09
└── command_line_chat_application/         # Project 10
```

---

## Contributing

Contributions, feedback, and issue reports are welcome. Review [CONTRIBUTING.md](CONTRIBUTING.md) for local development setup, code conventions, and pull request guidelines.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for full details.
