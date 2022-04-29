import tkinter as tk
from typing import Dict

from components.base.Component import Component
from define.types import TagInfo


class Checkboxes(Component):
    def __init__(self, root, **kwargs) -> None:
        super().__init__(root, **kwargs)

        self.tags = self.create_checkboxes()

    def create_checkboxes(self):
        tags: Dict[str, TagInfo] = {}

        tag_names = [
            "Groceries",
            "Dining",
            "Household",
            "Jason",
            "Xiaochen",
            "Social",
            "Travel",
            "Games",
            "Alcohol",
            "Big Purchases",
            "Bento",
            "Car",
            "Clothing",
        ]
        current_row = 0
        current_col = 0

        for tag_name in tag_names:
            value = tk.IntVar()
            tags[tag_name] = {
                "value": value,
                "button": tk.Checkbutton(self, text=tag_name, variable=value),
            }

            tags[tag_name].get("button").grid(
                row=current_row, column=current_col
            )

            if current_col < 2:
                current_col += 1
            else:
                current_col = 0
                current_row += 1
        return tags

    def get(self):
        """Get all values from every checkbox and concatenate into a string."""
        final_tags = []
        for tag in self.tags:
            value = self.tags[tag]["value"].get()
            if value:
                final_tags.append(tag)
        return ", ".join(final_tags)

    def reset(self):
        """Reset each checkbox to unchecked."""
        for tag in self.tags:
            self.tags[tag]["value"].set(0)
