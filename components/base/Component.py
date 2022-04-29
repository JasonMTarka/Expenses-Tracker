import tkinter as tk


class Component(tk.Frame):
    def __init__(self, root, **kwargs) -> None:
        super().__init__(root, **kwargs)
        self.pack()

    def get(self) -> None:
        """Get value from a component."""
        pass

    def reset(self) -> None:
        """Reset component value back to initial setting."""
        pass
