"""Scrollable frame implementation with interactive widgets using Tkinter."""

import tkinter as tk
from tkinter import ttk
# from data import config
from utils import database
from utils.widgets import (
    highlight_row, add_scrollable_frame, bind_scroll_events, add_widgets
)

def widget_layout(canvas, scrollable_frame, template, row_index):
    """Create and add row widgets to scrollable frame."""
    checked = tk.IntVar()
    checkbutton = tk.Checkbutton(
        scrollable_frame,
        text=f"{template[0]}",
        anchor="w",
        variable=checked,
        )
    checkbutton.checked = checked
    checkbutton.associated_text = template[1]

    button = tk.Button(scrollable_frame, text="Edit", width=4)

    # Place widgets
    checkbutton.grid(row=row_index, column=0, sticky="we")
    button.grid(row=row_index, column=1, sticky="e")

    # Bind hover events for row highlight
    highlight_row([checkbutton, button])

    # Apply bindings to widgets
    bind_scroll_events(checkbutton, canvas)
    bind_scroll_events(button, canvas)

    # Ensure widgets take up the entire width of scrollable frame
    scrollable_frame.grid_columnconfigure(0, weight=1)
    scrollable_frame.grid_columnconfigure(1, weight=0)


def set_widgets(frame, instance=None, tags = None, tab_opened=0):
    """Set up a scrollable frame and add widgets within the given frame."""

    def on_tab_change(event):
        """Store selected tab in instance class when reloading widgets."""
        notebook = event.widget
        selected_tab_id = notebook.select()
        instance.default_tab = notebook.index(selected_tab_id)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Create a notebook to hold the tabs for each category
    # Set the style of the tabs
    style = ttk.Style()
    style.configure("Custom.TNotebook.Tab", foreground="black")
    style.map("TNotebook.Tab",
        foreground=[('selected', 'black'), ('!selected', '#665956')],
        )
    notebook = ttk.Notebook(frame, style='TNotebook')

    # Create and add tabs for each category in the database
    categories = database.get_categories()
    for _, category in enumerate(categories):
        tab_frame = ttk.Frame(notebook)
        tab_label = f"({len(database.get_templates(category[0], tags))}) {category[0][:4]}..."
        notebook.add(tab_frame, text=tab_label)

        # Make tab scrollable and add widgets to tab.
        canvas, scrollable_frame = add_scrollable_frame(tab_frame)
        add_widgets(widget_layout, scrollable_frame, canvas, category[0], tags)

    notebook.grid(row=0, column=0, sticky="nsew")
    notebook.select(tab_opened)

    # Detect and store a selected tab in instance class
    if instance:
        notebook.bind("<<NotebookTabChanged>>", on_tab_change)
