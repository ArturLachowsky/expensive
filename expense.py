class Expense:
    def __init__(self, name: str, amount: float, category: str):
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self):
        return f"Expense: {self.name}, {self.category}, {self.amount:.2f}"
