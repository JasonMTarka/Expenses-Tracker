import tkinter as tk

from components.ReadoutBox import ReadoutBox
from components.InputBox import InputBox
from repository.repository import Repository


def main() -> None:
    """Set up interactive window."""
    root = tk.Tk()
    db = Repository()
    InputBox(root, db).pack(side="left")
    ReadoutBox(root, db).pack(side="right")
    root.title("Expenses Tracker")
    root.mainloop()


if __name__ == "__main__":
    main()
