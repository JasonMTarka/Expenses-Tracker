import sys
from enum import Enum
from datetime import date
from typing import Optional, Any, Union

from database import Database
from expense import Expense


class Labels(Enum):
    FUNC = "function"
    DESC = "description"


class Application:
    """Class that gets data from database and prints it to the user."""

    def __init__(self, db: Database) -> None:
        """Initializes database and menu options."""

        self.db = db
        self.menu = {
            'add expense':
                {Labels.FUNC:
                    self.add_expense,
                 Labels.DESC:
                    "Add an expense."},
            'remove expense':
                {Labels.FUNC:
                    self.remove_expense,
                 Labels.DESC:
                    "Remove an expense."},
            'update tags':
                {Labels.FUNC:
                    self.update_tags,
                 Labels.DESC:
                    "Update an expense's tags."},
            'order by price':
                {Labels.FUNC:
                    self.order_by_price,
                 Labels.DESC:
                    "Get a list of all expenses "
                    "ordered in descending order."},
            'get tag':
                {Labels.FUNC:
                    self.print_tags,
                 Labels.DESC:
                    "Get a list of all expenses in a tag."},
            'get distinct tags':
                {Labels.FUNC:
                    self.print_distinct_tags,
                 Labels.DESC:
                    "Get a list of all current tags."},
            'get over':
                {Labels.FUNC:
                    self.print_over,
                 Labels.DESC:
                    "Get a list of all expenses over a certain amount."},
            'get all':
                {Labels.FUNC:
                    self.print_all,
                 Labels.DESC:
                    "Get a list of all expenses."},
            'get month':
                {Labels.FUNC:
                    self.print_month,
                 Labels.DESC:
                    "Get a month's expenses."},
            'get total':
                {Labels.FUNC:
                    self.print_total,
                 Labels.DESC:
                    "Get a total cost."}
        }

    def start(self) -> None:
        """Display messages once on program initialization."""

        if self.db.debug is True:
            print("DEBUGGING MODE!")
        print(
            "\nWelcome to your expenses tracker.\n"
            "What would you like to do?")
        self.main_menu()

    def main_menu(self):
        """Display main menu options."""
        self.print_ten()
        print()
        for key in self.menu.keys():
            print(f"{key} - {self.menu.get(key).get(Labels.DESC)}")
        print(
            "\nYou can return to this page by entering 'main' at any point.\n"
            "You can also quit this program at any point by entering 'quit'.")

        acceptable_inputs = set(self.menu.keys())

        intent = self.input_handler(
            acceptable_inputs=acceptable_inputs)

        self.menu.get(intent).get(Labels.FUNC)()

    def quit_program(self) -> None:
        """Close database connection and exit program."""

        self.db.conn.close()
        sys.exit("Closing program...")

    def add_expense(self) -> None:
        """Create an updated Expense object and add it to the database."""

        TAX = 1.1
        alcohol_expense = None

        date_intent = self.input_handler(
            prompt="What date was this expense? Enter like '21-04-31'.\n"
            "If today, press Enter.")

        if date_intent == "":
            date_intent = str(date.today())[2:]

        name_intent = self.input_handler(
            prompt="What's the name of your expense?",
            allow_uppercase=True)
        cost_intent = self.input_handler(
            prompt="What's the cost of your expense?",
            integer=True)
        tag_intent = self.input_handler(
            prompt="What tags does this expense have?")

        if "groceries" in tag_intent:
            alcohol_check = self.input_handler(
                prompt="Did you buy any alcohol?",
                boolean=True)

            if alcohol_check == "yes":
                alcohol_cost = self.input_handler(
                    prompt="How much did you spend on alcohol?",
                    integer=True)

                taxed_alcohol = alcohol_cost * TAX

                cost_intent -= taxed_alcohol
                alcohol_expense = Expense(0,
                                          date_intent,
                                          name_intent,
                                          taxed_alcohol,
                                          "alcohol")
            else:
                pass

        expense = Expense(0,
                          date_intent,
                          name_intent,
                          cost_intent,
                          tag_intent)
        # Id argument will be handled later by database, so 0 is placeholder
        if alcohol_expense:
            self.db.add_expense(alcohol_expense)
        self.db.add_expense(expense)
        print("Expense added.")
        self.main_menu()

    def remove_expense(self) -> None:
        """Remove an expense from the database."""

        removal_intent = self.input_handler(
            prompt="What expense would you like to remove?",
            integer=True)

        self.db.remove_expense(removal_intent)
        print(f"Expense ID {removal_intent} has been successfully removed.")
        self.main_menu()

    def update_tags(self) -> None:
        """Update tags on an existing expense."""

        id_intent = self.input_handler(
            prompt="What expense would you like to update? (Enter an ID)",
            integer=True)

        expense = self.db.get_expense(id_intent)

        new_tags = self.input_handler(
            prompt="What tags would you like to set for this expense?")

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

        month = self.input_handler(
            prompt="What month would you like to see?\n"
            "Enter like '04' for April.")

        year = self.input_handler(
            prompt=f"Press Enter for {str(date.today())[:4]},"
            " or for a different year, enter like '19' for 2019.")

        total_cost = 0
        for expense in self.db.get_month(month, year):
            print(expense)
            total_cost += expense.cost
        if total_cost:
            print(f"\nThe total cost is {total_cost} yen.")
        else:
            print(f"There are no expenses for {year}-{month}.")
        self.main_menu()

    def print_tags(
        self, tag_holder: Optional[list] = None, new_tag: Optional[str] = None
    ) -> None:
        """Print all expenses with tags specified by the user."""

        if tag_holder is None:
            tag_holder = []

        if new_tag is None:
            for tag in self.db.get_distinct_tags():
                print(tag)
            new_tag = self.input_handler(
                prompt="\nWhich tag would you like to see?")

        tag_holder.append(new_tag)

        intent = self.input_handler(
            prompt="Enter other tags you want to see, or press Enter.")

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

        amount_intent = self.input_handler(
            prompt="Over how much would you like to see?",
            integer=True)

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

    def print_total(self) -> None:
        """Print total cost of all expenses."""

        print(f"Total expenses are {self.db.get_total()} yen.")
        self.main_menu()

    def input_handler(self,
                      prompt: str = "",
                      error_msg: str = "Please enter a valid input.",
                      destination: str = "main menu",
                      **kwargs) -> Any:
        '''Checks inputs based on parameters and redirects if invalid input.
        Following keyword arguments are supported:
        'allow_uppercase = True' for allowing capital letters
        boolean for yes / no inputs
        integer for integer inputs
        acceptable_inputs can be a tuple, list, or set of valid inputs
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
        """Send user a message and redirect to main menu."""
        if message:
            print(message)
        print(f"Returning to main menu.\n")
        self.main_menu()


def main() -> None:

    def cmd_line_arg_handler() -> dict:

        PYTHON_VERSION = "Python version: 3.9.2"

        opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]

        cmd_line_args = {"debug": False}

        if opts:

            if "-h" in opts or "--help" in opts:
                print(
                    "Expenses Tracker by Jason Tarka\n"
                    "Accepted command line arguments:\n"
                    '"-v" or "--version": Display version information\n'
                    '"-d" or "--debug": Enter debugging mode')
                sys.exit()

            if "-v" in opts or "--version" in opts:
                print(
                    "Application version: 1.1.0\n"
                    f"Python version: {PYTHON_VERSION}")
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
