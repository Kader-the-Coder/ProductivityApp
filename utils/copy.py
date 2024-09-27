"""
provides utility functions for clipboard operations.
"""

import pyperclip


def copy(text):
    """Copies the given text to the clipboard."""
    pyperclip.copy(text)
