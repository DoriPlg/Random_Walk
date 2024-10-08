"""
FILE : main.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: The page where the whole program will run
STUDENTS I DISCUSSED THE EXERCISE WITH: 
WEB PAGES I USED:
NOTES: ...
"""


import tkinter as tk
import sys
import os
from Code.walker_gui import SimulationGUI
from Code.simulation import run_from_json, run_and_plot

def run_gui() -> None:
    """
    This function runs the GUI.
    """
    root = tk.Tk()
    SimulationGUI(root)
    root.mainloop()

def print_help() -> None:
    """
    This function opens the help file.
    """
    path = os.getcwd() + "/src"
    with open(f"{path}/help.txt", "r", encoding="UTF-8") as f:
        print(f.read())
    
def run_json() -> None:
    """
    This function runs the simulation from a JSON file.
    """
    json_path = sys.argv[1]
    if not os.path.isfile(json_path):
        print(
            "Invalid JSON path. Please provide a valid file path or run with no arguments to use the GUI.")
        sys.exit(1)
    try:
        data, path = run_from_json(json_path)
        run_and_plot(data, path)
        print("Simulation completed successfully. \
You may view the results in the same directory as the JSON file.")
    except Exception as e:
        print(f"An error occurred while running the simulation:\n{e}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        run_gui()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "--help":
            help()
        else:
            run_json()
    else:
        print(
            "Invalid number of arguments. Please provide either no arguments or a single JSON path.")
