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
    """
    Bind mouse wheel events to given widget for scrolling.

    NOTE: This function exists due to a bounding box issue in the
    configure_scroll_region function and should be sorted out at a
    later date.
    """
    widget.bind("<MouseWheel>", lambda e: on_mouse_wheel(e, canvas))  # Windows and macOS
    widget.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux scroll up
    widget.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux scroll down


def highlight_row(widgets):
    """Change background color of a widget on hover."""

    def highlight(_event, row_widgets, highlight=True):
        """Binding function."""
        
        color = "darkgray" if highlight else "SystemButtonFace"
        for widget in row_widgets:
            widget.config(bg=color)

    for widget in widgets:
        widget.bind(
            "<Enter>",
            lambda event, row=widgets: highlight(event, row)
            )
        widget.bind(
            "<Leave>",
            lambda event, row=widgets: highlight(event, row, highlight=False)
            )


def add_widgets(widget_layout, instance, canvas, scrollable_frame,
                category=None, name=None, tags=None):
    """
    Add widgets to scrollable frame.

    widget_layout: A function with the following parameters:
        canvas, scrollable_frame, template, row_index
    """
    templates = database.get_templates(category, name, tags)
    for i, template in enumerate(templates):
        widget_layout(canvas, instance, scrollable_frame, template, i)


def configure_scroll_region(canvas, scrollable_frame):
    """Configure scroll region of canvas based on scrollable frame."""
    # Get the bounding box of the scrollable_frame
    bbox = scrollable_frame.bbox()
    if bbox:  # Check if bbox is valid
        canvas.configure(scrollregion=bbox)

        # Adjust the scrollregion if the content height is less than the
        # canvas height
        canvas_height = canvas.winfo_height()
        if bbox[3] <= canvas_height:  # bbox[3] is the bottom y coordinate
            canvas.configure(scrollregion=(0, 0, 0, canvas_height))


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

