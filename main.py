"""Main entry point of the application"""

import tkinter as tk
from tkinter import ttk
from frames import frames_top, frames_left, frames_body, frames_bottom
from data import config


class ProductivityApp:
    """Main application class for the Productivity App."""

    def __init__(self, root):
        root.title(config.WINDOW_TITLE)
        root.geometry(f"{config.DEFAULT_WIDTH}x{config.DEFAULT_HEIGHT}")
        root.config(bg=config.COLOR)
        root.wm_attributes('-topmost', 1)

        self.create_frames(root)
        self.configure_grid(root)

    def create_frames(self, root):
        """Create and place frames and widgets"""
        # Top frame
        style_top = ttk.Style()
        style_top.configure("frameTop.TFrame", background=config.COLOR)
        self.add_frame(root, "frameTop.TFrame", frames_top.set_widgets,
                       row=0, col=0, colspan=3,
                       width=400, height=32)

        # Left frame (Side frame)
        style_left = ttk.Style()
        style_left.configure("frameLeft.TFrame", background=config.COLOR)
        self.add_frame(root, "frameLeft.TFrame", frames_left.set_widgets,
                       row=1, col=0, rowspan=6,
                       width=32, height=250)

        # Top body frame
        style_body = ttk.Style()
        style_body.configure("frameBody.TFrame", background=config.COLOR)
        self.add_body_section(root, row=1, col=1)

        # Separator
        self.add_separator(root, row=4, col=1, colspan=2)

        # Bottom body frame
        self.add_body_section(root, row=5, col=1)

        # Bottom frame
        self.add_frame(root, "frameTop.TFrame", frames_bottom.set_widgets,
                       row=8, col=0, colspan=3,
                       width=400, height=32)

    def add_frame(self, root, style, widget_func,
                  row, col, rowspan=1, colspan=1,
                  width=0, height=0):
        """Helper function to add a frame."""
        frame = ttk.Frame(root, borderwidth=config.FRAME_BORDER_WIDTH,
                          relief=config.FRAME_RELIEF,
                          width=width, height=height,
                          style=style)
        frame.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan,
                   padx=config.PADDING, pady=config.PADDING,
                   sticky="nsew")
        if widget_func:
            widget_func(frame)

    def add_body_section(self, root, row, col):
        """Helper function to create body sections"""
        style = ttk.Style()
        style.configure("entry.TEntry", background=config.COLOR)
        search_entry = ttk.Entry(root, style="entry.TEntry")
        search_entry.grid(row=row, column=col, columnspan=2,
                          padx=config.PADDING, pady=config.PADDING,
                          sticky="nsew")

        self.add_frame(root, "frameBody.TFrame", frames_body.set_widgets,
                       row=row+1, col=col, colspan=2,
                       width=280)

        style = ttk.Style()
        style.configure("button.TButton", background=config.COLOR)
        copy_button = ttk.Button(root, text="Copy", style="button.TButton")
        copy_button.grid(row=row+2, column=col+1,
                         padx=config.PADDING, pady=config.PADDING,
                         sticky="e")

    def add_separator(self, root, row, col, colspan=1):
        """Helper function to add a separator."""
        separator = ttk.Separator(root, orient='horizontal')
        separator.grid(row=row, column=col, columnspan=colspan,
                       pady=5,
                       sticky="ew")

    def configure_grid(self, root):
        """Configure grid row and column weights and minimum sizes."""
        row_config = {
            0: {"minsize": 32},
            1: {"minsize": 32},
            2: {"weight": 1},
            3: {"minsize": 32},
            4: {"minsize": 8},
            5: {"minsize": 32},
            6: {"weight": 1},
            7: {"minsize": 32},
            8: {"minsize": 32}
        }
        for row, config_values in row_config.items():
            root.grid_rowconfigure(row, **config_values)

        root.grid_columnconfigure(0, minsize=32)
        root.grid_columnconfigure(1, weight=1)

    def on_resize(self, event):
        """Debug function to get the current window size."""
        width = event.width
        height = event.height
        print(f"Window resized to: {width}x{height}")


if __name__ == "__main__":
    main_root = tk.Tk()
    app = ProductivityApp(main_root)
    main_root.bind("<Configure>", app.on_resize)  # DEBUG BINDING
    main_root.mainloop()
