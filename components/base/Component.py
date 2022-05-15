import tkinter as tk
from typing import Any

from components.base.Box import Box


class Component(tk.Frame):
    def __init__(self, parent: Box, **kwargs) -> None:
        super().__init__(parent, **kwargs)

    def get(self) -> Any:
        """Get value from a component."""
        pass

    def reset(self) -> None:
        """Reset component value back to initial setting."""
        pass
