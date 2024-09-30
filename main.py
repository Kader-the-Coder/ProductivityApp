"""Main entry point of the application"""
import sys
import os
import tkinter as tk
from data.init_db import init_db
from frames.frames_main import TemplatePro

# Set working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DATABASE_PATH = "data/db.sqlite3"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Create and initialize database.
        if sys.argv[1] == 'init_db':
            init_db()
        else:
            print("Usage: python main.py init_db")
    else:
        # Check if the database file exists before running the main loop
        if os.path.exists(DATABASE_PATH):
            # Main loop
            main_root = tk.Tk()
            app = TemplatePro(main_root)
            main_root.mainloop()
        else:
            print(f"Database file '{DATABASE_PATH}' does not exist. "
                  "Please initialize the database first by running:")
            print("python main.py init_db")
