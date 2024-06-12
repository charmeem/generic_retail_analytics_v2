# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 15:44:06 2024

@author: hp
"""

# Cleaning requirement script

import re

def remove_local_file_lines(filename):
    """Removes lines in a requirements.txt file that contain 'file:///' paths.

    Args:
        filename (str): The path to the requirements.txt file.
    """

    with open(filename, 'r') as f:
        lines = f.readlines()

    # Use a regular expression to find lines with 'file:///'
    cleaned_lines = [line for line in lines if not re.search(r'file:///', line)]

    with open(filename, 'w') as f:
        f.writelines(cleaned_lines)

    print(f"Local file lines removed from '{filename}'.")


requirements_file = "requirements_new.txt"
remove_local_file_lines(requirements_file)