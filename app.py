import tkinter as tk
import datetime
from repository.database import Database
from entities.expense import Expense
from components import InputField, AppButton, Checkboxes
from components.base import Component
from constants import Fields
from define.types import FieldInfo
from typing import List, Dict


class MainApplication:
    """Class which builds and manages UI."""

    def __init__(self, root) -> None:
        self.db = Database()
        self.frames = self.create_frames(root)
        AppButton(root, self.create_expense)

    def create_frames(self, root) -> dict[Fields, Component]:
        frames: Dict[Fields, Component] = {}
        input_fields: List[FieldInfo] = [
            {"name": Fields.NAME, "label": "Expense Name: "},
            {"name": Fields.COST, "label": "Expense Cost: "},
            {"name": Fields.DATE, "label": "Expense Date: "},
        ]
        for field in input_fields:
            frame = InputField(root, field["label"])
            frames[field["name"]] = frame

        frames[Fields.TAGS] = Checkboxes(
            root,
        )
        return frames

    def create_expense(self):
        name = self.frames[Fields.NAME].get()
        cost = self.frames[Fields.COST].get()
        date = self.frames[Fields.DATE].get()
        tags = self.frames[Fields.TAGS].get()

        if not date:
            date = datetime.date.today()

        expense = Expense(0, date=date, name=name, cost=cost, tags=tags)

        try:
            self.db.add_expense(expense)
            self.clear_fields()
            self.refocus_cursor()

        except:
            print("error")

    def clear_fields(self):
        self.frames[Fields.NAME].reset()
        self.frames[Fields.COST].reset()
        self.frames[Fields.DATE].reset()
        self.frames[Fields.TAGS].reset()

    def refocus_cursor(self):
        self.frames[Fields.NAME].field.focus_set()


def main() -> None:
    """Set up interactive window."""
    root = tk.Tk()
    MainApplication(root)
    root.title("Expenses Tracker")
    root.mainloop()


if __name__ == "__main__":
    main()
