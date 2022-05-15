import tkinter as tk

from repository.repository import Repository


class Box(tk.Frame):
    def __init__(self, root, db: Repository, **kwargs) -> None:
        super().__init__(root, **kwargs)
        self.db = db
