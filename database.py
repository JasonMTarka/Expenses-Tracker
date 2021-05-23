import sqlite3
from expense import Expense


class Database:
    def __init__(self, test: bool = False, setup: bool = False) -> None:

        self.test = test
        if test is True:
            self.conn = sqlite3.connect(":memory:")
        else:
            self.conn = sqlite3.connect("expenses.db")

        self.c = self.conn.cursor()

        if setup is True or test is True:
            self.setup()

    def setup(self) -> None:
        with self.conn:
            self.c.execute("""
                    CREATE TABLE expenses (
                    id integer primary key,
                    date text,
                    name text,
                    cost integer,
                    category text
                    )""")

            if self.test is True:
                self.c.execute("""
                    INSERT INTO expenses VALUES
                    (NULL, "21-04-18", "Coca-Cola", 160, "soft drink"),
                    (NULL, "21-04-19", "Amazon Prime", 1500, "subscription"),
                    (NULL, "21-04-19", "Dinner", 3200, "dining"),
                    (NULL, "21-04-18", "Sprite", 160, "soft drink"),
                    (NULL, "21-04-18", "Hotto Motto Bento", 660, "bento"),
                    (NULL, "21-04-18", "New Super", 3000, "groceries"),
                    (NULL, "21-04-18", "Starcraft III", 6000, "games"),
                    (NULL, "21-04-18", "Chinese Super", 1100, "groceries, jason"),
                    (NULL, "21-04-18", "Sapporo", 990, "alcohol"),
                    (NULL, "21-04-18", "Tissues", 240, "household"),
                    (NULL, "21-04-18", "Earbuds", 10000, "accessories"),
                    (NULL, "21-04-18", "Boss Coffee", 160, "coffee, xiaochen"),
                    (NULL, "21-04-18", "Test", 160, "coffee, okinawa"),
                    (NULL, "21-04-18", "Sleeping Pills", 3990, "medicine, okinawa")
                    """)

    def add_expense(self, expense: Expense) -> None:
        with self.conn:
            self.c.execute("INSERT INTO expenses VALUES (NULL, :date, :name, :cost, :tags)", {"date": expense.date, "name": expense.name, "cost": expense.cost, "tags": expense.tags})

    def remove_expense(self, expense: Expense) -> None:
        with self.conn:
            try:
                self.c.execute("DELETE FROM expenses WHERE id=:key", {'key': expense.key})
            except AttributeError:
                self.c.execute("DELETE FROM expenses WHERE id=:key", {'key': expense})

    def update_tag(self, expense: Expense) -> None:
        with self.conn:
            try:
                self.c.execute("UPDATE expenses SET category = :tags WHERE id=:key", {'tags': expense.tags, 'key': expense.key})
            except AttributeError:
                self.c.execute("UPDATE expenses SET category = :tags WHERE id=:key", {'tags': expense.tags, 'key': expense})

    def get_tag(self, tag: str) -> list:
        self.c.execute("SELECT * FROM expenses WHERE category LIKE :tag", {"tag": '%' + tag + '%'})
        return [self.convert_to_object(expense) for expense in self.c.fetchall()]

    def get_all(self) -> list:
        self.c.execute("SELECT * FROM expenses")
        return [self.convert_to_object(expense) for expense in self.c.fetchall()]

    def get_expense(self, expense: Expense) -> Expense:
        try:
            self.c.execute("SELECT * FROM expenses WHERE id = :id", {'id': expense.key})
        except AttributeError:
            self.c.execute("SELECT * FROM expenses WHERE id = :id", {'id': expense})
        return self.convert_to_object(self.c.fetchone())

    def get_distinct_tags(self) -> list:
        self.c.execute("SELECT DISTINCT category FROM expenses")
        temp_list = [expense[0] for expense in self.c.fetchall()]
        result_list = []
        for category in temp_list:
            if "," in category:
                holder = category.split(", ")
                for item in holder:
                    if item in result_list:
                        pass
                    else:
                        result_list.append(item)
            else:
                if category in result_list:
                    pass
                else:
                    result_list.append(category)
        return result_list

    def get_over(self, upper: int) -> list:
        self.c.execute("SELECT * FROM expenses WHERE cost > :upper", {"upper": upper})
        return [self.convert_to_object(expense) for expense in self.c.fetchall()]

    def get_total(self) -> int:
        self.c.execute("SELECT SUM(cost) FROM expenses")
        return self.c.fetchone()[0]

    def order_by_price(self) -> list:
        self.c.execute("SELECT * FROM expenses ORDER BY cost DESC")
        return [self.convert_to_object(expense) for expense in self.c.fetchall()]

    def convert_to_object(self, record: list) -> Expense:
        tags = record[4].split(", ")
        return Expense(record[0], record[1], record[2], record[3], tags)
