import sqlite3


class Database:
    def __init__(self, test=False, setup=False):

        if test is True:
            self.conn = sqlite3.connect(":memory:")
        else:
            self.conn = sqlite3.connect("expenses.db")

        self.c = self.conn.cursor()

        if setup is True or test is True:
            self.setup()

    def setup(self):
        with self.conn:
            self.c.execute("""
                    CREATE TABLE expenses (
                    id integer primary key,
                    date text,
                    name text,
                    cost integer,
                    category text
                    )""")

            # self.c.execute("""
            #     INSERT INTO expenses VALUES
            #     (NULL, "21-04-18", "Coca-Cola", 160, "soft drink"),
            #     (NULL, "21-04-19", "Amazon Prime", 1500, "subscription"),
            #     (NULL, "21-04-19", "Dinner", 3200, "dining"),
            #     (NULL, "21-04-18", "Sprite", 160, "soft drink"),
            #     (NULL, "21-04-18", "Hotto Motto Bento", 660, "bento"),
            #     (NULL, "21-04-18", "New Super", 3000, "groceries"),
            #     (NULL, "21-04-18", "Starcraft III", 6000, "games"),
            #     (NULL, "21-04-18", "Chinese Super", 1100, "groceries"),
            #     (NULL, "21-04-18", "Sapporo", 990, "alcohol"),
            #     (NULL, "21-04-18", "Tissues", 240, "household"),
            #     (NULL, "21-04-18", "Earbuds", 10000, "accessories"),
            #     (NULL, "21-04-18", "Boss Coffee", 160, "coffee"),
            #     (NULL, "21-04-18", "Sleeping Pills", 3990, "medicine")
            #     """)

    def add_expense(self, expense):
        with self.conn:
            self.c.execute("INSERT INTO expenses VALUES (NULL, :date, :name, :cost, :category)", {"date": expense.date, "name": expense.name, "cost": expense.cost, "category": expense.category})

    def remove_expense(self, expense):
        with self.conn:
            try:
                self.c.execute("DELETE FROM expenses WHERE id=:key", {'key': expense.key})
            except AttributeError:
                self.c.execute("DELETE FROM expenses WHERE id=:key", {'key': expense})

    def get_category(self, category):
        self.c.execute("SELECT * FROM expenses WHERE category=:category", {"category": category})
        return [self.convert_to_object(expense) for expense in self.c.fetchall()]

    def get_all(self):
        self.c.execute("SELECT * FROM expenses")
        return [self.convert_to_object(expense) for expense in self.c.fetchall()]

    def get_food(self):
        self.c.execute("SELECT * FROM expenses WHERE category='dining' OR category='groceries' OR category='bento'")
        return [self.convert_to_object(expense) for expense in self.c.fetchall()]

    def get_drinks(self):
        self.c.execute("SELECT * FROM expenses WHERE category='soft drink' OR category='alcohol' OR category='coffee' OR category='tea'")
        return [self.convert_to_object(expense) for expense in self.c.fetchall()]

    def get_over(self, upper):
        self.c.execute("SELECT * FROM expenses WHERE cost > :upper", {"upper": upper})
        return [self.convert_to_object(expense) for expense in self.c.fetchall()]

    def get_category_total(self, category):
        self.c.execute("SELECT SUM(cost) FROM expenses WHERE category=:category", {"category": category})
        return self.c.fetchone()[0]

    def get_total(self):
        self.c.execute("SELECT SUM(cost) FROM expenses")
        return self.c.fetchone()[0]

    def order_by_price(self):
        self.c.execute("SELECT * FROM expenses ORDER BY cost DESC")
        return [self.convert_to_object(expense) for expense in self.c.fetchall()]

    def convert_to_object(self, record):
        return Expense(*record)


class Expense:
    def __init__(self, primary_key, date, name, cost, category):
        self.key = primary_key
        self.date = date
        self.name = name
        self.cost = cost
        self.category = category

    def __repr__(self):
        return f"Expense({self.key}, {self.date}, {self.name}, {self.cost}, {self.category}"

    def __str__(self):
        return f"""
Date: {self.date}  Name: {self.name}  Cost: {self.cost}  Category: {self.category}"""


class Application:
    def __init__(self, db):
        self.db = db

    def start(self):
        print()
        print("Welcome to your expenses tracker.")
        print("What would you like to do?")
        self.main_menu()

    def main_menu(self):
        print()
        print("'add expense' - Add an expense.")
        print("'remove expense' - Remove an expense.")
        print("'get category' - Get a list of all expenses in a category.")
        print("'get category total' - Get a total cost of a category's expenses.")
        print("'get food' - Get a list of all food-related expenses.")
        print("'get drinks' - Get a list of all drink-related expenses.")
        print("'get over' - Get a list of all expenses over a certain amount.")
        print("'order by price' - Get a list of all expenses ordered in descending order.")
        print("'get all' - Get a list of all expenses.")
        print("'get total' - Get a total cost.")
        print("'quit' - Quit program.")
        intent = input()

        if intent == "quit":
            self.quit_program()

        elif intent == "add expense":
            self.add_expense()

        elif intent == "remove expense":
            print("What expense would you like to remove?")
            removal_intent = input()
            self.remove_expense(removal_intent)

        elif intent == "get category":
            print("Which category would you like to see?")
            category_intent = input()
            for expense in self.db.get_category(category_intent):
                print(expense)
            self.main_menu()

        elif intent == "get category total":
            print("Which category would you like to see?")
            category_intent = input()
            print(self.db.get_category_total(category_intent))
            self.main_menu()

        elif intent == "get food":
            for expense in self.db.get_food():
                print(expense)
            self.main_menu()

        elif intent == "get drinks":
            for expense in self.db.get_drinks():
                print(expense)
            self.main_menu()

        elif intent == "get over":
            print("Over how much would you like to see?")
            amount_intent = input()
            for expense in self.db.get_over(amount_intent):
                print(expense)
            self.main_menu()

        elif intent == "order by price":
            for expense in self.db.order_by_price():
                print(expense)
            self.main_menu()

        elif intent == "get all":
            for expense in self.db.get_all():
                print(expense)
            self.main_menu()

        elif intent == "get total":
            print(self.db.get_total())
            self.main_menu()

    def quit_program(self):
        self.db.conn.close()
        quit()

    def add_expense(self):
        print("What date was this expense?")
        date_intent = input()
        print("What's the name of your expense?")
        name_intent = input()
        print("What's the cost of your expense?")
        cost_intent = input()
        print("What category does this expense belong in?")
        category_intent = input()
        expense = Expense(1, date_intent, name_intent, cost_intent, category_intent)
        self.db.add_expense(expense)
        print("Expense added.")
        self.main_menu()


def main():
    db = Database()
    app = Application(db)
    app.start()


if __name__ == "__main__":
    main()
