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
    walk = Walker('A')
    simulation = Simulation()
    simulation.add_walker(walk)
    simulation.simulation_average(1,50,10*5,
                                  "/home/dori/Documents/UNI/Intro/final_project/Results")
    print("Done")