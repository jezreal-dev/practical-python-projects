import pytest
from datetime import date
from decimal import Decimal
from utils import (
   add_expense, 
   calculate_total_expenditure,
   InvalidExpenditureError,
   InvalidAmountError,
   InvalidCategoryError,
)

def test_add_expense_valid_record():
    # 1. Arrange
    test_ledger = []
    input_amount = Decimal("45.50")
    input_category = " groceries "
    input_description = "weekly stock"

    # 2. Act
    returned_dict = add_expense(
       test_ledger, input_amount, input_category, input_description
    )

    # 3. Assert
    assert returned_dict["amount"] == Decimal("45.50")
    assert returned_dict["category"] == "Groceries"
    assert returned_dict["description"] == "Weekly stock"
    assert isinstance(returned_dict["date"], date)
    assert len(test_ledger) == 1
    assert test_ledger[0] == returned_dict


def test_add_expense_negative_amount_fails():
    """Proves that passing a negative monetary amount triggers an InvalidAmountError"""
    test_ledger = []
    with pytest.raises(InvalidAmountError):
        add_expense(
            test_ledger, Decimal("-15.00"), "Food", "Dinner"
        )


def test_add_expense_zero_amount_fails():
    """Proves that passing a zero value amount triggers an InvalidAmountError."""
    test_ledger = []
    with pytest.raises(InvalidAmountError):
        add_expense(
            test_ledger, Decimal("0.00"), "Utilities", "Electric bill"
        )


def test_add_expense_empty_category_fails():
    """Proves that whitespace-only categories trigger an InvalidCategoryError."""
    test_ledger = []
    with pytest.raises(InvalidCategoryError):
        add_expense(
            test_ledger, 
            Decimal("10.00"), "   ", "Valid description"
        )


def test_add_expense_empty_description_fails():
    """Proves that blank descriptions trigger the base InvalidExpenditureError."""
    test_ledger = []
    with pytest.raises(InvalidExpenditureError):
        add_expense(
            test_ledger, Decimal("10.00"), "Entertainment", ""
        )


def test_calculate_total_expenditure():
    """Verifies that an empty tracking ledger defaults cleanly to 0.00."""
    test_ledger = []
    total = calculate_total_expenditure(test_ledger)
    assert total == Decimal("0.00")

def test_calculate_total_expenditure_multiple_items():
    """Verifies that the sum computation accumulates multiple Decimals perfectly."""
    test_ledger = [
        {"amount": Decimal("10.50"), "category": "Food"},
        {"amount": Decimal("4.50"), "category": "Transport"},
        {"amount": Decimal("100.00"), "category": "Bills"},
    ]

    total = calculate_total_expenditure(test_ledger)
    assert total == Decimal("115.00")

def test_add_expense_saves_authentic_string_type():
    test_ledger = []
    returned_record = add_expense(
        test_ledger, Decimal("12.00"), " food ", "Lunch"
    )

    assert isinstance(returned_record["category"], str), (
        "Architecture Violation: Saved category is a method object, not a string! "
        "Check your code and ensure you called the string methods using parentheses ()."
    )
    assert returned_record["category"] == "Food"