"""Scrollable frame implementation with interactive widgets using Tkinter."""

import tkinter as tk
from tkinter import ttk
from data import config
from utils import database

def set_widgets(frame):
    """Set up a scrollable frame and add widgets within the given frame."""

    def on_mouse_wheel(event):
        """Scroll the canvas with the mouse wheel."""
        canvas_height = canvas.bbox("all")[3]
        frame_height = frame.winfo_height()

        if canvas_height > frame_height:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def bind_to_widget(widget):
        """Bind mouse wheel events to the given widget for scrolling."""
        widget.bind("<MouseWheel>", on_mouse_wheel)  # Windows and macOS
        widget.bind("<Button-4>", on_mouse_wheel)  # Linux scroll up
        widget.bind("<Button-5>", on_mouse_wheel)  # Linux scroll down

    def add_widgets(category, scrollable_frame):
        """Add widgets to the scrollable frame."""
        def on_enter_row(_event, row_widgets):
            """Change background COLOR_2 the widget on hover."""
            for widget in row_widgets:
                widget.config(bg="darkgray")

        def on_leave_row(_event, row_widgets):
            """Revert background COLOR_2 of widget on mouse leave."""
            for widget in row_widgets:
                widget.config(bg="SystemButtonFace")

        # Create widgets for each of the templates in database.
        templates = database.get_templates(category)
        for i, template in enumerate(templates):
            checkbutton = tk.Checkbutton(scrollable_frame,
                                         text=f"{template[0]}",
                                         anchor="w")
            button = tk.Button(scrollable_frame,
                               text="Edit",
                               width=4)

            # Place widgets in the grid
            checkbutton.grid(row=i, column=0, sticky="we")
            button.grid(row=i, column=1, sticky="e")

            # Bind the mouse enter and leave events for row highlight
            row_widgets = [checkbutton, button]
            for widget in row_widgets:
                widget.bind("<Enter>", lambda event,
                            row=row_widgets: on_enter_row(event, row))
                widget.bind("<Leave>", lambda event,
                            row=row_widgets: on_leave_row(event, row))

            # Apply bindings to widgets
            bind_to_widget(checkbutton)
            bind_to_widget(button)

            # Have widgets take up the entire width of scrollable_frame
            scrollable_frame.grid_columnconfigure(0, weight=1)
            scrollable_frame.grid_columnconfigure(1, weight=0)

    def configure_scrollable_frame(event):
        """Update scrollable frame width to match canvas width."""
        canvas_width = event.width
        scrollable_frame.config(width=canvas_width)
        canvas.itemconfig(window_id, width=canvas_width)


    notebook = ttk.Notebook(frame)
    notebook.grid(row=0, column=0, sticky="nsew")

    # Creating tabs for each category
    categories = database.get_categories()
    for _, category in enumerate(categories):
        category_name = category[0]  # Use a unique variable for category name
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=category_name)

        # Create canvas and vertical scrollbar for each tab
        canvas = tk.Canvas(tab, highlightthickness=0)
        canvas.grid(row=1, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Create the scrollable frame inside the canvas for each tab
        scrollable_frame = ttk.Frame(canvas, style="frame.TFrame")
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Bind events for this specific tab
        canvas.bind("<Configure>", lambda e, c=canvas, w_id=window_id, sf=scrollable_frame: configure_scrollable_frame(e, c, w_id, sf))
        scrollable_frame.bind("<Configure>", lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))

        # Bind mouse wheel to this tab's canvas and scrollable frame
        bind_to_widget(canvas)
        bind_to_widget(scrollable_frame)

        # Add widgets to the scrollable_frame in this tab, pass category_name to add_widgets
        add_widgets(category_name, scrollable_frame)


    # Make the frame expandable
    frame.grid_rowconfigure(0, weight=0)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)