"""Module for configuring and setting an update button within a frame."""

import tkinter as tk
from tkinter import ttk
from data import config
from frames import frames_update


def open_new_window(frame, default:int = None):
    """Create a new window that overlaps the main window and hides the parent."""

    root = frame.winfo_toplevel()
    root.withdraw()  # Hide the parent window

    new_window = tk.Toplevel(root)
    new_window.title("Templates")
    new_window.wm_attributes('-topmost', 1)

    # Ensure new window overlaps old window.
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    new_window.geometry(f"{root_width}x{root_height}+{root_x}+{root_y}")

    frames_update.set_widgets(root, new_window, default)

    new_window.protocol(
        "WM_DELETE_WINDOW",
        lambda root=root, new_window=new_window: on_child_close(root, new_window)
        )


def on_child_close(root, new_window):
    """Closes the main window when the child is closed."""
    new_window.destroy()
    root.destroy()


def set_widgets(frame):
    """Set up and configure buttons in the given frame."""

    # Configure the button style and set up the button
    style = ttk.Style()
    style.configure("button.TButton", background=config.COLOR_1)
    button_load = ttk.Button(
        frame, text="UPDATE", style="button.TButton",
        command=lambda frame=frame: open_new_window(frame)
        )
    button_load.grid(row=0, column=1, padx=config.PADDING, pady=config.PADDING, sticky="ew")

    # Adjust row and column weights to make the frame responsive
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=0)
