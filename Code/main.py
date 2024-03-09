"""
FILE : main.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: The page where the whole program will run
STUDENTS I DISCUSSED THE EXERCISE WITH: 
WEB PAGES I USED:
NOTES: ...
"""

from walker import Walker, get_move_dict
from barrier import Barrier
from portal import Portal
from simulation import Simulation


if __name__ == "__main__":
    simulation = Simulation()
    letters = "ABCD"
    for i in range(4):
        simulation.add_walker(Walker(letters[i]))

    simulation.plot_simulation(100)
    simulation.simulation_average(10,1000,10**5,"results.json")
    print("Done")
