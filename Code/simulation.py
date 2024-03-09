"""
FILE : simulation.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: A class for the whole of the simulation
STUDENTS I DISCUSSED THE EXERCISE WITH: 
WEB PAGES I USED:
NOTES: ...
"""

from typing import Tuple
from walker import Walker, pull_push
from barrier import Barrier
from portal import Portal
import helper_functions

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

    def __step(self) -> int:
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

    def run_simulation(self,n: int, max_depth: int = 10**3) -> dict:
        """
        runs a single simulation and returns a dictionary where we have for each walker:
        {
            "distance_0": the distance from (0,0) after N steps
            "escape": the amount of steps it took the each walker to leave
                     the 10 unit circle around (0,0)
            "distance_axis": average distance from the x and y axis after N steps 
                                rep. as (distance_x, distance_y)
            "crosses": number of crosses of y axis
        }
        :param n: the N for which the values will be calculated
        "param max_depth: the greatest number of runs the simulation will allow.
        """
        info_dict = {}
        for walker in self.__walkers:
            step = 1
            info_dict[walker] = {"crosses": 0, "escape": None}
        while (step < max_depth or
                None not in [info_dict[walker]["escape"] for walker in self.__walkers])\
              and step < n:
            step = self.__step()
            for walker in self.__walkers:
                if walker.get_location()[0] ** 2 + walker.get_location()[1] ** 2 == 10 ** 2:
                    info_dict[walker]["escape"] = step
                if self.__location_log[walker][-2] * self.__location_log[walker][-1] < 0:
                    info_dict[walker]["crosses"] += 1
        for walker in self.__walkers:
            locations = [loc for loc in self.__location_log[walker][:n]]
            distances_from_0 = [(location[0] ** 2 + location[1] ** 2) for location in locations]
            info_dict[walker]["distance_0"] = sum(distances_from_0)/len(distances_from_0)
            info_dict[walker]["distance_axis"] = (sum([x[0] for x in locations]) / len(locations),
                                                  sum([x[1] for x in locations]) / len(locations))
        return info_dict

    def simulation_average(self, iterations: int, n: int, max_depth: int, path: str) -> None:
        """
        runs multiple simulations and saves a json with their average outcome for:
        {
            "distance_0": the distance from (0,0) after N steps
            "escape": the amount of steps it took the each walker to leave
                     the 10 unit circle around (0,0)
            "distance_axis": average distance from the x and y axis after N steps 
                                rep. as (distance_x, distance_y)
            "crosses": number of crosses of y axis
        } 
        Note that if the simulation contains multiple walkers, 
        it will average the results for each walker, allowing you to compare
        :param iteration: the number of times the simulation will be repeated
        :param n: the number for which the results will be checked
        :param max_depth: the most iterations before we give up on a walker escaping the circle
        :param path: the desired loction where to save the results
        """
        distance_0 =[]
        escape = []
        distance_x_axis = []
        distance_y_axis = []
        crosses = []

        for _ in range(iterations):
            simulation_results = self.run_simulation(n,max_depth)
            distance_0.append(simulation_results["distance_0"])
            escape.append(simulation_results["escape"])
            distance_x_axis.append(simulation_results["distance_axis"][0])
            distance_y_axis.append(simulation_results["distance_axis"][1])
            crosses.append(simulation_results["crosses"])

        dict_to_save = {
                            "distance_0": sum(distance_0)/iterations,
                            "escape": sum(escape)/iterations,
                            "distance_axis": (sum(distance_x_axis)/iterations,
                                              sum(distance_y_axis)/iterations),
                            "crosses": sum(crosses)/iterations
                        }
        
        helper_functions.save_to_json(dict_to_save, path)
