import tkinter as tk

from components.base.Component import Component


class InputField(Component):
    def __init__(self, root, label, **kwargs) -> None:
        super().__init__(root, **kwargs)

        self.label = tk.Label(
            self,
            text=label,
        )
        self.field = tk.Entry(
            self,
        )
        self._align_horizontally()

    def _align_horizontally(self):
        self.label.pack(side="left")
        self.field.pack(side="right")

    def get(self):
        return self.field.get()

    def reset(self):
        self.field.delete(0, tk.END)
