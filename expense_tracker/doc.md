# Project 1: Expense Tracker — Complete Engineering Retrospective & Learning Log

> An exhaustive, unfiltered technical record of the design, implementation, failures, bug post-mortems, software design principles, and lessons learned while building the Expense Tracker CLI engine.

---

## Table of Contents
1. [Project Overview & Core Architecture](#1-project-overview--core-architecture)
2. [Software Engineering Principles in Action](#2-software-engineering-principles-in-action)
   - [Separation of Concerns (SoC)](#separation-of-concerns-soc)
   - [Single Responsibility Principle (SRP)](#single-responsibility-principle-srp)
   - [SOLID Principles in Procedural Python](#solid-principles-in-procedural-python)
   - [CRUD Architecture Mapping](#crud-architecture-mapping)
3. [The Unfiltered Bug Chronicles (16 Real Bugs & Autopsies)](#3-the-unfiltered-bug-chronicles-16-real-bugs--autopsies)
4. [Domain Invariants & Technical Contracts](#4-domain-invariants--technical-contracts)
5. [Automated Test Harness & Verification](#5-automated-test-harness--verification)
6. [The Execution Guard: How `__name__ == '__main__'` Works](#6-the-execution-guard-how-__name__--__main__-works)
7. [System Design Horizons & Recommended Reading](#7-system-design-horizons--recommended-reading)

---

## 1. Project Overview & Core Architecture

The **Expense Tracker** is a terminal-based personal finance ledger. The objective of this project was to transition from writing exploratory Python scripts to practicing production-grade software engineering.

### The Problem with Naive Scripting
Junior implementations typically write the entire program in a single `main.py` file, prompting the user with `input()`, converting numbers with `float()`, calculating totals inside print statements, and writing raw text to files on the fly. This creates three fatal flaws:
1. **Financial inaccuracy**: Float math introduces rounding errors.
2. **Untestable code**: Logic cannot be tested automatically with `pytest` without mocking the user's keyboard.
3. **Fragile persistence**: Deleting an item breaks ID numbering, and typing a comma in a description corrupts flat text files.

### Architectural Solution
The Expense Tracker separates responsibilities into distinct layers:

```
+--------------------------------------------------------------------------+
|                     Presentation Layer (main.py)                         |
|   - Terminal ANSI menus & screen clearing (os.system("clear"))           |
|   - User input collection & validation retry loops                       |
|   - Centralized cancellation handler (prompt_input & ActionCancelled)    |
|   - Formatting tables, currency symbols (₦), and error banners           |
+--------------------------------------------------------------------------+
                                    |
                                    v
+--------------------------------------------------------------------------+
|                    Domain Service Layer (utils.py)                       |
|   - Pure business logic (add, calculate totals, filter, delete)          |
|   - Domain invariant validation (validate_amount, non-empty text)        |
|   - Monotonic collision-free surrogate ID generation                     |
|   - Custom exception hierarchy (InvalidExpenditureError tree)            |
|   - ZERO terminal I/O (no input(), no print())                           |
+--------------------------------------------------------------------------+
                                    |
                                    v
+--------------------------------------------------------------------------+
|                     Persistence Engine (utils.py)                        |
|   - JSON serialization with schema enforcement (save_ledger_to_json)     |
|   - Explicit type rehydration (load_ledger_from_json)                    |
|   - Cold-start bootstrapping & corrupted file recovery                   |
|   - File: expenses_log.json                                              |
+--------------------------------------------------------------------------+
                                    ^
                                    | (verifies)
+--------------------------------------------------------------------------+
|              Automated Test Suite (tests/test_expense_tracker.py)        |
|   - 17 pytest unit tests covering nominal, boundary, and error paths     |
|   - Isolated file testing using pytest tmp_path fixtures                 |
+--------------------------------------------------------------------------+
```

---

## 2. Software Engineering Principles in Action

### Separation of Concerns (SoC)
- **The Rule**: `main.py` is the Presentation Layer; `utils.py` is the Domain & Storage Layer.
- **Why It Matters**: By stripping all `input()` and `print()` calls out of `utils.py`, the business logic becomes **pure and deterministic**. Given the same arguments, it always returns the exact same result or raises the exact same typed exception.
- **Practical Benefit**: The test suite can run 17 automated tests in **0.11 seconds** without needing mock objects or interactive input simulation. Furthermore, if the terminal interface is replaced tomorrow with a web API (FastAPI) or a desktop GUI (PyQt), `utils.py` requires zero modifications.

### Single Responsibility Principle (SRP)
Every function in the codebase has one, and only one, reason to change:
- `add_expense()`: Only changes if the rules for validating or structuring an expense record change.
- `calculate_total_expenditure()`: Only changes if the formula for calculating ledger totals changes.
- `calculate_category_aggregate()`: Only changes if the category grouping logic changes.
- `delete_expense_by_id()`: Only changes if the identification and removal mechanism changes.
- `save_ledger_to_json()`: Only changes if the storage serialization format changes.
- `load_ledger_from_json()`: Only changes if the deserialization or rehydration rules change.
- `prompt_input()`: Only changes if user input collection or cancellation triggers change.

### SOLID Principles in Procedural Python
While SOLID is often taught in Object-Oriented Programming, its foundational principles apply directly to clean modular procedural Python:
1. **S — Single Responsibility**: Each function performs one logical task. Logic is segregated from display.
2. **O — Open/Closed Principle**: We can add new reporting functions (such as monthly summaries or percentage breakdowns) by writing new pure functions in `utils.py` without modifying existing calculation functions.
3. **L — Liskov Substitution**: Our custom exception hierarchy (`InvalidAmountError` and `InvalidCategoryError` inheriting from `InvalidExpenditureError`, which inherits from `ValueError`) allows caller code to catch either the specific error or the broad domain base class interchangeably.
4. **I — Interface Segregation**: Functions require only the parameters they actually operate on (e.g. `calculate_total_expenditure` only needs the `ledger` list, not file paths or configuration flags).
5. **D — Dependency Inversion**: Higher-level operations accept file paths as parameters (`filepath: str | Path`) rather than hardcoding static paths inside core functions.

### CRUD Architecture Mapping
The application fully implements the four operations of persistent storage:
- **Create (C)**: Handled by `add_expense()` in memory, persisted via `save_ledger_to_json()`.
- **Read (R)**: Handled by `view_expenses()`, `calculate_total_expenditure()`, `calculate_category_aggregate()`, and `filter_by_category()`.
- **Update (U)**: In this ledger model, transactions are immutable financial facts. Modifications occur through explicit deletion (`delete_expense_by_id`) and re-creation to maintain audit trails.
- **Delete (D)**: Handled by `delete_expense_by_id()` with referential integrity checks (`ExpenseNotFoundError`) and immediate write-through file synchronization.

---

## 3. The Unfiltered Bug Chronicles (16 Real Bugs & Autopsies)

This section documents every failure, bug, syntax error, and edge case encountered during development, including the exact root causes and fixes.

### Bug 01: Binary Floating-Point Rounding Error
- **What Failed**: Using Python's built-in `float` for currency caused calculations like `0.1 + 0.2` to evaluate to `0.30000000000000004`.
- **Root Cause**: Python floats adhere to IEEE 754 double-precision binary representations. Base-10 decimal fractions cannot be represented exactly in base-2 binary.
- **How It Was Fixed**: Replaced all floats with Python's standard library `from decimal import Decimal`.
- **Lesson Learned**: *Never use binary floating-point numbers for money. Always enforce exact fixed-point arithmetic (`Decimal`).*

### Bug 02: I/O Coupling Inside Domain Functions
- **What Failed**: `input()` and `print()` statements were placed directly inside `add_expense()` and calculation functions.
- **Root Cause**: Conflating user interaction with business calculation rules.
- **How It Was Fixed**: Stripped all I/O from `utils.py`. Domain functions take arguments, validate invariants, return values, or raise typed exceptions. All `input()` and `print()` calls were moved to `main.py`.
- **Lesson Learned**: *Keep business logic pure. If a function pauses for keyboard input, it cannot be easily automated in a CI/CD test runner.*

### Bug 03: Surrogate Primary Key Collisions (`len + 1` Trap)
- **What Failed**: Record IDs were originally generated using `len(ledger) + 1`. Adding 3 expenses gave IDs 1, 2, 3. When expense 2 was deleted, `len(ledger)` became 2. Adding a new expense assigned ID 3, creating duplicate primary keys!
- **Root Cause**: Confusing collection cardinality (number of items currently in the list) with a monotonically increasing sequence.
- **How It Was Fixed**: Changed the ID generator to evaluate the maximum existing ID:
  ```python
  new_id = max((item["id"] for item in ledger), default=0) + 1
  ```
- **Lesson Learned**: *Surrogate primary keys must be monotonic and independent of mutable collection length.*

### Bug 04: Plain-Text CSV Delimiter Collisions
- **What Failed**: In Milestone 3, saving an expense with the description `"Coffee, milk, and sugar"` caused `line.split(",")` to break the record into 7 fields instead of 5, corrupting the rehydrated data.
- **Root Cause**: The comma was used as both the column separator and literal text inside the user's description.
- **How It Was Fixed**: Enforced bounded splitting using `line.split(",", maxsplit=4)`.
- **Lesson Learned**: *Flat delimited files are fragile. Delimited protocols must either enforce strict field counts via `maxsplit` or migrate to structured formats like JSON.*

### Bug 05: Premature Abstraction vs. Foundational Mechanics
- **What Failed**: Temptation to skip plain-text file parsing and jump immediately to Python's `csv` module in Milestone 3.
- **Root Cause**: Reaching for higher-level library abstractions before mastering basic file stream handling, newline management, and parsing.
- **How It Was Fixed**: Followed the strict roadmap progression: built raw string parsing first, then upgraded to JSON in Milestone 4, and reserved CSV for Project 8.
- **Lesson Learned**: *Master low-level mechanics before adopting abstractions. When abstractions fail in production, only developers who understand the underlying mechanics can diagnose the issue.*

### Bug 06: Python Compound Statement Syntax Error in `try...except`
- **What Failed**: The test runner halted with `SyntaxError: invalid syntax` on:
  ```python
  except:
      json.JSONDecodeError():
      return []
  ```
- **Root Cause**: In Python syntax grammar, an exception handler defines its target type directly on the header line (`except <Type>:`). Instantiating `json.JSONDecodeError():` on its own line with a colon was an illegal syntax construct.
- **How It Was Fixed**: Refactored to canonical exception syntax:
  ```python
  except json.JSONDecodeError:
      return []
  ```
- **Lesson Learned**: *The `except` header declares what exception to catch; the indented body declares what to do when that exception occurs.*

### Bug 07: Silent Type Degradation During JSON Deserialization
- **What Failed**: After loading expenses from `expenses_log.json`, mathematical operations failed with `TypeError` because amounts were loaded as strings (e.g. `"15.50"` instead of `Decimal("15.50")`).
- **Root Cause**: JSON is a lightweight transport format supporting only strings, numbers, booleans, arrays, objects, and null. It has no native concept of Python's `Decimal` or `datetime.date` objects.
- **How It Was Fixed**: Built an explicit type rehydration pipeline in `load_ledger_from_json`:
  ```python
  "amount": Decimal(item["amount"]),
  "date": date.fromisoformat(item["date"])
  ```
- **Lesson Learned**: *Data at Rest is distinct from Data in Memory. A persistence layer must explicitly reconstruct domain value objects from storage primitives.*

### Bug 08: Dead Imports and Outdated Test Names
- **What Failed**: `import json` was left at the top of `main.py` and `tests/test_expense_tracker.py` without being used. Additionally, the test was named `test_save_and_load_plain_text_roundtrip` even though it was testing JSON persistence.
- **Root Cause**: Fast iteration leaving behind dead code and stale documentation.
- **How It Was Fixed**: Removed unused imports and renamed the test to `test_save_and_load_json_roundtrip` using `expenses.json`.
- **Lesson Learned**: *Dead code and misleading test names create cognitive debt. Keep tests aligned with the code they verify.*

### Bug 09: Test Coverage Gap (Unchecked Error Branch)
- **What Failed**: We added `except json.JSONDecodeError: return []` in `utils.py`, but had no test verifying that corrupted files actually returned `[]`.
- **Root Cause**: Testing only the "happy path" (nominal roundtrip) while neglecting the error recovery path.
- **How It Was Fixed**: Added `test_load_ledger_corrupted_json(tmp_path)` which writes malformed text (`"{broken json"`) and asserts that `load_ledger_from_json` returns `[]`.
- **Lesson Learned**: *Continuous Testing Mandate: If you write defensive code to catch an error, write a test that intentionally triggers that error to verify the recovery branch.*

### Bug 10: Auditor Finding 1 — Menu Choice Whitespace Leakage
- **What Failed**: Typing `"1 "` in the main menu was accepted as option 1.
- **Root Cause**: `main.py` called `.strip()` on the raw input: `choice = input(...).strip()`. This stripped trailing spaces and matched `if choice == "1":`.
- **How It Was Fixed**: Captured the raw input without stripping, validated strictly using `raw_choice.isdigit()`, and verified the range `1 <= int(raw_choice) <= 7`.
- **Lesson Learned**: *Do not prematurely strip input if trailing whitespace is considered invalid. `isdigit()` ensures every single character is a digit.*

### Bug 11: Auditor Finding 2 — Frustrating Input Error Bounce
- **What Failed**: Mistyping an expense amount (e.g. typing `"12.oo"` instead of `"12.00"`) displayed an error and immediately kicked the user back to the main menu.
- **Root Cause**: `get_expense()` executed a single try/catch block that did an early `return` on exception.
- **How It Was Fixed**: Wrapped the amount prompt in an internal `while True:` retry loop so users can re-enter numbers immediately without losing context.
- **Lesson Learned**: *Design resilient CLI prompts. An error should prompt for correction in place rather than aborting the entire workflow.*

### Bug 12: Auditor Finding 3 — Missing Batch Receipt Entry Flow
- **What Failed**: After adding an expense, the app returned to the root menu. Users entering 10 receipts had to re-select option `1` ten times.
- **Root Cause**: No post-success continuation loop.
- **How It Was Fixed**: Added a post-save prompt: `again = prompt_input("Add another expense? (y/n): ")`. If the user confirms, the loop continues in place.
- **Lesson Learned**: *Optimize common user workflows. Batch data entry is standard in financial accounting applications.*

### Bug 13: Tuple Equality Logic Trap (`==` vs. `in`)
- **What Failed**: In `get_expense`, typing `cancel` did not exit:
  ```python
  if raw_input == ('q', 'cancel'):
      return
  ```
- **Root Cause**: In Python, `==` tests equality. A string (`"cancel"`) can never equal a tuple `('q', 'cancel')`. The condition always evaluated to `False`.
- **How It Was Fixed**: Used the membership operator `in`:
  ```python
  if raw_input.lower() in ('q', 'cancel'):
      return
  ```
- **Lesson Learned**: *Use `==` for exact value comparison; use `in` to test if an element belongs to a collection.*

### Bug 14: The Double "Press Enter" UX Friction
- **What Failed**: After exiting `get_expense` (either by cancelling or by answering `n` to "Add another"), the terminal paused and printed `Press [Enter] to return to the main menu...`.
- **Root Cause**: In `main()`, the `input("\nPress [Enter]...")` call was placed at the very bottom of the loop, executing after every single menu branch.
- **How It Was Fixed**: Added `continue` immediately after calling `get_expense(ledger)` to bypass the pause gate and re-render `menu()` immediately.
- **Lesson Learned**: *Interactive flows that manage their own exit prompts do not need a secondary pause gate.*

### Bug 15: `return` vs. `raise` with Custom Exceptions
- **What Failed**: The cancellation helper returned an exception instead of triggering it:
  ```python
  def prompt_input(prompt_text: str) -> str:
      val = input(prompt_text).strip()
      if val.lower() in ('q', 'cancel'):
          return ActionCancelled()  # Bug!
      return val
  ```
- **Root Cause**: In Python, `return` hands an object back as normal data. It does not trigger control-flow interruption. Consequently, `Decimal(ActionCancelled())` crashed with a `TypeError`.
- **How It Was Fixed**: Replaced `return` with `raise`:
  ```python
  if val.lower() in ('q', 'cancel'):
      raise ActionCancelled()
  ```
- **Lesson Learned**: *Exceptions must be raised (`raise`), not returned (`return`). Raising activates Python's stack unwinding to the nearest matching `except` block.*

### Bug 16: Copy-Paste Variable Trap in Description Loop
- **What Failed**: Leaving the description empty was accepted without error:
  ```python
  while True:
      raw_description = prompt_input("Enter expense description: ")
      if raw_category:  # Bug!
          break
      print("Error: Category cannot be empty. Please try again.")
  ```
- **Root Cause**: Copy-pasting the category loop logic without updating `if raw_category:` to `if raw_description:`. Because `raw_category` was already non-empty from the previous step, the loop broke immediately.
- **How It Was Fixed**: Corrected the condition to `if raw_description:` and updated the error message to specify `Description`.
- **Lesson Learned**: *Copy-paste code duplication introduces silent semantic bugs. Always verify variable names when adapting cloned blocks.*

---

## 4. Domain Invariants & Technical Contracts

### The Expense Data Model
```python
{
    "id": int,              # Monotonically increasing surrogate key (>= 1)
    "date": datetime.date,  # Gregorian calendar date
    "category": str,        # Non-empty string
    "amount": Decimal,      # Positive arbitrary-precision decimal (> 0)
    "description": str     # Non-empty narrative string
}
```

### Invariant Rules Enforced
1. **Amount Invariant**: Must be coercible to `Decimal` and strictly positive ($> 0$). Violations raise `InvalidAmountError` or `InvalidOperation`.
2. **Category Invariant**: Must contain at least one non-whitespace character. Violations raise `InvalidCategoryError`.
3. **Description Invariant**: Must contain at least one non-whitespace character. Violations raise `InvalidExpenditureError`.
4. **Referential Integrity Invariant**: Deleting an ID absent from the ledger raises `ExpenseNotFoundError`.

---

## 5. Automated Test Harness & Verification

The project is protected by 17 automated tests written with `pytest`. Tests adhere to the **AAA Pattern (Arrange, Act, Assert)**:

```bash
# Execute the complete test suite
../.venv/bin/python -m pytest tests -v
```

### Complete Test Inventory
| Test Function | What It Validates |
| :--- | :--- |
| `test_add_expense_valid_record` | Nominal record creation and list mutation |
| `test_add_expense_negative_amount_fails` | Rejection of negative amounts (`InvalidAmountError`) |
| `test_add_expense_zero_amount_fails` | Rejection of zero amount ($0.00$) |
| `test_add_expense_empty_category_fails` | Rejection of empty or whitespace category |
| `test_add_expense_empty_description_fails`| Rejection of empty or whitespace description |
| `test_calculate_total_expenditure` | Total sum calculation on populated ledger |
| `test_calculate_total_expenditure_multiple_items` | Accurate summation across multiple items |
| `test_add_expense_saves_authentic_string_type` | Category and description remain strings |
| `test_add_expense_generates_sequential_ids` | Sequential ID numbering (1, 2, 3...) |
| `test_delete_expense_by_id_success` | Record deletion by ID and list reduction |
| `test_delete_expense_by_id_not_found_raises` | `ExpenseNotFoundError` raised on missing ID |
| `test_calculate_category_aggregate` | Accurate category totals |
| `test_filter_by_category` | Filtering records matching target category |
| `test_get_category_counts` | Category frequency counting |
| `test_load_ledger_nonexistent_file` | Missing file cold-start returns `[]` |
| `test_save_and_load_json_roundtrip` | Full JSON serialization and type rehydration |
| `test_load_ledger_corrupted_json` | Corrupted JSON recovery returns `[]` |

---

## 6. The Execution Guard: How `__name__ == '__main__'` Works

At the bottom of `main.py`:
```python
if __name__ == "__main__":
    main()
```

### How Python Sets `__name__`
- When you execute a file directly (`python3 main.py`), Python sets `__name__ = "__main__"`. The condition evaluates to `True`, launching `main()`.
- When another file imports it (`from main import DATA_FILE`), Python sets `__name__ = "main"`. The condition evaluates to `False`, preventing the interactive CLI menu loop from starting.

### Why This Matters
Without this guard, running automated tests or importing constants from `main.py` would instantly hijack the terminal and block test execution.

---

## 7. System Design Horizons & Recommended Reading

To continue expanding your architectural intuition throughout the remaining 9 projects, study these four foundational books:

### 1. *Architecture Patterns with Python* by Harry Percival & Bob Gregory (O'Reilly)
- **Core Concept**: Domain-Driven Design (DDD), the Repository Pattern, and maintaining an I/O-free core.
- **Connection to Project 1**: Formalizes what you built in `utils.py` into Domain Services and Repositories. Available free online at `cosmicpython.com`.

### 2. *A Philosophy of Software Design* by John Ousterhout
- **Core Concept**: Designing "Deep Modules" (modules with simple interfaces that hide substantial internal complexity).
- **Connection to Project 1**: Your `add_expense()` function is a deep interface—the caller simply passes strings and numbers, while the function handles validation, date generation, ID sequencing, and record creation internally.

### 3. *Designing Data-Intensive Applications* by Martin Kleppmann (O'Reilly)
- **Core Concept**: Chapters 3 & 4 (Storage Engines, Serialization Formats, Schema Evolution).
- **Connection to Project 1**: Directly explains why JSON does not preserve Python types, how delimiter-based flat files scale, and how storage engines guarantee consistency.

### 4. *Clean Code in Python* by Mariano Anaya (Packt)
- **Core Concept**: Idiomatic Python, proper exception hierarchies, context managers (`with`), and the Single Responsibility Principle.
- **Connection to Project 1**: Reinforces why specific custom exceptions are superior to generic `ValueError` calls.

---

*Certified & Completed: Project 1 (Expense Tracker). All 17 unit tests passing green. Ready for Stage 1 — Project 2: Quiz / Trivia Game.*
