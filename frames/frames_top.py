"""Module for configuring and setting widgets within a frame."""

from tkinter import ttk
from data import config


def set_widgets(frame):
    """Set up and configure buttons in the given frame."""
    style = ttk.Style()

    style.configure("entry.TEntry", background=config.COLOR_2)
    entry = ttk.Entry(frame, style="entry.TEntry")
    entry.grid(row=0, column=0, padx=config.PADDING, pady=config.PADDING,
               sticky="nsew")
    entry = ttk.Entry(frame, style="entry.TEntry")
    entry.grid(row=0, column=1, padx=config.PADDING, pady=config.PADDING,
               sticky="nsew")

    style.configure("button.TButton", background=config.COLOR_2)
    button_load = ttk.Button(frame, text="LOAD", width=8, style="button.TButton")
    button_load.grid(row=0, column=2, padx=config.PADDING, pady=config.PADDING)

    # Make frame responsive
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
