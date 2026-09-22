from decimal import Decimal
from datetime import date
from typing import Any

class InvalidExpenditureError(ValueError):
    """Base exception for all expenditure domain invariant violations."""
    pass

class InvalidAmountError(InvalidExpenditureError):
    """Raised specifically when a monetary amount breaks domain rules."""
    pass

class InvalidCategoryError(InvalidExpenditureError):
    """Raised specifically when a category string breaks database invariants."""
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

    # Assembling the sanitized input data to the dictionary
    new_expense: dict[str, Any] = {
        "amount": amount,
        "category": sanitized_category,
        "description": sanitized_description,
        "date": date.today(),
    }

    ledger.append(new_expense)
    return new_expense


def calculate_total_expenditure(ledger: list[dict[str, Any]]) -> Decimal:
    total = Decimal("0.00")
    for item in ledger:
        total += item["amount"]
    return total