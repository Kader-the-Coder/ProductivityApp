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

    def create_text_widget(frame):
        """Add widgets (buttons) to the scrollable frame"""
        # Set a fixed size for the frame if necessary
        frame_width = frame.winfo_width()
        frame_height = frame.winfo_height()/4
        
        # Create and configure the Text widget
        text = tk.Text(frame, wrap="word")
        text.grid(row=0, column=0, sticky="nsew")
        text.config(width=frame_width, height=frame_height)  # Adjust height as needed

        button = ttk.Button(frame, text="Open")
        button.grid(row=1, column=0, sticky="e")  # Place button within the frame

        # Insert initial text
        text.insert(tk.END, "A test sentence that is very long to see how things wrap.")

    # Schedule the widget creation after the frame has been properly sized
    frame.after(100, lambda: create_text_widget(frame))

    # Optionally, ensure that the frame does not resize dynamically
    #frame.grid_propagate(False)  # Prevent frame from resizing based on child widgets
