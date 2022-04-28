from typing_extensions import TypedDict
import tkinter as tk


class TagInfo(TypedDict):
    value: int
    button: tk.Checkbutton


class FieldInfo(TypedDict):
    name: str
    label: str
