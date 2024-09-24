"""Module for configuring and setting an update button within a frame."""

import tkinter as tk
from tkinter import ttk
from data import config


def set_widgets(frame):
    """Set up and configure buttons in the given frame."""

    def open_new_window():
        """Create a new window that overlaps the main window and hides the parent."""
        
        root = frame.winfo_toplevel()
        root.withdraw()  # Hide the parent window

        new_window = tk.Toplevel(root)
        new_window.title("Templates")
        new_window.wm_attributes('-topmost', 1)

        # Get the position of the main window
        root_width = root.winfo_width()
        root_height = root.winfo_height()
        root_x = root.winfo_x()
        root_y = root.winfo_y()

        # Set the new window position to overlap the main window
        new_window.geometry(f"{root_width}x{root_height}+{root_x}+{root_y}")

        # Add a label in the new window
        label = tk.Label(new_window, text="This is a new window!")
        label.pack(pady=20)

        # Add a close button in the new window
        close_button = tk.Button(new_window, text="Close", command=lambda: close_new_window(new_window, root))
        close_button.pack(pady=10)

        new_window.protocol("WM_DELETE_WINDOW", lambda root=root, new_window=new_window: on_child_close(root, new_window))

    def close_new_window(new_window, root):
        """Close the new window and show the parent window again."""
        new_width = new_window.winfo_width()
        new_height = new_window.winfo_height()
        new_x = new_window.winfo_x()
        new_y = new_window.winfo_y()

        root.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")
        new_window.destroy()  # Close the new window
        root.deiconify()  # Show the parent window again

    def on_child_close(root, new_window):
        """Closes the main window when the child is closed."""
        new_window.destroy()
        root.destroy()

    # Configure the button style and set up the button
    style = ttk.Style()
    style.configure("button.TButton", background=config.COLOR_1)
    button_load = ttk.Button(frame, text="UPDATE", style="button.TButton", command=open_new_window)
    button_load.grid(row=0, column=1, padx=config.PADDING, pady=config.PADDING, sticky="ew")

    # Adjust row and column weights to make the frame responsive
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=0)
