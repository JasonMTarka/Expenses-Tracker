import sys

from database import Database
from expense import Expense
from typing import Optional


class Application:
    def __init__(self, db: Database):
        self.db = db
        self.menu = {
            'add expense': {'func': self.add_expense, 'description': "Add an expense."},
            'remove expense': {'func': self.remove_expense, 'description': "Remove an expense."},
            'update tags': {'func': self.update_tags, 'description': "Update an expense's tags."},
            'get tag': {'func': self.get_tags, 'description': "Get a list of all expenses in a tag."},
            'get distinct tags': {'func': self.get_distinct_tags, 'description': "Get a list of all current tags."},
            'get over': {'func': self.get_over, 'description': "Get a list of all expenses over a certain amount."},
            'order by price': {'func': self.order_by_price, 'description': "Get a list of all expenses ordered in descending order."},
            'get all': {'func': self.get_all, 'description': "Get a list of all expenses."},
            'get total': {'func': self.get_total, 'description': "Get a total cost."}
        }

    def start(self):
        print()
        print("Welcome to your expenses tracker.")
        if self.db.test is True:
            print("DEBUGGING MODE!")
        print("What would you like to do?")
        self.main_menu()

    def main_menu(self):
        print()
        for key in self.menu.keys():
            print(f"{key} - {self.menu.get(key).get('description')}")
        print()
        print("You can return to this page by entering 'main' at any point.")
        print("You can also quit this program at any point by entering 'quit'.")
        intent = self.input_handler(acceptable_inputs=self.menu.keys())

        self.menu.get(intent).get('func')()

    def quit_program(self):
        self.db.conn.close()
        sys.exit("Closing program...")

    def add_expense(self):
        print("What date was this expense?")
        date_intent = self.input_handler()
        print("What's the name of your expense?")
        name_intent = self.input_handler()
        print("What's the cost of your expense?")
        cost_intent = self.input_handler(integer=True)
        print("What tags does this expense have?")
        tag_intent = self.input_handler()
        expense = Expense(0, date_intent, name_intent, cost_intent, tag_intent)
        self.db.add_expense(expense)
        print("Expense added.")
        self.main_menu()

    def remove_expense(self):
        print("What expense would you like to remove?")
        removal_intent = self.input_handler(integer=True)
        self.db.remove_expense(removal_intent)
        print(f"Expense ID {removal_intent} has been successfully removed.")
        self.main_menu()

    def update_tags(self):
        print("What expense would you like to update? (Enter an ID)")
        id_intent = self.input_handler(integer=True)
        expense = self.db.get_expense(id_intent)
        print("What tags would you like to set for this expense?")
        new_tags = self.input_handler()
        expense.tags = new_tags
        self.db.update_tag(expense)
        self.main_menu()

    def get_tags(self, holder: Optional[list] = None, new_tag: Optional[str] = None):
        if holder is None:
            holder = []
        if new_tag is None:
            print("Which tag would you like to see?")
            new_tag = self.input_handler()
        holder.append(new_tag)
        print("Enter other tags you want to see, or press Enter.")
        other_intent = self.input_handler()
        if other_intent == "":
            total_cost = 0
            for intent in holder:
                for expense in self.db.get_tag(intent):
                    total_cost += expense.cost
                    print(expense)
            print()
            print(f"The total cost is {total_cost} yen.")
            self.main_menu()
        else:
            self.get_tags(holder, new_tag=other_intent)

    def get_distinct_tags(self):
        for expense in self.db.get_distinct_tags():
            print(expense)
        self.main_menu()

    def get_over(self):
        print("Over how much would you like to see?")
        amount_intent = self.input_handler(integer=True)
        for expense in self.db.get_over(amount_intent):
            print(expense)
        self.main_menu()

    def order_by_price(self):
        for expense in self.db.order_by_price():
            print(expense)
        self.main_menu()

    def get_all(self):
        for expense in self.db.get_all():
            print(expense)
        self.main_menu()

    def get_total(self):
        print(f"Total expenses are {self.db.get_total()} yen.")
        self.main_menu()

    def input_handler(self, message="Please enter a valid input.", destination="main menu", **kwargs):
        # Checks user inputs based on parameters and redirects them if their inputs are not valid.
        # Following keyword arguments are accepted:
        # boolean for yes / no inputs
        # integer for integer inputs
        # acceptable_inputs can be a tuple, list, or set of valid inputs
        if kwargs.get('boolean'):
            print("Enter 'yes' or 'no'.")
        intent = input().lower()
        print()

        if intent == 'main' or intent == 'back':
            self.main_menu()
        if intent == 'quit':
            self.quit_program()
        if kwargs.get('integer'):
            try:
                intent = int(intent)
            except ValueError:
                self.redirect(message="Please enter an integer.")
        if kwargs.get('acceptable_inputs'):
            acceptable_inputs = kwargs.get('acceptable_inputs')
            if intent not in acceptable_inputs:
                self.redirect(message=message)
        if kwargs.get('boolean'):
            if intent not in {'yes', 'no'}:
                self.redirect(message="Please enter 'yes' or 'no'.")

        return intent

    def redirect(self, message: str = "Please enter a valid input.") -> None:
        # Sends users back to the specified destination and sends them an appropriate message.
        if message:
            print(message)
        print(f"Returning to main menu.")
        print()
        self.main_menu()


def main() -> None:
    db = Database()
    app = Application(db)
    app.start()


if __name__ == "__main__":
    main()
