"""Module for configuring and setting an update button within a frame."""

from tkinter import ttk
from data import config


def set_widgets(frame):
    """Set up and configure buttons in the given frame."""
    style = ttk.Style()
    style.configure("button.TButton", background=config.COLOR)
    button_load = ttk.Button(frame, text="UPDATE", style="button.TButton")
    button_load.grid(row=0, column=1, padx=config.PADDING, pady=config.PADDING, sticky="ew")

    # Adjust row and column weights to make the frame responsive
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=0)
