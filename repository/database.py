import sqlite3
from datetime import date

from entities.expense import Expense


class Database:
    """Database object for reading from and writing to database file."""

    def __init__(self, debug: bool = False, setup: bool = False) -> None:
        """Establish database connection and create cursor."""

        self.debug = debug
        if debug is True:
            self.conn = sqlite3.connect(":memory:")
        else:
            self.conn = sqlite3.connect("repository/expenses.db")

        self.c = self.conn.cursor()

        if setup is True or debug is True:
            self.setup()

    def setup(self) -> None:
        """Handle first-time setup or debugging mode setup."""

        with self.conn:
            self.c.execute(
                """
                    CREATE TABLE expenses (
                    id integer primary key,
                    date text,
                    name text,
                    cost integer,
                    category text
                    )"""
            )

            if self.debug is True:
                self.c.execute(
                    """
                    INSERT INTO expenses VALUES
                    (NULL, "20-03-18", "Coca-Cola", 160, "soft drink"),
                    (NULL, "20-03-19", "Amazon Prime", 1500, "subscription"),
                    (NULL, "21-03-19", "Dinner", 3200, "dining"),
                    (NULL, "21-04-18", "Sprite", 160, "soft drink"),
                    (NULL, "21-04-18", "Hotto Motto Bento", 660, "bento"),
                    (NULL, "21-04-18", "New Super", 3000, "groceries"),
                    (NULL, "21-05-18", "Starcraft III", 6000, "games"),
                    (NULL, "21-05-18", "Chinese Super", 1100,
                        "groceries, user1"),
                    (NULL, "21-05-18", "Sapporo", 990, "alcohol"),
                    (NULL, "21-04-18", "Tissues", 240, "household"),
                    (NULL, "21-04-18", "Earbuds", 10000, "accessories"),
                    (NULL, "21-04-18", "Boss Coffee", 160, "coffee, user2"),
                    (NULL, "21-04-18", "Test", 160, "coffee, okinawa"),
                    (NULL, "21-04-18", "Sleeping Pills", 3990,
                        "medicine, okinawa")
                    """
                )

    def add_expense(self, expense: Expense) -> None:
        """Add an expense to the database."""

        with self.conn:
            self.c.execute(
                """
                INSERT INTO expenses VALUES (
                NULL,
                :date,
                :name,
                :cost,
                :tags
                )
                """,
                {
                    "date": expense.date,
                    "name": expense.name,
                    "cost": expense.cost,
                    "tags": expense.tags,
                },
            )

    def remove_expense(self, expense: Expense) -> None:
        """Remove an expense from the database."""

        with self.conn:
            try:
                self.c.execute(
                    "DELETE FROM expenses WHERE id=:key", {"key": expense.key}
                )
            except AttributeError:
                self.c.execute(
                    "DELETE FROM expenses WHERE id=:key", {"key": expense}
                )

    def update_tag(self, expense: Expense) -> None:
        """Update tag of a given expense."""

        with self.conn:
            try:
                self.c.execute(
                    "UPDATE expenses SET category = :tags WHERE id=:key",
                    {"tags": expense.tags, "key": expense.key},
                )
            except AttributeError:
                self.c.execute(
                    "UPDATE expenses SET category = :tags WHERE id=:key",
                    {"tags": expense.tags, "key": expense},
                )

    def order_by_price(self) -> list[Expense]:
        """Query database for a list of expenses ordered by cost."""

        self.c.execute("SELECT * FROM expenses ORDER BY cost DESC")

        return [
            self.convert_to_object(expense) for expense in self.c.fetchall()
        ]

    def get_tag(self, tag: str) -> list[Expense]:
        """Query database for a list of expenses with given tags."""

        self.c.execute(
            "SELECT * FROM expenses WHERE category LIKE :tag",
            {"tag": "%" + tag + "%"},
        )

        return [
            self.convert_to_object(expense) for expense in self.c.fetchall()
        ]

    def get_all(self) -> list[Expense]:
        """Query database for a list of all expenses."""

        self.c.execute("SELECT * FROM expenses")

        return [
            self.convert_to_object(expense) for expense in self.c.fetchall()
        ]

    def get_limit(self, limit: int = 10) -> list[Expense]:
        """Query for a list of expenses up to 'limit'."""

        self.c.execute(
            "SELECT * FROM expenses ORDER BY id DESC LIMIT :limit",
            {"limit": limit},
        )

        return [
            self.convert_to_object(expense) for expense in self.c.fetchall()
        ]

    def get_month(self, month: str, year: str) -> list[Expense]:
        """Query database for expenses on a given month."""

        if year == "":
            year = str(date.today())[2:4]
        search_params = year + "-" + month + "%"
        self.c.execute(
            "SELECT * FROM expenses WHERE date LIKE :month",
            {"month": search_params},
        )

        return [
            self.convert_to_object(expense) for expense in self.c.fetchall()
        ]

    def get_expense(self, expense: Expense) -> Expense:
        """Query database for a specific expense."""

        try:
            self.c.execute(
                "SELECT * FROM expenses WHERE id = :id", {"id": expense.key}
            )

        except AttributeError:
            self.c.execute(
                "SELECT * FROM expenses WHERE id = :id", {"id": expense}
            )

        return self.convert_to_object(self.c.fetchone())

    def get_distinct_tags(self) -> list[str]:
        """Display all unique tags in table."""

        self.c.execute("SELECT DISTINCT category FROM expenses")

        temp_list = [expense[0] for expense in self.c.fetchall()]
        result_list = []
        for category in temp_list:
            if "," in category:
                holder = category.split(", ")
                for item in holder:
                    if item in result_list:
                        continue
                    else:
                        result_list.append(item)
            else:
                if category in result_list:
                    continue
                else:
                    result_list.append(category)

        return result_list

    def get_over(self, upper: int) -> list[Expense]:
        """Get all expenses over a specified amount."""

        self.c.execute(
            "SELECT * FROM expenses WHERE cost > :upper", {"upper": upper}
        )
        return [
            self.convert_to_object(expense) for expense in self.c.fetchall()
        ]

    def get_total(self) -> int:
        """Query database for sum total of expenses."""

        self.c.execute("SELECT SUM(cost) FROM expenses")
        return self.c.fetchone()[0]

    def convert_to_object(self, record: list) -> Expense:
        """Converts database record into an Expense object."""

        tags = record[4].split(", ")
        return Expense(record[0], record[1], record[2], record[3], tags)
