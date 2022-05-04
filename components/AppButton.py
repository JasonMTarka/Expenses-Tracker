import tkinter as tk

from components.base.HoverButton import HoverButton
from components.base.Component import Component


class AppButton(Component):
    def __init__(self, root, callback, **kwargs) -> None:
        tk.Frame.__init__(self, master=root, **kwargs)

        button = HoverButton(
            self,
            text="Add Expense",
            padx=25,
            pady=4,
            borderwidth=3,
            command=callback,
        )
        button.pack()
        button.configure(activebackground="#d4d4ff")
