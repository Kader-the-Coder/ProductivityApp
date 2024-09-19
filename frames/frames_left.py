"""XXX"""

from tkinter import ttk


def set_widgets(frame):
    """XXX"""
    button1 = ttk.Button(frame, text="A", width=4)
    button1.pack(fill="x")
    button2 = ttk.Button(frame, text="B", width=4)
    button2.pack(fill="x")
    button_open = ttk.Button(frame, text="^", width=4)
    button_open.pack(fill="x", side="bottom")
