import tkinter as tk


class Component(tk.Frame):
    def __init__(self, root, **kwargs) -> None:
        super().__init__(root, **kwargs)
        self.pack()

    def get(self) -> None:
        pass

    def reset(self) -> None:
        pass
