import sqlite3
import sys

def init_db(database: str = "data/db.sqlite3"):
    """Initialize the database."""

    sql_script = '''
    /* Table for categories */
    CREATE TABLE IF NOT EXISTS category (
        category_id INTEGER PRIMARY KEY,
        category_name VARCHAR(20) UNIQUE NOT NULL
    );

    /* Table for templates */
    CREATE TABLE IF NOT EXISTS templates (
        template_id INTEGER PRIMARY KEY,
        template_name VARCHAR(20) NOT NULL,
        template_text TEXT NOT NULL,
        category_id INT, -- Foreign key to category table
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES category (category_id) 
        ON DELETE SET NULL -- Temporarily set to NULL on delete
    );

    /* Trigger to move templates to 'Unassigned' category if category is deleted */
    CREATE TRIGGER IF NOT EXISTS move_templates_to_unassigned
    AFTER UPDATE ON templates
    FOR EACH ROW
    WHEN NEW.category_id IS NULL
    BEGIN
        UPDATE templates 
        SET category_id = (SELECT category_id FROM category WHERE category_name = 'Unassigned')
        WHERE template_id = NEW.template_id;
    END;

    /* Table for tags */
    CREATE TABLE IF NOT EXISTS tags (
        tag_id INTEGER PRIMARY KEY,
        tag_name VARCHAR(255) UNIQUE NOT NULL
    );

    /* Table to associate templates with tags (many-to-many relationship) */
    CREATE TABLE IF NOT EXISTS template_tags (
        template_id INT NOT NULL,
        tag_id INT NOT NULL,
        PRIMARY KEY (template_id, tag_id), -- Composite key
        FOREIGN KEY (template_id) REFERENCES templates (template_id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tags (tag_id) ON DELETE CASCADE
    );

    /* Table for quick copy buttons */
    CREATE TABLE IF NOT EXISTS quick_copy_buttons (
        button_id INTEGER PRIMARY KEY,
        button_icon VARCHAR(1) NOT NULL,
        button_text VARCHAR(20) NOT NULL
    );

    /* Insert dummy data into category table */
    INSERT OR IGNORE INTO category (category_name) VALUES
        ('Unassigned'),
        ('Completeness'),
        ('Efficiency'),
        ('Style'),
        ('Documentation'),
        ('Links'),
        ('Other');

    /* Insert dummy data into quick_copy_buttons table */
    INSERT OR IGNORE INTO quick_copy_buttons (button_icon, button_text) VALUES
        ('Space', '‎ ‎ ‎ ‎ '),
        ('❌', '❌ '),
        ('●', '●'),
        ('○', '○'),
        ('▪', '▪'),
        ('→', '→'),
        ('✔️', '✔️ '),
        ('⚠️', '⚠️'),
        ('🔎', '🔎'),
        ('📖', '📖'),
        ('🔗', '🔗'),
        ('💡', '💡'),
        ('⬆️', '⬆️');
    '''

    # Connect to the SQLite database and execute the SQL script
    try:
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            cursor.executescript(sql_script)
            conn.commit()
            print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")
