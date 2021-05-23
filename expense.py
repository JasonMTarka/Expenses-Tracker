
class Expense:
    def __init__(self, primary_key, date: str, name: str, cost: int, tags: str) -> None:
        self.key = primary_key
        self.date = date
        self.name = name
        self.cost = cost
        self.tags = tags

    def __repr__(self) -> str:
        return f"Expense({self.key}, {self.date}, {self.name}, {self.cost}, {self.tags}"

    def __str__(self) -> str:
        return f"""
ID: {self.key} Date: {self.date}  Name: {self.name}  Cost: {self.cost}  Tags: {", ".join(self.tags)}"""
