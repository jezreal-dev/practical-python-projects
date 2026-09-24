from decimal import Decimal
from datetime import date
from typing import Any
from pathlib import Path
import json

class InvalidExpenditureError(ValueError):
    """Base exception for all expenditure domain invariant violations."""
    pass
class InvalidAmountError(InvalidExpenditureError):
    """Raised specifically when a monetary amount breaks domain rules."""
    pass
class InvalidCategoryError(InvalidExpenditureError):
    """Raised specifically when a category string breaks database invariants."""
    pass
class ExpenseNotFoundError(InvalidExpenditureError):
    """Raised when an operation targes an expense ID that does not exist"""
    pass


def add_expense(ledger: list[dict[str, Any]], amount: Decimal, category: str, description: str,) -> dict[str, Any]:
    if amount <= Decimal("0"):
        raise InvalidAmountError("Monetary Rule Violation: Expense amount must be greater than zero.")

    sanitized_category = category.strip().capitalize()
    sanitized_description = description.strip().capitalize()

    if not sanitized_category:
        raise InvalidCategoryError("Text invariant Violation: Category cannot be empty or whitespace-only.")
    if not sanitized_description:
        raise InvalidExpenditureError("Text invariant violation: Description cannot be empty or whitespace-only.")

    new_id = max((item["id"] for item in ledger), default = 0) + 1 
    # Assemble the sanitized input data to a dictionary
    new_expense: dict[str, Any] = {
        "id": new_id,
        "amount": amount,
        "category": sanitized_category,
        "description": sanitized_description,
        "date": date.today(),
    }
    ledger.append(new_expense)
    return new_expense


def validate_amount(amount: Decimal) -> None:
    if amount <= Decimal("0"):
        raise InvalidAmountError("Monetary Rule Violation: Expense amount must be greater than zero.")


def calculate_total_expenditure(ledger: list[dict[str, Any]]) -> Decimal:
    total = Decimal("0.00")
    for item in ledger:
        total += item["amount"]
    return total


def calculate_category_aggregate(ledger: list[dict[str, Any]]) -> dict[str, Decimal]:
    category_totals = {}
    for item in ledger:
        category = item["category"]
        amount = item["amount"]
        if category not in category_totals:
            category_totals[category] = Decimal("0.00")
        category_totals[category] += amount
    return category_totals


def filter_by_category(ledger: list[dict[str, Any]], query_category: str) -> list[dict[str, Any]]:
    target = query_category.strip().capitalize()
    if not target:
        raise InvalidExpenditureError("Search Failure: Category query string cannot be empty or whitespace-only.")
    matching_records = [item for item in ledger if item["category"] == target]
    return matching_records


def delete_expense_by_id(ledger: list[dict[str, Any]], expense_id: int) -> dict[str, Any]:
    for index, item in enumerate(ledger):
        if item.get("id") == expense_id:
            delete_record = ledger.pop(index)
            return delete_record
    raise ExpenseNotFoundError(f"Expense with ID {expense_id} does not exist.")

def get_category_counts(ledger: list[dict[str, Any]]) -> dict[str, int]:
    counts = {}

    for item in ledger:
        category = item["category"]
        counts[category] = counts.get(category, 0) + 1
    return counts


def save_ledger_to_json(ledger: list[dict[str, Any]], filepath: str | Path) -> None:
    path = Path(filepath)

    serializable_data = []
    for item in ledger:
        record = {
            "id": item["id"],
            "date": item["date"].isoformat(),
            "category": item["category"],
            "amount": str(item["amount"]),
            "description": item["description"],
        }
        serializable_data.append(record)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(serializable_data, file, indent=4)


def load_ledger_from_json(filepath: str | Path) -> list[dict[str, Any]]:
    path = Path(filepath)
    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as file:
        try:
            raw_data = json.load(file)
        except json.JSONDecodeError:
            return []

    reload_ledger = []
    for item in raw_data:
        record = {
            "id": int(item["id"]),
            "date": date.fromisoformat(item["date"]),
            "category": item["category"],
            "amount": Decimal(item["amount"]),
            "description": item["description"],
        }
        reload_ledger.append(record)
    return reload_ledger