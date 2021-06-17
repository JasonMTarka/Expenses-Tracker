import sys
from datetime import date
from typing import Optional, Any, Union

from database import Database
from expense import Expense


class Application:

    def __init__(self, db: Database) -> None:
        """Initializes database and menu options."""

        self.db = db
        self.menu = {
            'add expense': {'func': self.add_expense, 'description': "Add an expense."},
            'remove expense': {'func': self.remove_expense, 'description': "Remove an expense."},
            'update tags': {'func': self.update_tags, 'description': "Update an expense's tags."},
            'order by price': {'func': self.order_by_price, 'description': "Get a list of all expenses ordered in descending order."},
            'get tag': {'func': self.print_tags, 'description': "Get a list of all expenses in a tag."},
            'get distinct tags': {'func': self.print_distinct_tags, 'description': "Get a list of all current tags."},
            'get over': {'func': self.print_over, 'description': "Get a list of all expenses over a certain amount."},
            'get all': {'func': self.print_all, 'description': "Get a list of all expenses."},
            'get month': {'func': self.print_month, 'description': "Get a month's expenses."},
            'get total': {'func': self.print_total, 'description': "Get a total cost."},
            'get ten': {'func': self.print_ten, 'description': "Get the ten most recent entries."}
        }

    def start(self) -> None:
        """Display messages once on program initialization."""

        if self.db.debug is True:
            print("DEBUGGING MODE!")
        print("\nWelcome to your expenses tracker.")
        print("What would you like to do?")
        self.main_menu()

    def main_menu(self):
        """Display main menu options."""

        print()
        for key in self.menu.keys():
            print(f"{key} - {self.menu.get(key).get('description')}")
        print("\nYou can return to this page by entering 'main' at any point.")
        print("You can also quit this program at any point by entering 'quit'.")
        acceptable_inputs = set(self.menu.keys())
        intent = self.input_handler(acceptable_inputs=acceptable_inputs)

        self.menu.get(intent).get('func')()

    def quit_program(self) -> None:
        """Close database connection and exit program."""

        self.db.conn.close()
        sys.exit("Closing program...")

    def add_expense(self) -> None:
        """Create an updated Expense object and send it to the database to be added."""

        date_intent = self.input_handler(prompt="What date was this expense? Enter like '21-04-31'.  If today, press Enter.")
        if date_intent == "":
            date_intent = str(date.today())[2:]
        name_intent = self.input_handler(prompt="What's the name of your expense?", allow_uppercase=True)
        cost_intent = self.input_handler(prompt="What's the cost of your expense?", integer=True)
        tag_intent = self.input_handler(prompt="What tags does this expense have?")
        expense = Expense(0, date_intent, name_intent, cost_intent, tag_intent)  # id argument will be handled later by database, so 0 is placeholder
        self.db.add_expense(expense)
        print("Expense added.")
        self.main_menu()

    def remove_expense(self) -> None:
        """Remove an expense from the database."""

        removal_intent = self.input_handler(prompt="What expense would you like to remove?", integer=True)
        self.db.remove_expense(removal_intent)
        print(f"Expense ID {removal_intent} has been successfully removed.")
        self.main_menu()

    def update_tags(self) -> None:
        """Update tags on an existing expense."""

        id_intent = self.input_handler(prompt="What expense would you like to update? (Enter an ID)", integer=True)
        expense = self.db.get_expense(id_intent)
        new_tags = self.input_handler(prompt="What tags would you like to set for this expense?")
        expense.tags = new_tags
        self.db.update_tag(expense)
        self.main_menu()

    def order_by_price(self) -> None:
        """Display expenses ordered by price."""

        for expense in self.db.order_by_price():
            print(expense)
        self.main_menu()

    def print_month(self) -> None:
        """Display expenses for a month determined by user input."""

        month = self.input_handler(prompt="What month would you like to see?\nEnter like '04' for April.")
        year = self.input_handler(prompt=f"Press Enter for {str(date.today())[:4]}, or for a different year, enter like '19' for 2019.")
        total_cost = 0
        for expense in self.db.get_month(month, year):
            print(expense)
            total_cost += expense.cost
        if total_cost:
            print(f"\nThe total cost is {total_cost} yen.")
        else:
            print(f"There are no expenses for {year}-{month}.")
        self.main_menu()

    def print_tags(self, tag_holder: Optional[list] = None, new_tag: Optional[str] = None) -> None:
        """Print all expenses with tags specified by the user."""

        if tag_holder is None:
            tag_holder = []
        if new_tag is None:
            for tag in self.db.get_distinct_tags():
                print(tag)
            new_tag = self.input_handler(prompt="\nWhich tag would you like to see?")
        tag_holder.append(new_tag)
        intent = self.input_handler(prompt="Enter other tags you want to see, or press Enter.")
        if intent == "":
            total_cost = 0
            for tag in tag_holder:
                for expense in self.db.get_tag(tag):
                    total_cost += expense.cost
                    print(expense)
            print(f"\nThe total cost is {total_cost} yen.")
            self.main_menu()
        else:
            self.print_tags(tag_holder, new_tag=intent)

    def print_distinct_tags(self) -> None:
        """Print all unique tags in the database."""

        for expense in self.db.get_distinct_tags():
            print(expense)
        self.main_menu()

    def print_over(self) -> None:
        """Print all expenses over an amount specified by the user."""

        amount_intent = self.input_handler(prompt="Over how much would you like to see?", integer=True)
        for expense in self.db.get_over(amount_intent):
            print(expense)
        self.main_menu()

    def print_all(self) -> None:
        """Print all expenses."""

        for expense in self.db.get_all():
            print(expense)
        self.main_menu()

    def print_ten(self) -> None:
        """Print the 10 most recent expenses."""

        for expense in self.db.get_limit()[::-1]:
            print(expense)
        self.main_menu()

    def print_total(self) -> None:
        """Print total cost of all expenses."""

        print(f"Total expenses are {self.db.get_total()} yen.")
        self.main_menu()

    def input_handler(self, prompt: str = "", error_msg: str = "Please enter a valid input.",
                      destination: str = "main menu", **kwargs) -> Any:
        '''Checks user inputs based on parameters and redirects them if their inputs are not valid.
        Following keyword arguments are supported:
        'allow_uppercase = True' for allowing capital letters
        boolean for yes / no inputs
        integer for integer inputs
        acceptable_inputs can be a tuple, list, or set (preferred b/c hashing) of valid inputs
        '''

        if prompt:
            print(prompt)

        if kwargs.get('boolean'):
            print("Enter 'yes' or 'no'.")

        if kwargs.get("allow_uppercase"):
            intent: Union[int, str] = input()
        else:
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
            acceptable_inputs = kwargs.get('acceptable_inputs', set())
            if intent not in acceptable_inputs:
                self.redirect(message=error_msg)

        if kwargs.get('boolean'):
            if intent not in ('yes', 'no'):
                self.redirect(message="Please enter 'yes' or 'no'.")

        return intent

    def redirect(self, message: str = "Please enter a valid input.") -> None:
        # Sends users back to the specified destination and sends them an appropriate message.
        if message:
            print(message)
        print(f"Returning to main menu.\n")
        self.main_menu()


def main() -> None:

    def cmd_line_arg_handler() -> dict:

        opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]

        cmd_line_args = {"debug": False}

        if opts:

            if "-h" in opts or "--help" in opts:
                print("Expenses Tracker by Jason Tarka")
                print("Accepted command line arguments:")
                print('"-v" or "--version": Display version information')
                print('"-d" or "--debug": Enter debugging mode')
                sys.exit()

            if "-v" in opts or "--version" in opts:
                print("Application version: 1.1.0")
                print(f"Python version: {sys.version}")
                sys.exit()

            if "-d" in opts or "--debug" in opts:
                cmd_line_args["debug"] = True

        return cmd_line_args

    debug = cmd_line_arg_handler().get("debug", False)

    db = Database(debug=debug)
    app = Application(db)
    app.start()


if __name__ == "__main__":
    main()
