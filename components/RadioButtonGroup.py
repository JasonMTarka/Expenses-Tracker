import tkinter as tk
from enum import Enum
from typing import Type

from components.base.Component import Component
from constants import Currencies


class RadioButtonGroup(Component):
    def __init__(
        self,
        root,
        targets: Type[Currencies],
        default: Enum,
        label: str,
        **kwargs
    ) -> None:
        super().__init__(root, **kwargs)

        self.default = default
        self.targets = targets
        self.label = label
        self.group_value = tk.StringVar(root, default.value)
        self.create_buttons()

    def create_buttons(self):
        current_row = 0
        current_column = 0

        label = tk.Label(
            self,
            text=self.label,
        )
        label.grid(row=current_row, column=current_column)
        current_column += 1

        for target in self.targets:
            button = tk.Radiobutton(
                self,
                text=target.value,
                value=target.value,
                variable=self.group_value,
            )
            button.grid(row=current_row, column=current_column)
            current_column += 1

    def get(self):
        return self.group_value.get()

    def reset(self) -> None:
        self.group_value.set(self.default.value)
