import tkinter as tk


class HoverButton(tk.Button):
    """Class for changing button color when highlighting with cursor."""

    def __init__(self, master, **kwargs) -> None:
        """Initialize a Tkinter button and Enter/Leave bindings."""

        tk.Button.__init__(self, master=master, **kwargs)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, z) -> None:
        """Define entrance functionality."""

        self["background"] = self["activebackground"]

    def on_leave(self, z) -> None:
        """Define exit functionality."""

        self["background"] = self.defaultBackground
