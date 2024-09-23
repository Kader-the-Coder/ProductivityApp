import tkinter as tk
from tkinter import ttk
from frames import frames_top, frames_left, frames_body
from data import config


class ProductivityApp:
    """Main application class for the Productivity App."""

    def __init__(self, root):
        root.title(config.WINDOW_TITLE)
        root.geometry(f"{config.DEFAULT_WIDTH}x{config.DEFAULT_HEIGHT}")
        root.wm_attributes('-topmost', 1)
        self.create_styles()
        self.create_frames(root)
    
    def create_styles(self):
        """Configure styles for the application."""
        s_top = ttk.Style()
        s_top.configure("frameTop.TFrame", background='#333333')
        s_left = ttk.Style()
        s_left.configure("frameLeft.TFrame", background='#333333')
        s_body = ttk.Style()
        s_body.configure("frameBody.TFrame", background='#333333')

    def create_frames(self, root):
        """Create frames and place them in the grid."""
        frame_top = ttk.Frame(root, borderwidth=config.FRAME_BORDER_WIDTH, relief=config.FRAME_RELIEF, width=400, height=32, style="frameTop.TFrame")
        frame_top.grid(row=0, column=0, columnspan=2, padx=config.PADDING, pady=config.PADDING, sticky="ew")
        frames_top.set_widgets(frame_top)

        frame_left = ttk.Frame(root, borderwidth=config.FRAME_BORDER_WIDTH, relief=config.FRAME_RELIEF, width=32, height=250, style="frameLeft.TFrame")
        frame_left.grid(row=1, column=0, rowspan=2, padx=config.PADDING, pady=config.PADDING, sticky="ns")
        frames_left.set_widgets(frame_left)

        # Create a PanedWindow for the body frames (top and bottom)
        frame_body = ttk.PanedWindow(root, orient=tk.VERTICAL, style="frameBody.TFrame")
        frame_body.grid(row=1, column=1, rowspan=2, padx=config.PADDING, pady=config.PADDING, sticky="nsew")
        
        frame_body_top = ttk.Frame(frame_body, borderwidth=config.FRAME_BORDER_WIDTH, relief=config.FRAME_RELIEF, width=280)
        frame_body.add(frame_body_top, weight=1)
        frames_body.set_widgets(frame_body_top)

        frame_body_bottom = ttk.Frame(frame_body, borderwidth=config.FRAME_BORDER_WIDTH, relief=config.FRAME_RELIEF, width=280)
        frame_body.add(frame_body_bottom, weight=1)
        frames_body.set_widgets(frame_body_bottom)

        # Configure grid to handle sizes
        root.grid_rowconfigure(0, minsize=32)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)
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
