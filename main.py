"""XXX"""
import tkinter as tk
from tkinter import ttk
from frames import frames_top, frames_left, frames_body_top, frames_body_bot
from data import config


class ProductivityApp:
    """XXX"""
    def __init__(self, root):
        root.title(config.WINDOW_TITLE)
        root.geometry(f"{config.DEFAULT_WIDTH}x{config.DEFAULT_HEIGHT}")
        root.wm_attributes('-topmost', 1)

        # Bind the <Configure> event to the on_resize method
        # root.bind("<Configure>", self.on_resize)

        # Create frames and place them in the grid
        frame_top = ttk.Frame(root, borderwidth=config.FRAME_BORDER_WIDTH, relief=config.FRAME_RELIEF, width=400, height=32)
        frame_top.grid(row=0, column=0, columnspan=2, padx=config.PADDING, pady=config.PADDING, sticky="ew")
        frames_top.set_widgets(frame_top)

        frame_left = ttk.Frame(root, borderwidth=config.FRAME_BORDER_WIDTH, relief=config.FRAME_RELIEF, width=32, height=250)
        frame_left.grid(row=1, column=0, rowspan=2, padx=config.PADDING, pady=config.PADDING, sticky="ns")
        frames_left.set_widgets(frame_left)

        frame_body_top = ttk.Frame(root, borderwidth=config.FRAME_BORDER_WIDTH, relief=config.FRAME_RELIEF, width=280, height=125)
        frame_body_top.grid(row=1, column=1, padx=config.PADDING, pady=config.PADDING, sticky="nsew")
        frames_body_top.set_widgets(frame_body_top)

        frame_body_bottom = ttk.Frame(root, borderwidth=config.FRAME_BORDER_WIDTH, relief=config.FRAME_RELIEF, width=280, height=125)
        frame_body_bottom.grid(row=2, column=1, padx=config.PADDING, pady=config.PADDING, sticky="nsew")
        frames_body_bot.set_widgets(frame_body_bottom)

        # Configure the grid to handle row and column sizes
        root.grid_rowconfigure(0, minsize=32)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, minsize=32)
        root.grid_columnconfigure(1, weight=1)

    def on_resize(self, event):
        """
        DEBUG FUNCTION
        Get the current width and height of the window
        """
        width = event.width
        height = event.height
        print(f"Window resized to: {width}x{height}")


if __name__ == "__main__":
    main_root = tk.Tk()
    app = ProductivityApp(main_root)
    main_root.mainloop()
