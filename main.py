"""Main entry point of the application"""

import tkinter as tk
from tkinter import ttk
from frames import (
    frames_top, frames_left, frames_body, frames_bottom
)
from data import config


class ProductivityApp:
    """Main application class for the Productivity App."""

    def __init__(self, root):
        """Initialize the application."""
        self.configure_root_window(root)
        self.configure_styles()
        self.create_frames(root)
        self.configure_grid(root)

    def configure_root_window(self, root):
        """Configure the main window."""
        root.title(config.WINDOW_TITLE)
        root.geometry(f"{config.DEFAULT_WIDTH}x{config.DEFAULT_HEIGHT}")
        root.config(bg=config.COLOR_1)
        root.wm_attributes('-topmost', 1)
        root.bind("<Button-1>", self.debug_widget)  # Debug binding

    def configure_styles(self):
        """Set up the styles for the application."""
        styles = [
            ("frameTop.TFrame", config.COLOR_2),
            ("frameLeft.TFrame", config.COLOR_2),
            ("frameBody.TFrame", config.COLOR_2),
            ("entry.TEntry", config.COLOR_1),
            ("button.TButton", config.COLOR_1),
        ]
        for style_name, background_color in styles:
            style = ttk.Style()
            style.configure(style_name, background=background_color)

    def create_frames(self, root):
        """Create and place frames and widgets."""
        
        # Add top frame
        self.add_frame(
            root, "frameTop.TFrame", frames_top.set_widgets,
            row=0, col=0, colspan=3, width=400, height=32
        )

        # Add left frame (Side button frame)
        self.add_frame(
            root, "frameLeft.TFrame", frames_left.set_widgets,
            row=1, col=0, rowspan=6, width=32, height=250
        )

        # Add top body frame
        self.create_body_section(root)

        # Add bottom frame
        self.add_frame(
            root, "frameTop.TFrame", frames_bottom.set_widgets,
            row=8, col=0, colspan=3, width=400, height=32
        )

    def create_body_section(self, root):
        """Create the body section with search entry and buttons."""
        search_entry = ttk.Entry(root, style="entry.TEntry")
        search_entry.grid(
            row=1, column=1, columnspan=2,
            padx=config.PADDING, pady=config.PADDING,
            sticky="nsew"
        )

        self.add_frame(
            root, "frameBody.TFrame", frames_body.set_widgets,
            row=2, col=1, rowspan=5, colspan=2, width=280
        )

        copy_button = ttk.Button(
            root, text="Copy", style="button.TButton"
        )
        copy_button.grid(
            row=7, column=2,
            padx=config.PADDING, pady=config.PADDING,
            sticky="e"
        )

    def add_frame(self, root, style, widget_func,
                  row, col, rowspan=1, colspan=1,
                  width=0, height=0):
        """Helper function to add and configure a frame."""
        frame = ttk.Frame(
            root, borderwidth=config.FRAME_BORDER_WIDTH,
            relief=config.FRAME_RELIEF, width=width, height=height,
            style=style
        )
        frame.grid(
            row=row, column=col, rowspan=rowspan,
            columnspan=colspan, padx=config.PADDING,
            pady=config.PADDING, sticky="nsew"
        )
        if widget_func:
            widget_func(frame)

    def configure_grid(self, root):
        """Configure grid row and column weights and minimum sizes."""
        row_config = {
            0: {"minsize": 32}, 1: {"minsize": 32},
            2: {"weight": 1}, 3: {"minsize": 32},
            4: {"minsize": 8}, 5: {"minsize": 32},
            6: {"weight": 1}, 7: {"minsize": 32},
            8: {"minsize": 32}
        }
        for row, config_values in row_config.items():
            root.grid_rowconfigure(row, **config_values)

        root.grid_columnconfigure(0, minsize=32)
        root.grid_columnconfigure(1, weight=1)

    def on_resize(self, event):
        """Debug method to get the current window size."""
        width = event.width
        height = event.height
        print(f"Window resized to: {width}x{height}")

    def debug_widget(self, event):
        """Debug method to get the widget being clicked."""
        widget = event.widget  # Get the clicked widget
        print(f"Clicked widget: {widget} of type {type(widget).__name__}")


if __name__ == "__main__":
    main_root = tk.Tk()
    app = ProductivityApp(main_root)
    # main_root.bind("<Configure>", app.on_resize)  # DEBUG BINDING
    main_root.mainloop()
