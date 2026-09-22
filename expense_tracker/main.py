from decimal import Decimal, InvalidOperation
from utils import (
    add_expense,
    calculate_total_expenditure,
    InvalidExpenditureError,
    InvalidCategoryError,
    InvalidAmountError,
)

def menu() -> None:
    """Command-line interface"""
    print("\n=================================")
    print("==== TRACK...YOUR...EXPENSE💸====")
    print("=================================")
    print("[1.] Add Expenses")
    print("[2.] View All Expenses")
    print("[3.] Show Total Spending")
    print("[4.] Exit")

def get_expense(ledger: list) -> None:
    raw_amount = input("Enter expense amount (e.g, 12.50): ")
    raw_category = input("Enter expense category: ")
    raw_description = input("Enter expense description: ")

    try:
        dec_amount = Decimal(raw_amount)
        new_record = add_expense(
            ledger, dec_amount, raw_category, raw_description
        )
        print(f"✅ Success! Added '{new_record['category']}' expense to the ledger.")

    except InvalidOperation:
        print("Error:- Invalid number format. Please enter a valid number.")
    except InvalidExpenditureError as e:
        print(f"Business logic Error: {e}")


def view_expenses(ledger: list) -> None:
    if not ledger:
        print("No expenses recorded yet.")
        return

    print("\n=== Current Expense Log ===")
    for item in ledger:
        print(
            f"ID: {item.get('id', 'N/A')} | "
            f"Date: {item['date']} | "
            f"Category: {item['category']} | "
            f"Amount: ₦{item['amount']:.2f} | "
            f"Desc: {item['description']}"
        )


def main():
    ledger:list = []

    while True:
        menu()
        choice = input("Select an option [1]..[2]..[3]..[4]: ").strip()

        if choice == "1":
                get_expense(ledger)

        elif choice == "2":
            view_expenses(ledger)
        elif choice == "3":
            total = calculate_total_expenditure(ledger)
            print(f"\nTOTAL ACCUMULATED EXPENDITURE: ₦{total:.2f}")
        elif choice == "4":
            print("SEE YOU AGAIN HOPE SOON...GOOD BYE 👋.")
            break
        else: 
            print("Invalid Menu choice🙃! Please Select an Option between [1]..[2]..[3].&.[4].")


if __name__ == "__main__":
    main()