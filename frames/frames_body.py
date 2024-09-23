"""Scrollable Frame Example with Widgets"""

import tkinter as tk
from tkinter import ttk


def set_widgets(frame):
    """Set up a scrollable frame and add widgets within the given frame."""

    def on_mouse_wheel(event):
        """Scroll the canvas with the mouse wheel."""
        canvas_height = canvas.bbox("all")[3]
        frame_height = frame.winfo_height()

        if canvas_height > frame_height:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


    def bind_to_widget(widget):
        """Bind mouse wheel events to the specified widget for scrolling."""
        widget.bind("<MouseWheel>", on_mouse_wheel)  # Windows and macOS
        widget.bind("<Button-4>", on_mouse_wheel)  # Linux scroll up
        widget.bind("<Button-5>", on_mouse_wheel)  # Linux scroll down        


    def add_widgets(scrollable_frame):
        """Add buttons, checkbuttons, and labels to the scrollable frame."""
        for i in range(1, 5):
            button = ttk.Button(scrollable_frame, text="C", width=4)
            button.grid(row=i, column=0)
            checkbutton = tk.Checkbutton(scrollable_frame, text=f"Button {i}")
            checkbutton.grid(row=i, column=1)
            label = ttk.Label(scrollable_frame, text="- Some other info")
            label.grid(row=i, column=2)
            bind_to_widget(button)
            bind_to_widget(checkbutton)
            bind_to_widget(label)


    # Make the frame expandable
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Create canvas and vertical scrollbar
    canvas = tk.Canvas(frame, highlightthickness=0)
    canvas.grid(row=1, column=0, sticky="nsew")
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=1, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas
    scrollable_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Update the scroll region whenever the frame is resized
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    # Optimize redrawing
    frame.bind("<Configure>", lambda e: canvas.update_idletasks())
    
    # Bind mouse wheel events to the canvas and scrollable frame
    bind_to_widget(canvas)
    bind_to_widget(scrollable_frame)

    # Add widgets to the scrollable frame
    add_widgets(scrollable_frame)
