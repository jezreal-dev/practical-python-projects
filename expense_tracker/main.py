from pathlib import Path
import os
from decimal import Decimal, InvalidOperation
from utils import (add_expense,
    calculate_total_expenditure,
    calculate_category_aggregate,
    filter_by_category,
    delete_expense_by_id,
    validate_amount,
    get_category_counts,
    InvalidExpenditureError,
    ExpenseNotFoundError,
    save_ledger_to_json,
    load_ledger_from_json,
)

DATA_FILE = Path(__file__).parent / "expenses_log.json"
def menu() -> None:
    """Command-line interface"""
    os.system("clear")
    print("\n=================================")
    print("==== TRACK...YOUR...EXPENSE💸====")
    print("=================================")
    print("[1.] Add Expenses")
    print("[2.] View All Expenses")
    print("[3.] Show Total Spending")
    print("[4.] Show Spending by Category")
    print("[5.] Filter Expenses by Category")
    print("[6.] Delete an Expense")
    print("[7.] Exit")

def get_expense(ledger: list):
    try:
        raw_amount = Decimal(input("Enter expense amount (e.g, ₦ 12.50): "))
        validate_amount(raw_amount)
        raw_category = input("Enter expense category: ")
        raw_description = input("Enter expense description: ")
        new_record = add_expense(
            ledger, raw_amount, raw_category, raw_description
        )
        save_ledger_to_json(ledger, DATA_FILE)
        print(f"✅ Success! Added '{new_record['category']}' expense to the ledger.")

    except InvalidOperation:
        print("Error:- Invalid number format. Please enter a valid number.")
        return
    except InvalidExpenditureError as e:
        print(f"Business logic Error: {e}")
        return


def view_expenses(ledger: list):
    if not ledger:
        print("Expenses Record 🧾 Empty.")
        return

    print("\n=== Current Expense Log ===")
    for item in ledger:
        print(
            f"ID: {item.get('id', 'N/A')} | "
            f"Date: {item['date']} | "
            f"Category: {item['category']} | "
            f"Amount: ₦{item['amount']:.2f} | "
            f"Description: {item['description']}"
        )

def display_category_breakdown(ledger: list):
    if not ledger:
        print("🗒 No expenses recorded yet.")
        return

    totals_by_category = calculate_category_aggregate(ledger)
    print("\n=== Category Expenditure Breakdown ===")
    for category, total in totals_by_category.items():
        print(f"Category: {category:<12} | Total: ₦{total:.2f}")

def handle_filter_by_category(ledger: list):
    if not ledger:
        print("🗒 No expenses recorded yet.")
        return

    counts = get_category_counts(ledger)
    if not counts:
        print("No categories found in ledger.")
        return 

    category_list = list(counts.keys())
    print("\n=== Select a Category to Filter ===")
    for index, category in enumerate(category_list, start=1):
        count = counts[category]
        label = "expense" if count == 1 else "expenses"
        print(f"{index} {category} {count} {label}")

    raw_choice = input(f"Select category [1-{len(category_list)}] or type category name: ").strip()
    if raw_choice.isdigit():
        choice_num = int(raw_choice)
        if 1 <= choice_num <= len(category_list):
            target_category = category_list[choice_num
             -1]
        else:
            print("Error: Invalid category selection number.")
            return
    else:
        target_category = raw_choice

    try:
        matches = filter_by_category(ledger, target_category)
        if not matches:
            print(f"🗒 No expenses found under category {target_category}.")
        else:
            print(f"\n=== Filtered Results for {target_category} ===")
            for item in matches:
                print(
                    f"ID: {item['id']} | "
                    f"Date: {item['date']} | "
                    f"Category: {item['category']} | "
                    f"Amount: ₦{item['amount']:.2f} | "
                    f"Description: {item['description']}"
                )
    except InvalidExpenditureError as e:
        print(f"Search Error: {e}")
        return

def handle_delete_expense(ledger: list):
    if not ledger:
        print("🗒 No expenses available to delete.")
        return

    view_expenses(ledger)

    raw_id = input("\nEnter Expense ID to delete (or press Enter to cancel): ".strip())
    if raw_id == "":
        print("Deletion cancelled.")
        return
    try:
        expense_id = int(raw_id)
    except ValueError:
        print("Error: Expense ID must be an Integer.")
        return
    try:
        deleted_record = delete_expense_by_id(ledger, expense_id)
        save_ledger_to_json(ledger, DATA_FILE)
        print(
            f"✅ Successfully deleted Expense | "
            f"ID: {deleted_record['id']} | "
            f"CATEGORY: {deleted_record['category']} | "
            f"AMOUNT: ₦{deleted_record['amount']}."
        )
    except ExpenseNotFoundError as e:
        print(f"Deletion Error: {e}")
        return


def main():
    ledger = load_ledger_from_json(DATA_FILE)

    while True:
        menu()
        choice = input("Select an option between [1]..&..[7]: ").strip()

        if choice == "1":
                get_expense(ledger)
        elif choice == "2":
            view_expenses(ledger)
        elif choice == "3":
            total = calculate_total_expenditure(ledger)
            print(f"\nTOTAL ACCUMULATED EXPENDITURE 📊: ₦{total:.2f}")
        elif choice == "4":
            display_category_breakdown(ledger)
        elif choice == "5":
            handle_filter_by_category(ledger)
        elif choice == "6":
            handle_delete_expense(ledger)
        elif choice == "7":
            print("SEE YOU AGAIN HOPE SOON...GOOD BYE👋.")
            break
        else: 
            print("Invalid Menu choice🙃! Please Select an Option between [1]..&.[7].")
        input("\nPress [Enter] to return to the main menu...")


if __name__ == "__main__":
    main()