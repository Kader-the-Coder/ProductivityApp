"""Interacts with the database"""

import sqlite3
from typing import List, Tuple

def get_templates(category: str = None, tags: list = None) -> List[Tuple]:
    """
    Returns the name and text of all templates matching the specified
    category and tags. Both parameters are optional.

    Args:
        category: The name of the category to filter templates by (optional).
        tags: A list of tag names to filter templates by (optional).

    Returns:
        A list of tuples, each containing the template name and text.
    """
    with sqlite3.connect("..\\data\\db.sqlite3") as db:
        cursor = db.cursor()

        # Base query.
        query = '''
            SELECT t.template_name, t.template_text
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

        # Add filtering by tags if provided
        if tags:
            # Placeholder for variable length 'IN' clause for multiple tags
            placeholders = ','.join('?' for _ in tags)
            query += f' AND tg.tag_name IN ({placeholders})'
            params.extend(tags)

        # Grouping to avoid duplicates in case of multiple tags
        query += ' GROUP BY t.template_id'

        # Execute query with dynamic parameters
        cursor.execute(query, params)
        templates = cursor.fetchall()

    return templates


# UNIT TEST
if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(get_templates())
