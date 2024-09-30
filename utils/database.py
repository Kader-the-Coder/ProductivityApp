"""Interacts with the database"""

import sqlite3
from typing import List, Tuple, Optional


def get_categories(database:Optional[str] = "data\\db.sqlite3") -> List[Tuple]:
    """
    Returns the name of all categories in the database.

    Args:
        database: The database to connect two (optional).

    Returns:
        A list of tuples, each containing a category.
    """
    with sqlite3.connect(database) as db:
        cursor = db.cursor()
        query = '''
            SELECT category_name
            FROM category
        '''
        cursor.execute(query)
        data = cursor.fetchall()

    return data


def get_quick_copy_buttons(database:Optional[str] = "data\\db.sqlite3") -> List[Tuple]:
    """
    Returns the name and text of all quick copy buttons

    Args:
        database: The database to connect two (optional).

    Returns:
        A list of tuples, each containing the quick copy button
        names and texts.
    """
    with sqlite3.connect(database) as db:
        cursor = db.cursor()
        query = '''
            SELECT button_icon, button_text
            FROM quick_copy_buttons
        '''
        cursor.execute(query)
        data = cursor.fetchall()

    return data


def get_templates(
        category: Optional[str] = None,
        template_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        database: str = "data\\db.sqlite3"
    ) -> List[Tuple]:
    """
    Returns the name and text of all templates matching the specified
    category, tags, and template name. All parameters are optional.

    Args:
        category: The name of the category to filter templates by (optional).
        template_name: The name of the template to filter by (optional).
        tags: A list of tag names to filter templates by (optional).
        database: The database to connect to (optional).

    Returns:
        A list of tuples, each containing the template ID, name, text, category ID, and creation date.
    """
    with sqlite3.connect(database) as db:
        cursor = db.cursor()

        # Base query
        query = '''
            SELECT t.template_id, t.template_name, t.template_text, t.category_id, t.created_at
            FROM templates t
            LEFT JOIN category c ON t.category_id = c.category_id
            LEFT JOIN template_tags tt ON t.template_id = tt.template_id
            LEFT JOIN tags tg ON tt.tag_id = tg.tag_id
            WHERE 1=1
        '''
        params = []

        # Add filtering by category if provided
        if category:
            query += ' AND c.category_name = ?'
            params.append(category)

        # Add filtering by template name if provided
        if template_name:
            query += ' AND t.template_name LIKE LOWER(?)'
            params.append(f'%{template_name}%')

        # Add filtering by tags if provided
        elif tags:
            like_conditions = ' OR '.join('tg.tag_name LIKE LOWER(?)' for _ in tags)
            query += f' AND ({like_conditions})'
            params.extend([f'%{tag}%' for tag in tags])

        # Grouping to avoid duplicates in case of multiple tags
        query += ' GROUP BY t.template_id'

        # Execute query with dynamic parameters
        cursor.execute(query, params)
        templates = cursor.fetchall()

    return templates


def get_tags(template_id:int, database:Optional[str] = "data\\db.sqlite3") -> List[str]:
    """
    Returns all the tags associated with a given template ID.

    Args:
        template_id: The ID of the template to filter tags by.
        database: The database to connect to (optional).

    Returns:
        A list of tags.
    """
    with sqlite3.connect(database) as db:
        cursor = db.cursor()

        # Get all tag IDs associated with the given template ID.
        cursor.execute('''
            SELECT tag_id
            FROM template_tags
            WHERE template_id=?
        ''', (template_id,))

        tag_ids = cursor.fetchall()

        # If there are no tags associated, return an empty list.
        if not tag_ids:
            return [""]

        # Extract tag IDs from the fetched results
        tag_ids = [tag[0] for tag in tag_ids]

        # Prepare a placeholder string for the SQL query
        placeholders = ', '.join('?' for _ in tag_ids)

        # Execute the query to fetch tag names for the associated tag IDs
        query = f'''
            SELECT tag_name
            FROM tags
            WHERE tag_id IN ({placeholders})
        '''
        
        # Fetch the results
        cursor.execute(query, tag_ids)
        tags = cursor.fetchall()

    return [tag[0] for tag in tags]


def update_template(
        template_id:int,
        new_category:Optional[str] = None,
        new_name:Optional[str] = None,
        new_tags:Optional[List[str]] = None,
        new_template_text:Optional[str] = None,
        database:Optional[str] = "data\\db.sqlite3"
) -> None:
    """
    Updates a template with the provided information.

    Args:
        template_id: The ID of the template to update.
        new_category: The new category name to set (optional).
        new_name: The new template name to set (optional).
        new_tags: A list of new tags to associate with the template (optional).
        database: The database to connect to (optional).

    Returns:
        None.
    """

    # Format entries
    new_category = new_category.capitalize() if new_category else None
    new_name = new_name.capitalize() if new_name else None
    new_tags = [tag.capitalize() for tag in new_tags] if new_tags else []
    new_template_text = new_template_text.strip()

    with sqlite3.connect(database) as db:
        cursor = db.cursor()

        # Update template name if provided
        if new_name is not None:
            cursor.execute('''
                UPDATE templates
                SET template_name = ?
                WHERE template_id = ?
            ''', (new_name, template_id))

        # Update template category if provided
        if new_category is not None:
            # Find the category_id associated with the new category name
            cursor.execute('''
                SELECT category_id
                FROM category
                WHERE category_name = ?
            ''', (new_category,))
            category = cursor.fetchone()

            if category:  # If the category exists, update the template
                cursor.execute('''
                    UPDATE templates
                    SET category_id = ?
                    WHERE template_id = ?
                ''', (category[0], template_id))

        # Update tags if provided
        if new_tags:
            # Delete existing tags associated with the template
            cursor.execute('''
                DELETE FROM template_tags
                WHERE template_id = ?
            ''', (template_id,))

            # Insert new tags
            for tag_name in new_tags:
                # Check if the tag exists
                cursor.execute('''
                    SELECT tag_id
                    FROM tags
                    WHERE tag_name = ?
                ''', (tag_name,))
                tag = cursor.fetchone()

                if tag:  # If the tag exists, insert the association
                    cursor.execute('''
                        INSERT INTO template_tags (template_id, tag_id)
                        VALUES (?, ?)
                    ''', (template_id, tag[0]))
                else:  # If the tag does not exist, create it
                    cursor.execute('''
                        INSERT INTO tags (tag_name)
                        VALUES (?)
                    ''', (tag_name,))
                    new_tag_id = cursor.lastrowid  # Get the ID of the newly created tag

                    # Associate the new tag with the template
                    cursor.execute('''
                        INSERT INTO template_tags (template_id, tag_id)
                        VALUES (?, ?)
                    ''', (template_id, new_tag_id))

        # Update template text if provided
        if new_template_text is not None:
            cursor.execute('''
                UPDATE templates
                SET template_text = ?
                WHERE template_id = ?
            ''', (new_template_text, template_id))

        # Commit the changes
        db.commit()


def create_template(
        name: str,
        template_text: str,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        database: Optional[str] = "data\\db.sqlite3"
    ) -> None:
    """
    Creates a template with the provided information.

    Args:
        name: The name of the template.
        template_text: The text to store in the template.
        category: The category associated with the template (optional).
        tags: A list of new tags to associate with the template (optional).
        database: The database to connect to (optional).

    Returns:
        None.
    """

    # Format entries
    name = name.strip().capitalize()
    template_text = template_text.strip()
    category = category.capitalize() if category else None
    tags = [tag.capitalize() for tag in tags] if tags else []

    # Connect to the database
    with sqlite3.connect(database) as db:
        cursor = db.cursor()

        # Get category_id or set to 0 if the category does not exist
        category_id = 0  
        if category:
            # Check if category already exists
            cursor.execute('''
                SELECT category_id FROM category WHERE category_name = ?
            ''', (category,))
            result = cursor.fetchone()
            
            if result:
                # Retrieve the id
                category_id = result[0]

        # Insert the template
        cursor.execute('''
            INSERT INTO templates (template_name, template_text, category_id)
            VALUES (?, ?, ?)
        ''', (name, template_text, category_id))

        # Get the id of the newly inserted template
        template_id = cursor.lastrowid

        # Add tags
        if tags:
            for tag in tags:
                # Insert the tag if it does not exist
                cursor.execute('''
                    INSERT OR IGNORE INTO tags (tag_name)
                    VALUES (?)
                ''', (tag,))
                
                # Retrieve the tag_id of the inserted or existing tag
                cursor.execute('''
                    SELECT tag_id FROM tags WHERE tag_name = ?
                ''', (tag,))
                tag_id = cursor.fetchone()[0]

                # Associate the tag with the template
                cursor.execute('''
                    INSERT INTO template_tags (template_id, tag_id)
                    VALUES (?, ?)
                ''', (template_id, tag_id))

        # Commit the transaction
        db.commit()


def delete_template(template_id: int, database: Optional[str] = "data\\db.sqlite3") -> None:
    """
    Deletes a template with the given template_id from the database.

    Args:
        template_id: The ID of the template to delete.
        database: The database to connect to (optional, defaults to 'data\\db.sqlite3').

    Returns:
        None.
    """
    with sqlite3.connect(database) as db:
        cursor = db.cursor()

        # Delete associated entries in the template_tags table
        cursor.execute('''
            DELETE FROM template_tags WHERE template_id = ?
        ''', (template_id,))

        # Delete the template from the templates table
        cursor.execute('''
            DELETE FROM templates WHERE template_id = ?
        ''', (template_id,))

        db.commit()


# UNIT TESTS
if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print(get_templates(template_name="Code", tags=["Performance"], database="..\\data\\db.sqlite3"))
    #print(get_quick_copy_buttons(database="..\\data\\db.sqlite3"))
    #print(get_categories(database="..\\data\\db.sqlite3"))
    #print(get_tags(15, database="..\\data\\db.sqlite3"))
    update_template(1, new_name="TEST", database="..\\data\\db.sqlite3")
