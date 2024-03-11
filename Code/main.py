"""
FILE : main.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: The page where the whole program will run
STUDENTS I DISCUSSED THE EXERCISE WITH: 
WEB PAGES I USED:
NOTES: ...
"""

from walker import Walker
from barrier import Barrier
from portal import Portal
from mud import Mud
from simulation import Simulation

import tkinter as tk
from tkinter import filedialog
import json
"""
class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Walker Simulation")

        # Create a frame to hold the input widgets
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(padx=20, pady=20)

        # Create a label and entry for number of objects
        self.num_objects_label = tk.Label(self.input_frame, text="Number of Objects:")
        self.num_objects_label.grid(row=0, column=0)
        self.num_objects_entry = tk.Entry(self.input_frame)
        self.num_objects_entry.grid(row=0, column=1)

        # Create a button to add objects
        self.add_objects_button = tk.Button(self.input_frame, text="Add Objects", command=self.add_objects)
        self.add_objects_button.grid(row=0, column=2)

        # Create a button to load simulation from json
        self.load_button = tk.Button(self.input_frame, text="Load Simulation", command=self.load_simulation)
        self.load_button.grid(row=1, columnspan=3)

    def add_objects(self):
        num_objects = int(self.num_objects_entry.get())
        # Create input widgets for each object
        for i in range(num_objects):
            obj_label = tk.Label(self.input_frame, text=f"Object {i+1}:")
            obj_label.grid(row=i+2, column=0)
            # Add more input widgets as needed for each object's attributes

    def load_simulation(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                simulation_data = json.load(file)
            # Process the loaded simulation data, e.g., display key figures and graphs


if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationApp(root)
    root.mainloop()
"""

if __name__ == "__main__":
    simulation = Simulation()
    letters = ('Dup','Dright','Ddown','Dleft','Daxis')
    colors = "GCYR"
    for i in range(5):
        simulation.add_walker(Walker(letters[i], color= colors[1]))
    simulation.add_barrier(Barrier((0,10), 5, 0))
    simulation.add_portal(Portal((5,12),2.3))
    simulation.add_portal(Portal((-5,12),2.3))
    simulation.add_mud(Mud((-3,-4),6,3))

    simulation.plot_simulation(100)
    #simulation.simulation_average(5,500,10**5,"results.json")
    print("Done")
