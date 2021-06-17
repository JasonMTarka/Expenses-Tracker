
class Expense:
    """An Expense object created to store values from a record taken from the database."""

    def __init__(self, primary_key, date: str, name: str, cost: int, tags: str) -> None:
        """Set attributes to Expense object."""

        self.key = primary_key
        self.date = date
        self.name = name
        self.cost = cost
        self.tags = tags

    def __repr__(self) -> str:
        """Return string formatted to be same as initialized expense."""

        return f"Expense({self.key}, {self.date}, {self.name}, {self.cost}, {self.tags})"

    def __str__(self) -> str:
        """Return readable version of object attributes."""

        return f"""ID: {self.key} Date: {self.date}  Name: {self.name}  Cost: {self.cost}  Tags: {", ".join(self.tags)}"""
