from expense import Expense
import sys

def main():
    print(" Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    
    if len(sys.argv) < 2:
        expense = get_user_expense()
        save_expense_to_file(expense, expense_file_path)
        summarize_expenses(expense_file_path)
        return

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
        expense = Expense(name=expense_name, amount=expense_amount, category=expense_category)
        print(f"Using command line arguments: {expense_name}, {expense_amount}, {expense_category}")
        save_expense_to_file(expense, expense_file_path)
        summarize_expenses(expense_file_path)
    
    elif command == "list":
        category = sys.argv[2] if len(sys.argv) >= 3 else None
        list_expenses(expense_file_path, category)
    
    elif command == "total":
        show_total(expense_file_path)
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: add, total, list")
        sys.exit(1)
