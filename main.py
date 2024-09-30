"""Main entry point of the application"""
import tkinter as tk
from frames.frames_main import TemplatePro

if __name__ == "__main__":
    main_root = tk.Tk()
    app = TemplatePro(main_root)
    main_root.mainloop()
