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
from walker_gui import SimulationGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationGUI(root)
    root.mainloop()



if __name__ == "__min__":
    simulation = Simulation()
    letters = ('Dup','Dright','Ddown','Dleft','Daxis')
    colors = "GCYRP"
    for i in range(5):
        simulation.add_walker(Walker(letters[4], color= colors[i]))
    simulation.add_barrier(Barrier((0,10), 5, 0))
    simulation.add_portal(Portal((5,12),2.3))
    simulation.add_portal(Portal((-5,12),2.3))
    simulation.add_mud(Mud((-3,-4),6,3))

    simulation.plot_simulation(100)
    simulation.simulation_average(5,500,10**5)
    input("Done")
