import tkinter as tk
import datetime
from typing import List, Dict

from repository.database import Database
from entities.expense import Expense
from components import InputField, AppButton, Checkboxes
from components.base import Component
from constants import FieldNames
from define.types import FieldInfo


class MainApplication:
    """Class which builds and manages UI."""

    def __init__(self, root) -> None:
        self.db = Database()
        self.frames = self.create_frames(root)
        AppButton(root, self.create_expense)
        self.reset_cursor()

    def create_frames(self, root) -> dict[FieldNames, Component]:
        frames: Dict[FieldNames, Component] = {}
        input_fields: List[FieldInfo] = [
            {"name": FieldNames.NAME, "label": "Expense Name: "},
            {"name": FieldNames.COST, "label": "Expense Cost: "},
            {"name": FieldNames.DATE, "label": "Expense Date: "},
        ]
        for field in input_fields:
            frame = InputField(root, field["label"])
            frames[field["name"]] = frame

        frames[FieldNames.TAGS] = Checkboxes(
            root,
        )
        return frames

    def create_expense(self):
        name = self.frames[FieldNames.NAME].get()
        cost = self.frames[FieldNames.COST].get()
        date = self.frames[FieldNames.DATE].get()
        tags = self.frames[FieldNames.TAGS].get()

        if not date:
            date = datetime.date.today()

        expense = Expense(0, date=date, name=name, cost=cost, tags=tags)

        try:
            self.db.add_expense(expense)
            self.clear_fields()
            self.reset_cursor()

        except:
            print("error")

    def clear_fields(self):
        self.frames[FieldNames.NAME].reset()
        self.frames[FieldNames.COST].reset()
        self.frames[FieldNames.DATE].reset()
        self.frames[FieldNames.TAGS].reset()

    def reset_cursor(self):
        self.frames[FieldNames.NAME].field.focus_set()


def main() -> None:
    """Set up interactive window."""
    root = tk.Tk()
    MainApplication(root)
    root.title("Expenses Tracker")
    root.mainloop()


if __name__ == "__main__":
    main()
