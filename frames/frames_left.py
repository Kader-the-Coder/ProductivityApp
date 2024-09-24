"""Module for configuring and setting buttons within a frame."""

from tkinter import ttk
from data import config
from utils import database

def set_widgets(frame):
    """Set up and configure buttons in the given frame."""
    style = ttk.Style()
    style.configure("button.TButton", background=config.COLOR_2)

    button_data = database.get_quick_copy_buttons()
    for _, data in enumerate(button_data):
        button = ttk.Button(frame, text=data[0], width=4, style="button.TButton",)
        button.pack(fill="x")
    
    button_open = ttk.Button(frame, text="^", width=4, style="button.TButton",)
    button_open.pack(fill="x", side="bottom")
