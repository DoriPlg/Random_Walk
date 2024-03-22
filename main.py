"""
FILE : main.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: The page where the whole program will run
STUDENTS I DISCUSSED THE EXERCISE WITH: 
WEB PAGES I USED:
NOTES: ...
"""


from Code.simulation import run_from_json, run_and_plot, Simulation_3D
from Code.walker_3d import Walker3D as w3d  # For testing purposes
import tkinter as tk
from Code.walker_gui import SimulationGUI
import sys
import os

if __name__ == "__min__":

    if len(sys.argv) == 1:
        root = tk.Tk()
        app = SimulationGUI(root)
        root.mainloop()
    elif sys.argv[1] == "--help":
        with open("help.txt", "r") as f:
            print(f.read())
    elif len(sys.argv) == 2:
        json_path = sys.argv[1]
        if not os.path.isfile(json_path):
            print("Invalid JSON path. Please provide a valid file path or run with no arguments to use the GUI.")
            sys.exit(1)
        try:
            data, path = run_from_json(json_path)
            run_and_plot(data, path)
            print("Simulation completed successfully. \
You may view the results in the same directory as the JSON file.")
        except Exception as e:
            print(f"An error occurred while running the simulation:\n{e}")
    else:
        print("Invalid number of arguments. Please provide either no arguments or a single JSON path.")


if __name__ == "__main__":
    simu = Simulation_3D()
    simu.add_walker(w3d((0,0,0)))
    simu.add_walker(w3d((0,0,0)))
    simu.run_simulation(100)
    simu.mappit()
