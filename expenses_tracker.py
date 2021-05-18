from database import Database
from expense import Expense


class Application:
    def __init__(self, db):
        self.db = db

    def start(self):
        print()
        print("Welcome to your expenses tracker.")
        if self.db.test is True:
            print("DEBUGGING MODE!")
        print("What would you like to do?")
        self.main_menu()

    def main_menu(self):
        print()
        print("'add expense' - Add an expense.")
        print("'remove expense' - Remove an expense.")
        print("'update tags' - Update an expense's tags.")
        print("'get tag' - Get a list of all expenses in a tag.")
        print("'get distinct tags' - Get a list of all current tags.")
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

        elif intent == "update tags":
            print("What expense would you like to update?")
            id_intent = input()
            expense = self.db.get_expense(id_intent)
            print("What tags would you like to set for this expense?")
            new_tags = input()
            expense.tags = new_tags
            self.db.update_tag(expense)
            self.main_menu()

        elif intent == "get tag":
            print("Which tag would you like to see?")
            self.get_tags()

        elif intent == "get distinct tags":
            print()
            for expense in self.db.get_distinct_tags():
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

    def get_tags(self, holder=None, new_tag=None):
        if holder is None:
            holder = []
        if new_tag is None:
            new_tag = input()
        holder.append(new_tag)
        print("Enter other tags you want to see, or press Enter.")
        other_intent = input()
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
        print("What tags does this expense have?")
        tag_intent = input()
        expense = Expense(1, date_intent, name_intent, cost_intent, tag_intent)
        self.db.add_expense(expense)
        print("Expense added.")
        self.main_menu()

    def remove_expense(self, expense):
        self.db.remove_expense(expense)
        self.main_menu()


def main():
    db = Database()
    app = Application(db)
    app.start()


if __name__ == "__main__":
    main()
