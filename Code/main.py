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
    colors = "GCYR"
    for i in range(4):
        simulation.add_walker(Walker(letters[i], color= colors[i]))
    simulation.add_barrier(Barrier((0,10), 5, 0))
    simulation.add_portal(Portal((5,12),2.3))
    simulation.add_portal(Portal((-5,12),2.3))
    # simulation.add_portal(Portal((6,5),4, (-3,-2)))
    
    simulation.plot_simulation(500)
    #simulation.simulation_average(5,500,10**5,"results.json")
    print("Done")
