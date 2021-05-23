
class Expense:
    def __init__(self, primary_key, date: str, name: str, cost: int, tags: str):
        self.key = primary_key
        self.date = date
        self.name = name
        self.cost = cost
        self.tags = tags

    def __repr__(self):
        return f"Expense({self.key}, {self.date}, {self.name}, {self.cost}, {self.tags}"

    def __str__(self):
        return f"""
ID: {self.key} Date: {self.date}  Name: {self.name}  Cost: {self.cost}  Tags: {", ".join(self.tags)}"""
