import tkinter as tk

from components.base.HoverButton import HoverButton


class AppButton(tk.Frame):
    def __init__(self, root, callback, **kwargs) -> None:
        tk.Frame.__init__(self, master=root, **kwargs)

        button = HoverButton(
            root,
            text="Add Expense",
            padx=25,
            pady=4,
            borderwidth=3,
            command=callback,
        )
        button.pack()
        button.configure(activebackground="#d4d4ff")
