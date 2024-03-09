"""
FILE : helper_functions.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: Small functions not directly part of any module
STUDENTS I DISCUSSED THE EXERCISE WITH: 
WEB PAGES I USED: https://chat.openai.com/
NOTES: ...
"""

import json

def save_to_json(data, filename) -> None:
    """
    Save data to a JSON file.

    Parameters:
    - data: Dictionary containing the data to be saved.
    - filename: Name of the JSON file to be saved.

    Returns:
    - None
    """
    with open(filename, 'w', encoding='UTF-8') as json_file:
        json.dump(data, json_file)
