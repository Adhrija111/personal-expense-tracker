
import csv
import os

FILE_NAME = "expenses.csv"

CATEGORIES = [
    "Food",
    "Transport",
    "Education",
    "Shopping",
    "Other"
]

HEADERS = ["User", "Expense", "Amount", "Category"]


def load_expenses():
    expenses = []

    if not os.path.exists(FILE_NAME):
        return expenses

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                row["Amount"] = float(row["Amount"])

                if row["Amount"] >= 0:
                    expenses.append(row)

            except (ValueError, KeyError, TypeError):
                print("Warning: Skipped an invalid saved record.")

    return expenses


def save_expenses(expenses):
    # Rewrite the file with the records we want to keep.
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()

        for expense in expenses:
            writer.writerow({
                "User": expense["User"],
                "Expense": expense["Expense"],
                "Amount": expense["Amount"],
                "Category": expense["Category"]
            })


def get_non_empty_text(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty. Try again.")


def get_amount():
    while True:
        try:
            amount = float(input("How much did you spend (₹)? "))

            if amount <= 0:
                print("Enter an amount greater than zero.")
                continue

            return amount

        except ValueError:
            print("Enter a valid number, like 80 or 30.50.")


def get_category():
    print("\nChoose a category:")

    for number, category in enumerate(CATEGORIES, start=1):
        print(f"{number}. {category}")

    while True:
        try:
            choice = int(input("Enter category number (1-5): "))

            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]

            print("Choose a number from 1 to 5.")

        except ValueError:
            print("Enter a whole number from 1 to 5.")


def add_expense():
    name = get_non_empty_text("Enter your name: ")
    expense_name = get_non_empty_text(
        "What did you spend money on? "
    )
    amount = get_amount()
    category = get_category()

    expenses = load_expenses()

    expenses.append({
        "User": name,
        "Expense": expense_name,
        "Amount": amount,
        "Category": category
    })

    save_expenses(expenses)
    print("\nExpense saved successfully!")


def view_history():
    expenses = load_expenses()

    if not expenses:
        print("\nNo saved expenses yet.")
        return

    print("\n========== SAVED EXPENSE HISTORY ==========")

    total = 0

    for number, expense in enumerate(expenses, start=1):
        print(
            f"{number}. {expense['User']} | "
            f"{expense['Expense']} | "
            f"{expense['Category']} | "
            f"₹{expense['Amount']:.2f}"
        )
        total += expense["Amount"]

    print("-------------------------------------------")
    print(f"Total recorded spending: ₹{total:.2f}")

    print("\n--- Category-wise Spending ---")

    for category in CATEGORIES:
        category_total = sum(
            expense["Amount"]
            for expense in expenses
            if expense["Category"] == category
        )

        if category_total > 0:
            print(f"{category}: ₹{category_total:.2f}")


def delete_expense():
    expenses = load_expenses()

    if not expenses:
        print("\nThere are no expenses to delete.")
        return

    print("\n========== SELECT AN EXPENSE TO DELETE ==========")

    for number, expense in enumerate(expenses, start=1):
        print(
            f"{number}. {expense['User']} | "
            f"{expense['Expense']} | "
            f"{expense['Category']} | "
            f"₹{expense['Amount']:.2f}"
        )

    try:
        choice = int(input("\nEnter the record number to delete: "))

        if not 1 <= choice <= len(expenses):
            print("Invalid record number. Nothing was deleted.")
            return

    except ValueError:
        print("Please enter a valid whole number. Nothing was deleted.")
        return

    selected = expenses[choice - 1]

    print(
        f"\nSelected: {selected['Expense']} | "
        f"₹{selected['Amount']:.2f}"
    )

    confirm = input("Delete this record? (yes/no): ").strip().lower()

    if confirm == "yes":
        expenses.pop(choice - 1)
        save_expenses(expenses)
        print("Expense deleted successfully!")
    else:
        print("Deletion cancelled. Your records are unchanged.")


def main():
    print("================================")
    print("     PERSONAL EXPENSE TRACKER")
    print("================================")

    while True:
        print("\n1. Add an expense")
        print("2. View saved expense history")
        print("3. Delete an expense")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_history()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            print("Thank you for using the Expense Tracker!")
            break
        else:
            print("Invalid option. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
