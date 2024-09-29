"""Module for configuring and setting up the update window."""

import tkinter as tk
from tkinter import ttk
from utils.widgets import (
    highlight_row, add_scrollable_frame, bind_scroll_events, add_widgets
)


def set_widgets(root, new_window):
    """Set up and configure buttons in the given frame."""

    def configure_top_frame():
        # Create and add widgets to top frame.
        category_label = tk.Label(frame_top, text="Category", anchor="e")
        category = tk.Entry(frame_top)
        tag_label = tk.Label(frame_top, text="Tags", anchor="e")
        tags = tk.Entry(frame_top)
        template = tk.Text(frame_top, height=5, wrap="word", undo=True, autoseparators=True)
        add_template_button = tk.Button(frame_top, text="Add template")

        category_label.grid(row=0, column=0, sticky="nsew")
        category.grid(row=0, column=1, columnspan=2, sticky="nsew")
        tag_label.grid(row=1, column=0, sticky="nsew")
        tags.grid(row=1, column=1, columnspan=2, sticky="nsew")
        template.grid(row=2, column=0, columnspan=3, sticky="nsew")
        add_template_button.grid(row=3, column=2, sticky="e")

        # Configure the grid for the top frame
        frame_top.grid_rowconfigure(0, weight=0)
        frame_top.grid_rowconfigure(1, weight=0)
        frame_top.grid_rowconfigure(2, weight=1)
        frame_top.grid_columnconfigure(0, weight=1)
        frame_top.grid_columnconfigure(1, weight=1)
        frame_top.grid_columnconfigure(2, weight=1)

    def configure_middle_frame():
        # Add all templates in the database

        def widget_layout(canvas, scrollable_frame, template, row_index):
            """Create and add row widgets to scrollable frame."""

            # Create widgets
            label = tk.Label(scrollable_frame, text=f"{row_index}. {template[0]}", anchor="w",)
            label.associated_text = template[1]
            button = tk.Button(scrollable_frame, text="Edit", width=4)

            # Place widgets
            label.grid(row=row_index, column=0, sticky="we")
            button.grid(row=row_index, column=1, sticky="e")

            # Bind hover events for row highlight
            highlight_row([label, button])

            # Apply bindings to widgets
            bind_scroll_events(label, canvas)
            bind_scroll_events(button, canvas)

            # Ensure widgets take up the entire width of scrollable frame
            scrollable_frame.grid_columnconfigure(0, weight=1)
            scrollable_frame.grid_columnconfigure(1, weight=0)

        canvas, scrollable_frame = add_scrollable_frame(frame_middle)
        add_widgets(widget_layout, scrollable_frame, canvas)

    def configure_bottom_frame():
        
        def close_new_window(new_window, root):
            """Close the new window and show the parent window again."""
            new_width = new_window.winfo_width()
            new_height = new_window.winfo_height()
            new_x = new_window.winfo_x()
            new_y = new_window.winfo_y()

            root.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")
            new_window.destroy()  # Close the new window
            root.deiconify()  # Show the parent window again        

        # Add a close button
        close_button = tk.Button(
            frame_bottom, text="Close",
            command=lambda: close_new_window(new_window, root)
        )
        close_button.grid(sticky="e")

    # Create a PanedWindow to allow resizing between the top and middle frames
    paned_window = ttk.PanedWindow(new_window, orient=tk.VERTICAL)
    paned_window.grid(row=0, column=0, sticky="nsew")

    # Create frames
    frame_top = ttk.Frame(paned_window, padding=10)
    frame_middle = ttk.Frame(paned_window, padding=10, relief="sunken")
    frame_bottom = ttk.Frame(new_window, padding=10)

    # Add frames
    paned_window.add(frame_top, weight=1)
    paned_window.add(frame_middle, weight=3)
    frame_bottom.grid(row=2, column=0, sticky="nsew")

    # Configure frames
    configure_top_frame()
    configure_middle_frame()
    configure_bottom_frame()

    # Configure new window
    new_window.grid_rowconfigure(0, weight=1)
    new_window.grid_columnconfigure(0, weight=1)
