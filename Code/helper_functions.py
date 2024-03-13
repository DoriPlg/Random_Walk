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
from tkinter import filedialog

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


def load_simulation() -> dict:
        """
        loads data from a json from a chosen location"""
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                simulation_data = json.load(file)
            return simulation_data

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

def is_intable(x) -> bool:
    """
    checks if a characther is int
    :param x: the input to check
    """
    try:
        int(x)
        return True
    except ValueError:
        return False

def is_int(x) -> bool:
    """
    Checks if an input is a integer
    :param x: the input to check
    """
    try:
        return x == int(x)
    except:
        return False
    
def is_float(x) -> bool:
    """
    checks if an input is a floating point number
    :param x: the input to check
    """
    try:
        float(x)
        return True
    except ValueError:
        return False
