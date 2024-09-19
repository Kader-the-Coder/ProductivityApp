"""XXX"""

import tkinter as tk
from tkinter import ttk

def set_widgets(frame):
    """
    Sets up a scrollable frame and adds widgets within the given ttk frame.
    """
    # Make the frame expandable
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Create canvas and vertical scrollbar
    canvas = tk.Canvas(frame, highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create and add a frame inside the canvas
    scrollable_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Update the scroll region whenever the frame is resized
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


    def on_mouse_wheel(event):
        """Scroll the canvas with the mouse wheel."""
        # Calculate the height of the canvas and the frame
        canvas_height = canvas.bbox("all")[3]  # Bottom y-coordinate of the canvas content
        frame_height = frame.winfo_height()

        # Only scroll if the canvas content is taller than the visible frame
        if canvas_height > frame_height:
            # Scroll the canvas
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


    def bind_to_widget(widget):
        widget.bind("<MouseWheel>", on_mouse_wheel)  # Windows and macOS
        widget.bind("<Button-4>", on_mouse_wheel)  # Linux scroll up
        widget.bind("<Button-5>", on_mouse_wheel)  # Linux scroll down        


    def add_widgets(frame):
        """Add widgets (buttons) to the scrollable frame"""
        # Configure the columns to expand and fill available space
        for i in range(5):
            button = ttk.Button(frame, text="C", width=4)
            button.grid(row=i, column=0)
            checkbutton = tk.Checkbutton(frame, text=f"Button {i}")
            checkbutton.grid(row=i, column=1)
            label = ttk.Label(frame, text="- Some other info")
            label.grid(row=i, column=2)
            bind_to_widget(button)
            bind_to_widget(checkbutton)
            bind_to_widget(label)


    # Bind mouse wheel events to the canvas
    bind_to_widget(canvas)
    bind_to_widget(scrollable_frame)

    add_widgets(scrollable_frame)
