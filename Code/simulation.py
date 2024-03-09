"""
FILE : simulation.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: A clss for the whole of the simulation
STUDENTS I DISCUSSED THE EXERCISE WITH: 
WEB PAGES I USED:
NOTES: ...
"""

from typing import Tuple
from walker import Walker, get_move_dict, pull_push
from barrier import Barrier
from portal import Portal

Coordinates = Tuple[float,float]

class Simulation:
    """
    A class for Simulation objects for random walker simulations.
    :attribute __walkers: a list containg all walkers added to the simulation by order
    :attribute __location_log: a dictionary where the keys are the indexes of different walkers in __walker
                                and the values are lists in order of the locations the walker visited.
    :attribute __barriers: a list containg all barriers added to the simulation by order
    :attribute __portals: a list containg all portals added to the simulation by order
    :attribute __iteration: counts the iterations of the simulation
    """

    def __init__(self) -> None:
        """
        The constructor for Simulation objects
        """
        self.__walkers = []
        self.__location_log = {}
        self.__barriers = []
        self.__portals = []
        self.__iteration = 0

    def add_walker(self, walker: Walker) -> None:
        """
        Adds a walker to the simulation
        Once a walker is added may only be terminated!
        :param walker: the Walker to add
        """
        self.__walkers.append(walker)
        self.__location_log[walker] = []

    def __terminate_walker(self, index: int) -> None:
        """
        If you wish to terminate a walker. All log data will remain.
        Notice: once terminated the walker will not return to move, ever.
        :param index: the index for the exact walker you wish to remove
        """
        del self.__walkers[index]

    def add_portal(self, portal: Portal) ->None:
        """"
        Adds a portal to the simulation
        :param portal: The portal to add
        """
        self.__portals.append(portal)

    def add_barrier(self, barrier: Barrier) ->None:
        """"
        Adds a barrier to the simulation
        :param barrier: The barrier to add
        """
        self.__barriers.append(barrier)

    def step(self) -> int:
        """
        Preforms one step of the entire simulation.
        Returns the number of the step preformed.
        """
        for walker in self.__walkers:
            current_place = walker.get_location()
            self.__location_log[walker].append(current_place)
            next_place = walker.next_location()
            for barrier in self.__barriers:
                if barrier.intersects(current_place, next_place):
                    next_place = current_place
            for portal in self.__portals:
                if portal.inbounds(next_place):
                    next_place = portal.get_end()
            walker.jump(next_place)

        self.__iteration += 1
        return self.__iteration
