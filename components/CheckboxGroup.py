import tkinter as tk
from typing import Dict, List

from components.base.Component import Component
from define.types import TagInfo


class CheckboxGroup(Component):
    def __init__(self, root, targets: List[str], **kwargs) -> None:
        super().__init__(root, **kwargs)

        self.targets = targets
        self.checkboxes = self.create_checkboxes()

    def create_checkboxes(self):
        checkboxes: Dict[str, TagInfo] = {}

        current_row = 0
        current_col = 0

        for target_name in self.targets:
            value = tk.IntVar()
            checkboxes[target_name] = {
                "value": value,
                "button": tk.Checkbutton(
                    self, text=target_name, variable=value
                ),
            }

            checkboxes[target_name].get("button").grid(
                row=current_row, column=current_col
            )

            if current_col < 2:
                current_col += 1
            else:
                current_col = 0
                current_row += 1
        return checkboxes

    def get(self):
        """Get all values from every checkbox and concatenate into a string."""
        final_targets = []
        for target in self.checkboxes:
            value = self.checkboxes[target]["value"].get()
            if value:
                final_targets.append(target)
        return ", ".join(final_targets)

    def reset(self):
        """Reset each checkbox to unchecked."""
        for checkbox_name in self.checkboxes:
            self.checkboxes[checkbox_name]["value"].set(0)
