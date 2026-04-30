from expense import Expense
import sys
import csv
def main():
    print(" Running Expense Tracker!")
    expense_file_path = "expenses.csv"

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) != 5:
            print("Usage: python expenses.py add <amount> <category> <name>")
            sys.exit(1)
        try:
            expense_amount = float(sys.argv[2])
        except ValueError:
            print("Error: amount must be a number")
            sys.exit(1)
        expense_category = sys.argv[3]
        expense_name = sys.argv[4]

        existing_categories = set()
        try:
            with open(expense_file_path, "r") as f:
                reader = csv.reader(f)
                for line in reader:
                    if len(line) >= 3:
                        existing_categories.add(line[2])
        except FileNotFoundError:
            print("Error: expenses file not found. No categories exist yet.")
            sys.exit(1)
        if expense_category not in existing_categories:
            print(f"Error: category '{expense_category}' does not exist.")
            print(f"Available categories: {', '.join(existing_categories) if existing_categories else 'none'}")
            sys.exit(1)

        expense = Expense(name=expense_name, amount=expense_amount, category=expense_category)
        print(f"Using command line arguments: {expense_name}, {expense_amount}, {expense_category}")
        save_expense_to_file(expense, expense_file_path)
        summarize_expenses(expense_file_path)
    
    elif command == "list":
        category = sys.argv[2] if len(sys.argv) >= 3 else None
        list_expenses(expense_file_path, category)
    
    elif command == "total":
        show_total(expense_file_path)

    elif command =="add-category":
        new_category(expense_file_path)

    else:
        print(f"Unknown command: {command}")
        print("Available commands: add,add-category, total, list")
        sys.exit(1)

def new_category(expense_file_path):
    expense_category = sys.argv[2]
    print(f"Enter expense category: {expense_category} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f" {expense_category}\n")

def save_expense_to_file(expense: Expense, expense_file_path):
    print(f" Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")

def load_expenses(expense_file_path):
    expenses = []
    with open(expense_file_path, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) >= 3:  # пропускаем неполные строки
                expense_name, expense_amount, expense_category = parts
                expenses.append(Expense(name=expense_name, amount=float(expense_amount), category=expense_category))
    return expenses

def summarize_expenses(expense_file_path):
    print(" Summarizing User Expense")
    expenses = load_expenses(expense_file_path)
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        amount_by_category[key] = amount_by_category.get(key, 0) + expense.amount
    print("Expenses By Category :")
    for key, amount in amount_by_category.items():
        print(f"  {key}: {amount:.2f}")
    total_spent = sum(x.amount for x in expenses)
    print(f" Total Spent: {total_spent:.2f}")

def list_expenses(expense_file_path, category=None):
    expenses = load_expenses(expense_file_path)
    if category:
        expenses = [e for e in expenses if e.category.lower() == category.lower()]
        if not expenses:
            print(f"No expenses found in category '{category}'.")
            return
    print("\nAll Expenses:")
    for exp in expenses:
        print(f"  {exp.name}: {exp.amount:.2f} ({exp.category})")
    total = sum(e.amount for e in expenses)
    print(f"\nTotal Spent: {total:.2f}")

def show_total(expense_file_path):
    total = sum(e.amount for e in load_expenses(expense_file_path))
    print(f"Total Spent: {total:.2f}")

if __name__ == "__main__":
     main()
