import sqlite3
from datetime import date

from entities.expense import Expense


class Repository:
    """Database object for reading from and writing to database file."""

    def __init__(self, debug: bool = False, setup: bool = False) -> None:
        """Establish database connection and create cursor."""
        self.debug = debug
        if debug is True:
            self.conn = sqlite3.connect(":memory:")
        else:
            self.conn = sqlite3.connect("expenses.db")

        self.c = self.conn.cursor()

        if setup is True or debug is True:
            self.setup()

        (
            self.lookup_name_from_id,
            self.lookup_id_from_name,
        ) = self._create_lookup_tables()

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
            self.c.execute(
                """
                    CREATE TABLE expense_tags (
                    expense_id integer,
                    tag_id integer
                    )"""
            )
            self.c.execute(
                """
                    CREATE TABLE tags (
                    id integer,
                    name text
                    )"""
            )

            if self.debug is True:
                self.c.execute(
                    """
                    INSERT INTO expenses VALUES
                    (1, "20-03-18", "Coca-Cola", 160, ""),
                    (2, "20-03-19", "Amazon Prime", 1500, ""),
                    (3, "21-03-19", "Dinner", 3200, ""),
                    (4, "21-04-18", "Sprite", 160, ""),
                    (5, "21-04-18", "Hotto Motto Bento", 660, "")
                    """
                )
                self.c.execute(
                    """
                    INSERT INTO expense_tags VALUES
                    (1, 1),
                    (2, 4),
                    (3, 2),
                    (4, 1),
                    (5, 2),
                    (5, 3)
                    """
                )
                self.c.execute(
                    """
                    INSERT INTO tags VALUES
                    (1, "Groceries"),
                    (2, "Dining"),
                    (3, "Social"),
                    (4, "Household"),
                    (5, "Travel")
                    """
                )

    def remove_expense(self, expense: Expense) -> None:
        """Remove an expense from the database."""

        expenses_query = "DELETE FROM expenses WHERE id=:key"
        tags_query = "DELETE FROM expense_tags WHERE expense_id=:key"
        with self.conn:
            try:
                parameters = {"key": expense.key}
                self.c.execute(expenses_query, parameters)
                self.c.execute(tags_query, parameters)
            except AttributeError:
                parameters = {"key": expense}
                self.c.execute(expenses_query, parameters)
                self.c.execute(tags_query, parameters)
            except:
                self.conn.rollback()
                print("DB delete error")

    def order_by_price(self, limit: int = 100) -> list[Expense]:
        """Query database for a list of expenses ordered by cost."""

        query = "SELECT * FROM expenses ORDER BY cost DESC LIMIT :limit"
        self.c.execute(query, {"limit": limit})
        return [self.convert_to_object(expense) for expense in self.c.fetchall()]

    def get_tag(self, tag: str, limit: int = 100) -> list[Expense]:
        """Query database for a list of expenses with given tags."""

        query = (
            "SELECT id, name, cost, tags, date, created_at, updated_at, tags.name FROM expenses "
            "INNER JOIN expense_tags "
            "ON expenses.id = expense_tags.expense_id "
            "INNER JOIN tags "
            "ON expense_tags.tag_id = tags.id "
            "WHERE tags.name = :tag "
            "LIMIT :limit"
        )
        parameters = {"tag": tag, "limit": limit}
        self.c.execute(query, parameters)

        return [self.convert_to_object(expense) for expense in self.c.fetchall()]

    def get_all(self) -> list[Expense]:
        """Query database for a list of all expenses."""

        query = "SELECT * FROM expenses"
        self.c.execute(query)

        return [self.convert_to_object(expense) for expense in self.c.fetchall()]

    def get_limit(self, limit: int = 10) -> list[Expense]:
        """Query for a list of expenses up to 'limit'."""

        query = "SELECT * FROM expenses ORDER BY id DESC LIMIT :limit"
        self.c.execute(query, {"limit": limit})

        return [self.convert_to_object(expense) for expense in self.c.fetchall()]

    def get_month(self, month: str, year: str) -> list[Expense]:
        """Query database for expenses on a given month."""
        query = "SELECT * FROM expenses WHERE date LIKE :month"
        if year == "":
            year = str(date.today())[2:4]
        parameters = {"month": year + "-" + month + "%"}
        self.c.execute(query, parameters)

        return [self.convert_to_object(expense) for expense in self.c.fetchall()]

    def get_expense(self, expense: Expense) -> Expense:
        """Query database for a specific expense."""

        query = "SELECT * FROM expenses WHERE id = :id"
        try:
            self.c.execute(query, {"id": expense.key})

        except AttributeError:
            self.c.execute(query, {"id": expense})

        return self.convert_to_object(self.c.fetchone())

    def _create_lookup_tables(self) -> tuple[dict[str, str], dict[str, str]]:
        """Creates lookup tables for tags."""

        id_from_name = {}
        name_from_id = {}
        query = "SELECT id, name FROM tags"

        with self.conn:
            self.c.execute(query)
            for expense in self.c.fetchall():
                id, name = expense
                id_from_name[name] = id
                name_from_id[id] = name
            return (name_from_id, id_from_name)

    def get_expense_tags(self, expense_id: int) -> list[str]:
        query = "SELECT tag_id FROM expense_tags WHERE expense_id=:key"
        self.c.execute(query, {"key": expense_id})
        tag_ids = [tag[0] for tag in self.c.fetchall()]
        tag_names = []
        for id in tag_ids:
            tag_names.append(self.lookup_name_from_id[id])
        return tag_names

    def get_over(self, upper: int, limit: int = 100) -> list[Expense]:
        """Get all expenses over a specified amount."""

        self.c.execute(
            "SELECT * FROM expenses WHERE cost > :upper LIMIT :limit",
            {"upper": upper, "limit": limit},
        )
        return [self.convert_to_object(expense) for expense in self.c.fetchall()]

    def get_total(self) -> int:
        """Query database for sum total of expenses."""

        self.c.execute("SELECT SUM(cost) FROM expenses")
        return self.c.fetchone()[0]

    def convert_to_object(self, record: list) -> Expense:
        """Converts database record into an Expense object."""
        id, date, name, cost, _ = record
        print(id, name, date, cost)
        tags = self.get_expense_tags(id)
        return Expense(id, name, cost, tags, date)

    # def create_report(self):
    #     self.c.execute(
    #         "SELECT tags, SUM(cost), COUNT(*) FROM expenses WHERE date >= date_sub(CURRENT_TIMESTAMP, INTERVAL 30 DAY) GROUP BY tags"
    #     )
    #     raws = self.c.fetchall()
    #     categories = []
    #     for category in raws:
    #         categories.append(
    #             {
    #                 "category": category[0],
    #                 "cost": round(category[1]),
    #                 "count": category[2],
    #             }
    #         )

    #     self.c.execute(
    #         "SELECT SUM(cost) FROM expenses WHERE date >= date_sub(CURRENT_TIMESTAMP, INTERVAL 30 DAY)"
    #     )
    #     sum: int = round(self.c.fetchone()[0])

    #     return {"categories": categories, "total": sum}

    def add_expense(self, expense: Expense):
        insert_query = (
            "INSERT INTO expenses(name, cost, date) VALUES (:name, :cost, :date)"
        )
        expense_info = {
            "name": expense.name,
            "cost": expense.cost,
            "date": expense.date,
        }
        self.c.execute(insert_query, expense_info)
        expense_id = self.c.lastrowid

        tags = expense.tags.split(", ")
        for tag in tags:
            tag_id = self.lookup_id_from_name[tag]
            self.c.execute(
                "INSERT INTO expense_tags VALUES (:expense_id, :tag_id)",
                {"expense_id": expense_id, "tag_id": tag_id},
            )
        self.conn.commit()
