"""XXX"""

from tkinter import ttk
from data import config


def set_widgets(frame):
    """XXX"""
    entry = ttk.Entry(frame)
    entry.grid(row=0, column=0, padx=config.PADDING, pady=config.PADDING, sticky="nsew")
    entry = ttk.Entry(frame)
    entry.grid(row=0, column=1, padx=config.PADDING, pady=config.PADDING, sticky="nsew")

    button_load = ttk.Button(frame, text="LOAD", width=8)
    button_load.grid(row=0, column=2, padx=config.PADDING, pady=config.PADDING)

    # Optional: Adjust row and column weights to make the frame responsive
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)