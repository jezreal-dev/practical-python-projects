import pytest
from datetime import date
from decimal import Decimal
from utils import (
   add_expense, 
   calculate_total_expenditure,
   calculate_category_aggregate,
   InvalidExpenditureError,
   InvalidAmountError,
   InvalidCategoryError,
   get_category_counts,
   filter_by_category,
   delete_expense_by_id,
   ExpenseNotFoundError,
   save_ledger_to_file,
   load_ledger_from_file,
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

def test_add_expense_generates_sequential_ids():
    ledger = []
    # 2. Act
    first = add_expense(ledger, Decimal("10.00"), "Food", "Breakfast")
    second = add_expense(ledger, Decimal("20.00"), "Transport", "Bus")
    third = add_expense(ledger, Decimal("30.00"), "Food", "Dinner")
    # 3. Assert
    assert first["id"] == 1
    assert second["id"] == 2
    assert third["id"] == 3
    # Now simulate deletion of item 2:
    delete_expense_by_id(ledger, 2)
    # Add a fourth expense:
    fourth = add_expense(ledger, Decimal("40.00"), "Bills", "Internet")
    # The new ID must be 4, NOT 3 (proving collision immunity)
    assert fourth["id"] == 4


def test_delete_expense_by_id_success():
    ledger = []
    item1 = add_expense(ledger, Decimal("15.00"), "Food", "Lunch")
    item2 = add_expense(ledger, Decimal("50.00"), "Utilities", "Power")
    # 2. Act: Delete item 1
    removed_record = delete_expense_by_id(ledger, 1)
    # 3. Assert
    assert removed_record["id"] == 1
    assert removed_record["category"] == "Food"
    assert len(ledger) == 1
    assert ledger[0]["id"] == 2


def test_delete_expense_by_id_not_found_raises():
    ledger = []
    # 1. Arrange
    ledger = []
    add_expense(ledger, Decimal("10.00"), "Food", "Snack")
    # 2. Act & Assert: Target ID 999 does not exist
    with pytest.raises(ExpenseNotFoundError):
        delete_expense_by_id(ledger, 999)
    # Verify ledger was not mutated
    assert len(ledger) == 1


def test_calculate_category_aggregate():
    ledger = []
    add_expense(ledger, Decimal("10.00"), "Food", "Lunch")
    add_expense(ledger, Decimal("15.50"), "Food", "Dinner")
    add_expense(ledger, Decimal("40.00"), "Transport", "Fuel")
    # 2. Act
    summary = calculate_category_aggregate(ledger)
    # 3. Assert
    assert summary["Food"] == Decimal("25.50")
    assert summary["Transport"] == Decimal("40.00")
    assert "Bills" not in summary


def test_filter_by_category():
    ledger = []
    add_expense(ledger, Decimal("12.00"), "Food", "Groceries")
    add_expense(ledger, Decimal("25.00"), "Transport", "Taxi")
    add_expense(ledger, Decimal("8.00"), "Food", "Coffee")
    # 2. Act: Query with mixed case and leading/trailing whitespace
    food_results = filter_by_category(ledger, "   food   ")
    # 3. Assert
    assert len(food_results) == 2
    assert all(item["category"] == "Food" for item in food_results)


def test_get_category_counts():
    # 1. Arrange: Empty ledger check
    assert get_category_counts([]) == {}
    # 2. Arrange: Ledger with multiple items
    ledger = []
    add_expense(ledger, Decimal("10.00"), "Food", "Breakfast")
    add_expense(ledger, Decimal("15.00"), "Food", "Lunch")
    add_expense(ledger, Decimal("30.00"), "Transport", "Taxi")
    # 3. Act
    counts = get_category_counts(ledger)
    # 4. Assert
    assert counts["Food"] == 2
    assert counts["Transport"] == 1
    assert "Bills" not in counts


def test_load_ledger_nonexistent_file(tmp_path):
    ghost_file = tmp_path / "missing.txt"
    assert load_ledger_from_file(ghost_file) == []


def test_save_and_load_plain_text_roundtrip(tmp_path):
    test_file = tmp_path / "expenses.txt"
    ledger = []
    add_expense(ledger, Decimal("15.50"), "Food", "Lunch")
    add_expense(ledger, Decimal("40.00"), "Transport", "Taxi")
    save_ledger_to_file(ledger, test_file)
    reloaded = load_ledger_from_file(test_file)
    assert len(reloaded) == 2
    assert reloaded[0]["id"] == 1
    assert reloaded[0]["amount"] == Decimal("15.50")
    assert isinstance(reloaded[0]["amount"], Decimal)
    assert isinstance(reloaded[0]["date"], date)
    assert reloaded[0]["category"] == "Food"
    assert reloaded[0]["description"] == "Lunch"