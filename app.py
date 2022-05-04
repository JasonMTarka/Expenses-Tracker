import tkinter as tk
import datetime
from typing import List, Dict

from repository.database import Database
from entities.expense import Expense
from components import InputField, AppButton, CheckboxGroup, RadioButtonGroup
from components.base import Component
from constants import (
    DOLLAR_TO_YEN,
    TAG_NAMES,
    ComponentNames,
    Currencies,
)
from define.types import FieldInfo


class MainApplication:
    """Class which builds and manages UI."""

    def __init__(self, root) -> None:
        self.db = Database()
        self.components = self.create_components(root)
        self.render_components()
        self.reset_cursor()

    def create_components(self, root) -> dict[ComponentNames, Component]:
        components: Dict[ComponentNames, Component] = {}

        input_fields: List[FieldInfo] = [
            {"name": ComponentNames.NAME, "label": "Expense Name: "},
            {"name": ComponentNames.COST, "label": "Expense Cost: "},
            {"name": ComponentNames.DATE, "label": "Expense Date: "},
        ]
        for field in input_fields:
            frame = InputField(root, field["label"])
            components[field["name"]] = frame

        components[ComponentNames.CURRENCY] = RadioButtonGroup(
            root, Currencies, Currencies.YEN, "Currency: "
        )

        components[ComponentNames.TAGS] = CheckboxGroup(root, TAG_NAMES)

        components[ComponentNames.CREATE] = AppButton(
            root, self.create_expense
        )

        return components

    def create_expense(self):
        name = self.components[ComponentNames.NAME].get()
        cost = self.components[ComponentNames.COST].get()
        date = self.components[ComponentNames.DATE].get()
        tags = self.components[ComponentNames.TAGS].get()
        currency = self.components[ComponentNames.CURRENCY].get()

        if not date:
            date = datetime.date.today()

        if currency == Currencies.DOLLARS.value:
            cost = str(round(float(cost) / DOLLAR_TO_YEN))

        expense = Expense(0, date=date, name=name, cost=cost, tags=tags)

        try:
            self.db.add_expense(expense)
            self.clear_fields()
            self.reset_cursor()

        except:
            print("error")

    def clear_fields(self):
        for field_name in ComponentNames:
            self.components[field_name].reset()

    def reset_cursor(self):
        self.components[ComponentNames.NAME].field.focus_set()

    def render_components(self):
        component_order = [
            ComponentNames.NAME,
            ComponentNames.CURRENCY,
            ComponentNames.COST,
            ComponentNames.DATE,
            ComponentNames.TAGS,
            ComponentNames.CREATE,
        ]
        for i, component_name in enumerate(component_order):
            component = self.components[component_name]

            if i == (len(component_order) - 1):
                component.pack(pady=(15))
            else:
                component.pack(pady=(2))


def main() -> None:
    """Set up interactive window."""
    root = tk.Tk()
    MainApplication(root)
    root.title("Expenses Tracker")
    root.mainloop()


if __name__ == "__main__":
    main()
