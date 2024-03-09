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
    for _ in range(5):
        simulation.add_walker(Walker('C'))
    simulation.add_barrier(Barrier((0,7),6,0))
    simulation.add_portal(Portal((4,3),2.5))
    simulation.simulation_average(1,100,10**5,
                                  "/home/dori/Documents/UNI/Intro/final_project/Results/results.json")
    #simulation.simulation_average(6,100,10*5,
    #                              "/home/dori/Documents/UNI/Intro/final_project/Results/results1")
    print("Done")
