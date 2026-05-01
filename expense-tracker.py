from expense import Expense
import sys
import csv


def main():
    print("Учет расходов запущен")
    expense_file_path = "expenses.csv"
    open(expense_file_path, "a").close()

    if len(sys.argv) < 2:
        print("Введи: python expenses.py <add,add-category,list,total>")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) != 5:
            print("Введи: python expenses.py add <стоимость> <категория> <название>")
            sys.exit(1)
        try:
            expense_amount = float(sys.argv[2])
        except ValueError:
            print("Ошибка: Стоимость должна быть числом")
            sys.exit(1)
        expense_category = sys.argv[3]
        expense_name = sys.argv[4]

        existing_categories = get_existing_categories(expense_file_path)
        if existing_categories is None:
            print("Ошибка: файл расходов не найден. Категории пока не созданы.")
            sys.exit(1)
        if expense_category not in existing_categories:
            print(f"Ошибка: категории '{expense_category}' не существует.")
            print(f"Доступные категории: {', '.join(existing_categories) if existing_categories else 'none'}")
            sys.exit(1)
        expense = Expense(name=expense_name, amount=expense_amount, category=expense_category)
        saved = save_expense_to_file(expense, expense_file_path)
        print(f"Сохранено: {saved.name}, {saved.amount}, {saved.category} to {expense_file_path}")

        amount_by_category, total_spent = summarize_expenses(expense_file_path)
        print("Расходы по категориям:")
        for key, amount in amount_by_category.items():
            print(f"  {key}: {amount:.2f}")
        print(f"Общая сумма: {total_spent:.2f}")

    elif command == "list":
        category = sys.argv[2] if len(sys.argv) >= 3 else None
        expenses = list_expenses(expense_file_path, category)
        if not expenses:
            print(f"В категории Расходы ничего не найдено '{category}'." if category else "Расходы не обнаружены.")
        else:
            print("\nВсе расходы:")
            for exp in expenses:
                print(f"  {exp.name}: {exp.amount:.2f} ({exp.category})")
            print(f"\nОбщая сумма: {sum(e.amount for e in expenses):.2f}")

    elif command == "total":
        total = show_total(expense_file_path)
        print(f"Общая сумма: {total:.2f}")

    elif command == "add-category":
        existing_categories = get_existing_categories(expense_file_path)
        category = new_category(expense_file_path)
        if category in existing_categories:
            print(f"Ошибка: категория '{category}' уже существует.")
            sys.exit(1)

        if category:
            print(f"Категория '{category}' добавлена в {expense_file_path}")
        else:
            print("Ошибка: не указано название категории.")

    else:
        print(f"Неизвестная команда: {command}")
        print("Доступные команды: add, add-category, total, list")
        sys.exit(1)



def get_existing_categories(expense_file_path):
    existing_categories = set()
    try:
        with open(expense_file_path, "r") as f:
            reader = csv.reader(f)
            for line in reader:
                if len(line) >= 3:
                    existing_categories.add(line[2].strip())
                elif len(line) == 1:
                    existing_categories.add(line[0].strip())
    except FileNotFoundError:
        return None
    return existing_categories


def new_category(expense_file_path):
    expense_category = sys.argv[2] if len(sys.argv) >= 3 else None
    if not expense_category:
        return None
    with open(expense_file_path, "a") as f:
        f.write(f"{expense_category}\n")
    return expense_category


def save_expense_to_file(expense: Expense, expense_file_path):
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")
    return expense


def load_expenses(expense_file_path):
    expenses = []
    with open(expense_file_path, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) >= 3:
                expense_name, expense_amount, expense_category = parts
                expenses.append(Expense(name=expense_name, amount=float(expense_amount), category=expense_category))
    return expenses


def summarize_expenses(expense_file_path):
    expenses = load_expenses(expense_file_path)
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        amount_by_category[key] = amount_by_category.get(key, 0) + expense.amount
    total_spent = sum(x.amount for x in expenses)
    return amount_by_category, total_spent


def list_expenses(expense_file_path, category=None):
    expenses = load_expenses(expense_file_path)
    if category:
        expenses = [e for e in expenses if e.category.lower() == category.lower()]
        if not expenses:
            return []
    return expenses


def show_total(expense_file_path):
    total = sum(e.amount for e in load_expenses(expense_file_path))
    return total


if __name__ == "__main__":
    main()
