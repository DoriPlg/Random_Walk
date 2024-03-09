"""
FILE : simulation.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: A class for the whole of the simulation
STUDENTS I DISCUSSED THE EXERCISE WITH: 
WEB PAGES I USED:
NOTES: ...
"""

from copy import deepcopy
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
        Once a walker is added it can't be terminated!
        :param walker: the Walker to add
        """
        self.__walkers.append(walker)
        self.__location_log[len(self.__location_log)] = []

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
        for index, walker in enumerate(self.__walkers):
            current_place = walker.get_location()
            self.__location_log[index].append(current_place)
            next_place = walker.next_location()
            for barrier in self.__barriers:
                if barrier.intersects(current_place, next_place):
                    print(f"hit barrier on {self.__iteration}th iteration")
                    next_place = current_place
            for portal in self.__portals:
                if portal.inbounds(next_place):
                    print(f"passed through portal on {self.__iteration}th iteration")
                    next_place = portal.get_end()
            walker.jump(next_place)

        self.__iteration += 1
        return self.__iteration

    def get_log(self):
        """
        returns the location log of a specific simulation
        """
        return self.__location_log
    
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
        stunt_double = deepcopy(self)
        info_dict = {}
        for index, _ in enumerate(self.__walkers):
            info_dict[index] = {"crosses": 0, "escape": None}

        step = 1
        while (step < max_depth and
                None in [info_dict[index]["escape"] for index,_ in enumerate(self.__walkers)])\
              or step < n:
            step = stunt_double.step()
            for index, _ in enumerate(self.__walkers):
                if stunt_double.get_log()[index][-1][0] ** 2 + \
                      stunt_double.get_log()[index][-1][1] ** 2 > 10 ** 2 \
                    and info_dict[index]["escape"] is None:
                    info_dict[index]["escape"] = step

        for index, _ in enumerate(self.__walkers):
            locations = list(stunt_double.get_log()[index][:n])
            info_dict[index]["distance_0"] = \
                (locations[-1][0] ** 2 + locations[-1][1] ** 2) ** (1/2)
            x_values = [x[0] for x in locations]
            info_dict[index]["distance_axis"] = (locations[-1][0],
                                                  locations[-1][1])
            info_dict[index]["crosses"] = helper_functions.passes_0(x_values)
            print(locations, index)
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
        data_for_all_walkers = {}
        distance_0 = {}
        escape = {}
        distance_x_axis = {}
        distance_y_axis = {}
        crosses = {}

        for index, _ in enumerate(self.__walkers):
            distance_0[index] =[]
            escape[index] = []
            distance_x_axis[index] = []
            distance_y_axis[index] = []
            crosses[index] = []

        for _ in range(iterations):
            simulation_results = self.run_simulation(n,max_depth)
            for index, _ in enumerate(self.__walkers):
                distance_0[index].append(simulation_results[index]["distance_0"])
                escape[index].append(simulation_results[index]["escape"])
                distance_x_axis[index].append(simulation_results[index]["distance_axis"][0])
                distance_y_axis[index].append(simulation_results[index]["distance_axis"][1])
                crosses[index].append(simulation_results[index]["crosses"])

        for index, _ in enumerate(self.__walkers):
            dict_to_save = {
                            "distance_0": sum(distance_0[index])/iterations,
                            "escape": sum([number for number in escape[index] if number is not None])/
                            iterations,
                            "distance_axis": (sum(distance_x_axis[index])/iterations,
                                            sum(distance_y_axis[index])/iterations),
                            "crosses": sum(crosses[index])/iterations
                            }
            data_for_all_walkers[index] = dict_to_save
        
        helper_functions.save_to_json(data_for_all_walkers, path)
