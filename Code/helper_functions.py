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

def passes_0(lst: list[float]) -> int:
    """
    returns the amount of times a given list passes through 0
    """
    if lst == []: 
        return 0
    count = 0
    for index in range(1, len(lst)):
        if lst[index] != 0:
            for i in range(1,len(lst)-index):
                if lst[index]*lst[index-i] < 0:
                    count += 1
                    break
                elif lst[index]*lst[index-i] > 0:
                    break
    return count
