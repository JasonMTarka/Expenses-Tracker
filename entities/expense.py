import datetime

class Expense:
    """An Expense object to store values from a database record."""

    def __init__(
        self, primary_key, name: str, cost: int, tags: str, date: datetime.datetime
    ) -> None:
        """Set attributes to Expense object."""

        self.key = primary_key
        self.date = date
        self.name = name
        self.cost = cost
        self.tags = tags

    def __repr__(self) -> str:
        """Return string formatted to be same as initialized expense."""

        return (
            "Expense("
            f"{self.key},"
            f"{self.name},"
            f"{self.cost},"
            f"{self.tags},"
            f"{self.date})"
        )

    def __str__(self) -> str:
        """Return readable version of object attributes."""

        return (
            f"ID: {self.key}, "
            f"Name: {self.name}, "
            f"Cost: {self.cost}, "
            f"Tags: {self.tags}, "
            f"Date: {self.date}"
        )
