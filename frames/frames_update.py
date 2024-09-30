"""Module for configuring and setting up the update window."""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils import database
from utils.widgets import (
    highlight_row, add_scrollable_frame, bind_scroll_events, add_widgets
)


def set_widgets(root, instance, new_window, default:int = None):
    """Set up and configure buttons in the given frame."""

    def configure_top_frame():
        """
        Default represents the default template details to display.
        """

        # Create top frame widgets
        category_label = tk.Label(frame_top, text="Category", anchor="e")
        category = tk.Entry(frame_top)
        name_label = tk.Label(frame_top, text="Name", anchor="e")
        name = tk.Entry(frame_top)
        tag_label = tk.Label(frame_top, text="Tags", anchor="e")
        tags = tk.Entry(frame_top)
        template_text = tk.Text(frame_top, height=5, wrap="word", undo=True, autoseparators=True)

        def add_update_template():
            new_category = category.get()
            if new_category in [c[0] for c in database.get_categories()]:
                new_name = name.get()
                new_tags = [tag.strip() for tag in tags.get().split(",")]
                new_template = template_text.get("1.0", tk.END).strip()

                # Update an existing template
                if add_template_button.template:
                    new_name = name.get()
                    new_tags = [tag.strip() for tag in tags.get().split(",")]
                    new_template = template_text.get("1.0", tk.END).strip()
                    database.update_template(
                        add_template_button.template,
                        new_category,
                        new_name,
                        new_tags,
                        new_template
                        )
                    if default:
                        close_new_window(root, new_window, instance)
                    return

                # Create a new template
                database.create_template(
                    new_name,
                    new_template,
                    new_category,
                    new_tags,
                    )
                cancel_template()
                return
            
            messagebox.showerror("ERROR", "Category does not exist.")  

        def cancel_template():
            if default:
                close_new_window(root, new_window, instance)
                return
            category.delete(0, tk.END)
            name.delete(0, tk.END)
            tags.delete(0, tk.END)
            template_text.delete(1.0, tk.END)
            add_template_button.template = None
            add_template_button.configure(text="Insert")

        def delete_template():
            if add_template_button.template:
                if messagebox.askokcancel("Warning", "Delete template?"):
                    database.delete_template(add_template_button.template)
                    messagebox.showinfo("Info", "Template has been deleted.")

        add_template_button = tk.Button(frame_top, text="Insert", command=add_update_template)
        add_template_button.template = None  # For editing templates
        cancel_add_template_button = tk.Button(frame_top, text="Cancel", command=cancel_template)
        delete_add_template_button = tk.Button(frame_top, text="Delete", command=delete_template)

        # Add widgets to top frame
        category_label.grid(row=0, column=0, sticky="nsew")
        category.grid(row=0, column=1, columnspan=2, sticky="nsew")
        name_label.grid(row=1, column=0, sticky="nsew")
        name.grid(row=1, column=1, columnspan=2, sticky="nsew")
        tag_label.grid(row=2, column=0, sticky="nsew")
        tags.grid(row=2, column=1, columnspan=2, sticky="nsew")
        template_text.grid(row=3, column=0, columnspan=3, sticky="nsew")
        add_template_button.grid(row=4, column=2, sticky="ew")
        cancel_add_template_button.grid(row=4, column=1, sticky="ew")
        delete_add_template_button.grid(row=4, column=0, sticky="ew")

        # Configure the grid for the top frame
        frame_top.grid_rowconfigure(0, weight=0)
        frame_top.grid_rowconfigure(1, weight=0)
        frame_top.grid_rowconfigure(2, weight=0)
        frame_top.grid_rowconfigure(3, weight=1)
        frame_top.grid_columnconfigure(0, weight=1)
        frame_top.grid_columnconfigure(1, weight=1)
        frame_top.grid_columnconfigure(2, weight=1)

        return (category, name, tags, template_text, add_template_button)

    def configure_middle_frame(category, name, tags, template_text, add_template_button):
        # Add all templates in the database

        def widget_layout(canvas, _instance, scrollable_frame, template, row_index):
            """Create and add row widgets to scrollable frame."""

            def edit_template():
                category.delete(0, tk.END)
                category.insert(0, database.get_categories()[template[3] - 1])
                name.delete(0, tk.END)
                name.insert(0, template[1])
                tags.delete(0, tk.END)
                tags.insert(0, ", ".join(database.get_tags(template[0])))
                template_text.delete(1.0, tk.END)
                template_text.insert(tk.END, template[2])

                add_template_button.template = template[0]
                add_template_button.configure(text="Update")

            # Create widgets
            label = tk.Label(scrollable_frame, text=f"{row_index}. {template[1]}", anchor="w",)
            label.associated_text = template[2]

            button = tk.Button(scrollable_frame, text="Edit", width=4, command=edit_template)

            # Place widgets
            label.grid(row=row_index, column=0, sticky="we")
            button.grid(row=row_index, column=1, sticky="e")

            # Bind hover events for row highlight
            highlight_row([label, button])

            # Apply bindings to widgets
            bind_scroll_events(label, canvas)
            bind_scroll_events(button, canvas)

            # Ensure widgets take up the entire width of scrollable frame
            scrollable_frame.grid_columnconfigure(0, weight=1)
            scrollable_frame.grid_columnconfigure(1, weight=0)

            # Display a default selected template on load
            if default:
                template = default
                edit_template()

        canvas, scrollable_frame = add_scrollable_frame(frame_middle)
        add_widgets(widget_layout, instance, canvas, scrollable_frame)

    def configure_bottom_frame():

        # Add a close button
        close_button = tk.Button(
            frame_bottom, text="Close",
            command=lambda: close_new_window(root, new_window, instance)
        )
        close_button.grid(column=1, sticky="ew")

    # Create a PanedWindow to allow resizing between the top and middle frames
    paned_window = ttk.PanedWindow(new_window, orient=tk.VERTICAL)
    paned_window.grid(row=0, column=0, sticky="nsew")

    # Create frames
    frame_top = ttk.Frame(paned_window, padding=10)
    frame_middle = ttk.Frame(paned_window, padding=10, relief="sunken")
    frame_bottom = ttk.Frame(new_window, padding=10)

    # Add frames
    paned_window.add(frame_top, weight=1)
    paned_window.add(frame_middle, weight=3)
    frame_bottom.grid(row=2, column=0, sticky="nsew")

    # Configure frames
    category, name, tags, template_text, add_template_button = configure_top_frame()
    configure_middle_frame(category, name, tags, template_text, add_template_button)
    configure_bottom_frame()

    # Configure new window
    new_window.grid_rowconfigure(0, weight=1)
    new_window.grid_columnconfigure(0, weight=1)


def close_new_window(root, new_window, instance):
    """Close the new window and show the parent window again."""
    new_width = new_window.winfo_width()
    new_height = new_window.winfo_height()
    new_x = new_window.winfo_x()
    new_y = new_window.winfo_y()

    root.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")
    new_window.destroy()  # Close the new window
    root.deiconify()  # Show the parent window again
    instance.reload_window()
