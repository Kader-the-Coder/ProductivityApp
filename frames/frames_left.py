"""Module for configuring and setting buttons within a frame."""

from tkinter import ttk
from data import config


def set_widgets(frame):
    """Set up and configure buttons in the given frame."""
    style = ttk.Style()
    style.configure("button.TButton", background=config.COLOR)
    button1 = ttk.Button(frame, text="A", width=4, style="button.TButton",)
    button1.pack(fill="x")
    button2 = ttk.Button(frame, text="B", width=4, style="button.TButton",)
    button2.pack(fill="x")
    button_open = ttk.Button(frame, text="^", width=4, style="button.TButton",)
    button_open.pack(fill="x", side="bottom")
