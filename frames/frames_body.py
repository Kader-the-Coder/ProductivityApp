"""Scrollable frame implementation with interactive widgets using Tkinter."""

import tkinter as tk
from tkinter import ttk
# from data import config
from utils import database


def on_mouse_wheel(event, canvas):
    """Scroll the canvas with the mouse wheel."""
    scroll_speed = 1
    direction = -scroll_speed if event.delta > 0 else scroll_speed
    canvas.yview_scroll(direction, "units")


def bind_scroll_events(widget, canvas):
    """Bind mouse wheel events to given widget for scrolling."""
    widget.bind("<MouseWheel>", lambda e: on_mouse_wheel(e, canvas))  # Windows and macOS
    widget.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux scroll up
    widget.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux scroll down


def highlight_row(_event, row_widgets, highlight=True):
    """Change background color of a widget on hover."""
    color = "darkgray" if highlight else "SystemButtonFace"
    for widget in row_widgets:
        widget.config(bg=color)


def create_row_widgets(canvas, scrollable_frame, template, row_index):
    """Create and add row widgets to scrollable frame."""
    checkbutton = tk.Checkbutton(scrollable_frame, text=f"{template[0]}", anchor="w")
    button = tk.Button(scrollable_frame, text="Edit", width=4)

    # Place widgets
    checkbutton.grid(row=row_index, column=0, sticky="we")
    button.grid(row=row_index, column=1, sticky="e")

    # Bind hover events for row highlight
    row_widgets = [checkbutton, button]
    for widget in row_widgets:
        widget.bind(
            "<Enter>",
            lambda event, row=row_widgets: highlight_row(event, row)
            )
        widget.bind(
            "<Leave>",
            lambda event, row=row_widgets: highlight_row(event, row, highlight=False)
            )

    # Apply bindings to widgets
    bind_scroll_events(checkbutton, canvas)
    bind_scroll_events(button, canvas)

    # Ensure widgets take up the entire width of scrollable frame
    scrollable_frame.grid_columnconfigure(0, weight=1)
    scrollable_frame.grid_columnconfigure(1, weight=0)


def add_widgets(category, scrollable_frame, canvas):
    """Add widgets to scrollable frame."""
    templates = database.get_templates(category)
    for i, template in enumerate(templates):
        create_row_widgets(canvas, scrollable_frame, template, i)


def configure_scroll_region(canvas, scrollable_frame):
    """Configure scroll region of canvas based on scrollable frame."""
    bbox = scrollable_frame.bbox()
    if bbox:  # Check if bbox is valid
        canvas.configure(scrollregion=bbox)


def resize_canvas(event, canvas, window_id):
    """Resize the window_id to match the canvas width."""
    canvas_width = event.width
    canvas.itemconfig(window_id, width=canvas_width)


def add_scrollable_frame(frame):
    """Create a scrollable canvas with a frame inside for content."""
    canvas = tk.Canvas(frame, highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = ttk.Frame(canvas)
    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    scrollable_frame.bind(
        "<Configure>",
        lambda _event: configure_scroll_region(canvas, scrollable_frame)
        )
    canvas.bind(
        "<Configure>",
        lambda event: resize_canvas(event, canvas, window_id)
        )

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    bind_scroll_events(scrollable_frame, canvas)

    return canvas, scrollable_frame


def set_widgets(frame):
    """Set up a scrollable frame and add widgets within the given frame."""
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Create a notebook to hold the tabs for each category
    # Set the style of the tabs
    style = ttk.Style()
    style.configure("Custom.TNotebook.Tab", foreground="black")
    style.map("TNotebook.Tab",
    foreground=[('selected', 'black'), ('!selected', '#665956')],
    #background=[('selected', 'black'), ('!selected', 'white')]
    )
    notebook = ttk.Notebook(frame, style='TNotebook')

    # Create and add tabs for each category in the database
    categories = database.get_categories()
    for _, category in enumerate(categories):
        tab_frame = ttk.Frame(notebook)
        tab_label = f"{category[0]}"
        notebook.add(tab_frame, text=tab_label)

        # Make tab scrollable and add widgets to tab.
        canvas, scrollable_frame = add_scrollable_frame(tab_frame)
        add_widgets(category[0], scrollable_frame, canvas)

    notebook.grid(row=0, column=0, sticky="nsew")


    # DEBUG -------------------------------------------------------------------


    def on_tab_change(event):
        """Handle tab change events."""
        notebook = event.widget
        selected_tab_id = notebook.select()
        # selected_index = notebook.index(selected_tab_id)

        # DEBUG
        # selected_text = notebook.tab(selected_tab_id, "text")
        print(f"Selected Tab ID: {selected_tab_id}")
        # print(f"Selected Tab Index: {selected_index}")
        # print(f"Selected Tab Text: {selected_text}")


    notebook.bind("<<NotebookTabChanged>>", on_tab_change)  # DEBUG BINDING
