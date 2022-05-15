import tkinter as tk
from components.base.Box import Box


class ReadoutBox(Box):
    def __init__(self, parent, db, **kwargs):
        super().__init__(parent, db, **kwargs)
        self.pack(side="right")
        tk.Button().pack()
