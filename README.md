# TemplatePro - Productivity Application

TemplatePro is an application designed to help users manage templates with basic tagging and categorization. The user interface, built with [`tkinter`](https://docs.python.org/3/library/tkinter.html), provides a starting point for organizing template data. 

> **NOTE:**  
> - The term "user-friendly" is used with a grain of salt — the app still needs some polishing.  
> - Tags and categories are **not customizable yet** (they are automatically added when a new template is created).  
> - Tags can be created but **cannot be removed**, and categories **cannot be removed** once added.  
> - "Productivity" is subjective and may vary depending on the user’s experience.  
> - [`tkinter`](https://docs.python.org/3/library/tkinter.html) was used because it is a built-in module and doesn’t come with any licensing complications.

> **WARNING:**
> - The code in this project is currently in a spaghetti state. It may not adhere to best practices for organization and readability. Refactoring and improving the code structure are ongoing tasks to enhance maintainability and clarity.
> - Please review with care.

## Features

- **Create and Manage Templates**: Users can create, remove, update, and delete (CRUD) templates.
- **Tag and Categorize Templates**: Associate templates with tags and categories for easy searching and filtering.
- **Copy Functionality**: Quickly copy data to the clipboard for use in other applications.
- **GUI-based Interface**: Easy-to-use interface built using `tkinter`.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Functionality](#functionality)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/TemplatePro.git
    cd TemplatePro
    ```

2. **Install the Dependencies**:
    Use `pip` to install the necessary dependencies listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure the Database**:
    Ensure the SQLite database (`db.sqlite3`) is set up correctly in the `data/` folder:
    ```bash
    python main.py init_db  # Creates an empty database
    ```

---

## Usage

1. **Run the Application**:
    Start the application by running the `main.py` script:
    ```bash
    python main.py
    ```

2. **Creating a Template**:
    In the GUI, you can enter the template's name, text, category, and associated tags.

3. **Copy Data**:
    Use the "Copy" button to copy relevant data to the clipboard.

3. **Paste Data**:
    Press Ctrl + V to paste.

---

## Project Structure

TemplatePro/
├── data/
│   ├── db.sqlite3        # SQLite database file
│   └── init_db.py        # Database initialization script
├── frames/
│   ├── frames_main.py     # Main GUI frames and logic
│   └── ...                # Other frames for the application
├── main.py                # Main entry point of the application
├── requirements.txt       # List of dependencies
└── README.md              # Project documentation

---

## Functionality

- **Database Management**: Initializes and manages the SQLite database for templates, categories, and tags.
- **User Interaction**: Intuitive GUI that facilitates user actions for managing templates.
- **Data Handling**: Supports CRUD operations for templates and handles associations with tags and categories.

---

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


