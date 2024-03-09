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
import graph

Coordinates = Tuple[float,float]

# The radius we check if a walker escapes
ESCAPE_RAD = 10
# The path prefix to any file I save
DESTINATION_PATH = "/home/dori/Documents/UNI/Intro/final_project/Results/"

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
            if index == 2:
                print(next_place)
            """ There is a problem here (same problem)"""
            for barrier in self.__barriers:
                while barrier.intersects(current_place, next_place):
                    # print(f"hit barrier on {self.__iteration}th iteration")
                    next_place = walker.next_location()
            for portal in self.__portals:
                if portal.inbounds(next_place):
                    # print(f"passed through portal on {self.__iteration}th iteration")
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
            "location_list": an ordered list of coordinates visited by the walker
        }
        :param n: the N for which the values will be calculated
        "param max_depth: the greatest number of runs the simulation will allow.
        """

        # Deals with problematic input
        if n <= 0:
            raise ValueError("The simulation must be set for at least 1 time")
        if max_depth < n:
            raise ValueError("The max depth cannot be lower then the depth to check")

        # "Zero"s the variables
        stunt_double = deepcopy(self)
        info_dict = {}
        for index, _ in enumerate(self.__walkers):
            info_dict[index] = {"crosses": 0, "escape": None}
        step = 0

        # Runs through the steps, checking when ESCAPE_RAD is escaped
        while (step < max_depth + 1 and
                None in [info_dict[index]["escape"] for index,_ in enumerate(self.__walkers)])\
              or step < n + 1:
            step = stunt_double.step()
            for index, _ in enumerate(self.__walkers):
                if stunt_double.get_log()[index][-1][0] ** 2 + \
                      stunt_double.get_log()[index][-1][1] ** 2 > ESCAPE_RAD ** 2 \
                    and info_dict[index]["escape"] is None:
                    info_dict[index]["escape"] = step

        # Runs through the locations the simulation passed through and gets the desired answers
        for index, _ in enumerate(self.__walkers):
            self.__location_log[index].append(self.__walkers[index].get_location())
            locations = list(stunt_double.get_log()[index][:n+1])
            info_dict[index]["distance_0"] = \
                (locations[-1][0] ** 2 + locations[-1][1] ** 2) ** (1/2)
            x_values = [x[0] for x in locations]
            info_dict[index]["distance_axis"] = (abs(locations[-1][0]),
                                                  abs(locations[-1][1]))
            info_dict[index]["crosses"] = helper_functions.passes_0(x_values)
            info_dict[index]["location_list"] = locations

        return info_dict

    def simulation_average(self, iterations: int, n: int, max_depth: int, file_name: str) -> None:
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

        # Checking correct values of input
        if iterations <= 0:
            raise ValueError("The simulation must be set for at least 1 iteration")
        if n <= 0:
            raise ValueError("The simulation must be set for at least 1 time")
        if max_depth < n:
            raise ValueError("The max depth of the simulation cannot be less than the desired one")
        # Prepares dictionaries for the data
        data_for_all_walkers = {}
        distance_0 = {}
        escape = {}
        distance_x_axis = {}
        distance_y_axis = {}
        crosses = {}

        # "Zero"s the values for each walker
        for index, _ in enumerate(self.__walkers):
            distance_0[index] =[]
            escape[index] = []
            distance_x_axis[index] = []
            distance_y_axis[index] = []
            crosses[index] = []

        # Preforms the desired iterations of the simulation
        for _ in range(iterations):
            simulation_results = self.run_simulation(n,max_depth)
            for index, _ in enumerate(self.__walkers):
                distance_0[index].append(simulation_results[index]["distance_0"])
                escape[index].append(simulation_results[index]["escape"])
                distance_x_axis[index].append(simulation_results[index]["distance_axis"][0])
                distance_y_axis[index].append(simulation_results[index]["distance_axis"][1])
                crosses[index].append(simulation_results[index]["crosses"])

        # Compresses the data to averages for each walker
        for index, _ in enumerate(self.__walkers):
            dict_to_save = {
                            "distance_0": sum(distance_0[index])/iterations,
                            "escape": sum(number for number in escape[index]\
                                 if number is not None)/
                            iterations,
                            "distance_axis": (sum(distance_x_axis[index])/iterations,
                                            sum(distance_y_axis[index])/iterations),
                            "crosses": sum(crosses[index])/iterations
                            }
            data_for_all_walkers[index] = dict_to_save

        # Saves the data constructed to the desired path
        helper_functions.save_to_json(data_for_all_walkers, f"{DESTINATION_PATH}{file_name}")

    def plot_simulation(self, n: int, file_name: str = "walkerplot") -> None:
        """
        Runs the simulation independently of the simulation_average method.
        Saves to the destination folder graphs of the locations visited by the walker
        :param n: the N for which the values will be calculated
        :param file_name: the first part of the filename for the graph, *.png will be added automaticaly. 
                            an index discerning which walker is shown will be added
                            defaults to 'walkerplot'
        """
        simulation_results = self.run_simulation(n,n)
        locations_dict = {index: simulation_results[index]["location_list"]
                           for index in simulation_results}
        barriers = [barrier.get_points() for barrier in self.__barriers]
        portals = [(portal.get_center(), portal.get_radius(), portal.get_end()) \
                    for portal in self.__portals]
        for index, locations in locations_dict.items():
            color = self.__walkers[index].get_color()
            if index == 2:
                print(locations)
            """ There is a problem here"""
            graph.show_walker_way(locations, barriers, portals,
                                   DESTINATION_PATH+file_name+str(index), color)
