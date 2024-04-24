"""
FILE : simulation.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: A class for the whole of the simulation
STUDENTS I DISCUSSED THE EXERCISE WITH: 
WEB PAGES I USED:
NOTES: ...
"""

import os
from copy import deepcopy
from typing import Tuple, Optional
from Code.walker import Walker, gravitate
from Code.barrier import Barrier
from Code.portal import Portal
from Code.mud import Mud
import Code.helper_functions as helper
import Code.graph as gr

Coordinates = Tuple[float,float]

# The radius we check if a walker escapes
ESCAPE_RAD = 10
# The path prefix to any file I save
DESTINATION_PATH = "./Results/"

class Simulation:
    """
    A class for Simulation objects for random walker simulations.
    :attribute __walkers: a list containg all walkers added to the simulation by order
    :attribute __location_log: a dictionary where the keys are the indexes of different 
                                walkers in __walker and the values are lists in order of
                                the locations the walker visited.
    :attribute __barriers: a list containg all barriers added to the simulation by order
    :attribute __portals: a list containg all portals added to the simulation by order
    :attribute __iteration: counts the iterations of the simulation
    """

    def __init__(self, gravity = 0) -> None:
        """
        The constructor for Simulation objects
        """
        self.__walkers: list[Walker] = []
        self.__location_log: dict[int, list[Coordinates]] = {}
        self.__barriers: list[Barrier]= []
        self.__portals: list[Portal] = []
        self.__mudspots: list[Mud] = []
        self.__iteration = 0
        gravity_values = (-1,0,1)
        if gravity not in gravity_values:
            raise ValueError(f"Gravity can only be {gravity_values}")
        self.__gravity = gravity

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

    def add_mud(self, mud: Mud) -> None:
        """
        Adds mud to the simulation
        :param mus: The mud to add
        """
        self.__mudspots.append(mud)

    def step(self) -> int:
        """
        Preforms one step of the entire simulation.
        Returns the number of the step preformed.
        """
        MAX_BARRIER_HITS = 10**3
        for index, walker in enumerate(self.__walkers):
            current_place = walker.location
            self.__location_log[index].append(current_place)
            next_place = walker.next_location()
            if next_place:
                for barrier in self.__barriers:
                    barrier_hit = 0
                    while barrier.intersects(current_place, next_place):
                        #print(f"hit barrier on {self.__iteration}th iteration")
                        next_place = walker.next_location()
                        barrier_hit += 1
                        if barrier_hit > MAX_BARRIER_HITS:
                            raise helper.SimulationError(
                                "\nThe walker is stuck in a barrier, please change the simulation")
                for mud in self.__mudspots:
                    if mud.point_in_area(current_place):
                        next_place = (current_place[0] +
                                    (next_place[0] - current_place[0]) * mud.get_lag(),
                                    current_place[1] +
                                    (next_place[1] - current_place[1]) * mud.get_lag())
                for portal in self.__portals:
                    if portal.inbounds(next_place):
                        #print(f"passed through portal on {self.__iteration}th iteration")
                        next_place = portal.endpoint
                walker.jump(next_place)
            else:
                raise AttributeError(
                    "The walker has no next location, due to having bad type of movement")
        gravitate(self.__walkers, gravity=self.__gravity)

        self.__iteration += 1
        return self.__iteration

    @property
    def log(self):
        """
        returns the location log of a specific simulation
        """
        return self.__location_log

    def run_simulation(self,n: int, steps:int, max_depth: int = 10**3) -> dict:
        """
        runs a single simulation and returns a dictionary where we have for each walker:
        {
            "distance_0": the distance from (0,0) after N steps
            "escape": the amount of steps it took the each walker to leave
                     the 10 unit circle around (0,0)
            "distance_axis": average distance from the y axis after N steps 
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
        info_dict: dict[int,dict[int, dict[str, object]]] = {}
        escape: dict[int, Optional[int]] = {}
        for index, _ in enumerate(self.__walkers):
            info_dict[index] = {1: {"escape": None}}
            escape[index] = None
        step = 0
        # Runs through the steps, checking when ESCAPE_RAD is escaped
        while (step < max_depth + 1 and
                None in [info_dict[index][max(info_dict[index].keys())]["escape"]\
                          for index,_ in enumerate(self.__walkers)])\
              or step < n + 1:
            step = stunt_double.step()
            for index, _ in enumerate(self.__walkers):
                if stunt_double.log[index][-1][0] ** 2 + \
                        stunt_double.log[index][-1][1] ** 2 > ESCAPE_RAD ** 2 \
                        and escape[index] is None:
                    escape[index] = step
                if step in range(1, n+1, steps):
                    info_dict[index][step] = {"escape": escape[index]}

        # Runs through the locations the simulation passed through and gets the desired answers
        for index, _ in enumerate(self.__walkers):
            self.__location_log[index].append(self.__walkers[index].location)
            locations = list(stunt_double.log[index][:n+1])
            for i in range(1, n + 1, steps):
                info_dict[index][i]["distance_0"] = \
                    (locations[:i][-1][0] ** 2 + locations[:i][-1][1] ** 2) ** (1/2)
                x_values = [x[0] for x in locations[:i]]
                info_dict[index][i]["distance_axis"] = abs(locations[:i][-1][0])
                info_dict[index][i]["crosses"] = helper.passes_0(x_values)
                info_dict[index][i]["location_list"] = locations[:i]

        return info_dict

    def simulation_average(self, iterations: int, n: int, step: int, max_depth: int) -> dict:
        """
        runs multiple simulations and saves a json with their average outcome for:
        {
            "distance_0": the distance from (0,0) after N steps
            "escape": the amount of steps it took the each walker to leave
                     the 10 unit circle around (0,0)
            "distance_axis": average distance from the y axis after N steps 
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
        data_for_all_walkers: dict[int,dict[int, dict[str, float]]] = {}
        distance_0: dict[int, dict[int, list[float]]] = {}
        escape: dict[int, dict[int, list[int]]] = {}
        distance_x_axis: dict[int, dict[int, list[float]]] = {}
        distance_y_axis: dict[int, dict[int, list[float]]] = {}
        crosses: dict[int, dict[int, list[int]]] = {}

        # "Zero"s the values for each walker
        for index, _ in enumerate(self.__walkers):
            distance_0[index] = {}
            escape[index] = {}
            distance_x_axis[index] = {}
            distance_y_axis[index] = {}
            crosses[index] = {}
            for i in range(1, n + 1, step):
                distance_0[index][i] = []
                escape[index][i] = []
                distance_x_axis[index][i] = []
                distance_y_axis[index][i] = []
                crosses[index][i] = []

        # Preforms the desired iterations of the simulation
        for _ in range(iterations):
            simulation_results = self.run_simulation(n,step,max_depth)
            for index, _ in enumerate(self.__walkers):
                for i in range(1, n + 1, step):
                    distance_0[index][i].append(simulation_results[index][i]["distance_0"])
                    escape[index][i].append(simulation_results[index][i]["escape"])
                    distance_y_axis[index][i].append(simulation_results[index][i]["distance_axis"])
                    crosses[index][i].append(simulation_results[index][i]["crosses"])

        # Compresses the data to averages for each walker
        for index, _ in enumerate(self.__walkers):
            data_for_all_walkers[index] = {}
            for i in range(1, n + 1, step):
                dict_to_save = {
                                "distance_0": sum(distance_0[index][i])/iterations,
                                "escape": sum(number for number in escape[index][i]\
                                    if number is not None)/
                                iterations,
                                "distance_axis": sum(distance_y_axis[index][i])/iterations,
                                "crosses": sum(crosses[index][i])/iterations
                                }
                data_for_all_walkers[index][i] = dict_to_save

        # Returns the data constructed
        return data_for_all_walkers

    def graph_simulation(self, iterations: int, n: int,
                          max_depth: int, step: int, file_name: str) -> None:
        """
        Perform a graph simulation.

        Parameters:
        - iterations (int): The number of iterations to perform.
        - n (int): The maximum value for the range.
        - max_depth (int): The maximum depth for the simulation.
        - step (int): The step size for the range.
        - file_name (str): The name of the file to save the graph.

        Returns:
        None
        """

        data_for_graph = self.simulation_average(iterations, n, step, max_depth)
        helper.save_to_json(data_for_graph, f"{file_name}_results.json")
        gr.show_walker_graph(data_for_graph, file_name)

    def plot_simulation(self, n: int, file_name: str = f"{DESTINATION_PATH}walkerplot") -> None:
        """
        Runs the simulation independently of the simulation_average method.
        Saves to the destination folder graphs of the locations visited by the walker
        :param n: the N for which the values will be calculated
        :param file_name: the first part of the filename for the graph, *.png will
                            be added automaticaly. an index discerning which walker is 
                            shown will be added defaults to 'walkerplot'
        """
        simulation_results = self.run_simulation(n,n-1,n)
        locations_dict = {item[0]: item[1][n]["location_list"]
                           for item in simulation_results.items()}
        barriers = [barrier.points for barrier in self.__barriers]
        portals = [(portal.center, portal.radius, portal.endpoint) \
                    for portal in self.__portals]
        mudspots = [mud.properties for mud in self.__mudspots]
        color_list = [walker.color for walker in self.__walkers]
        obstacles = (barriers, portals, mudspots)
        for index, locations in locations_dict.items():
            graph_name = f"Graph number {index + 1}, \
showing a walker with {self.__walkers[index].movement} type movement"
            gr.show_walker_way(graph_name,locations, obstacles,
                                   f"{file_name}_{index}", color_list[index])
        graph_name = f"Graph number {len(color_list) + 1}, showing all walkers in unision"
        gr.walkers_unision(graph_name, locations_dict,
                           color_list=color_list,obstacles=obstacles, file_to_save=file_name+"_all")

def check_data(data: dict) -> bool:
    """
    checks if the data is valid for a simulation
    :param data: the data to check
    """
    keys = ['Walkers', 'Barriers', 'Portals', 'Mudspots', 'Simulation']

    if not isinstance(data, dict):
        raise TypeError("Data must be a dictionary")
    elif len(data) == 0:
        raise AttributeError("Empty data was given for the simulation")

    if [key for key in data.keys()] == keys:
        if data["Simulation"]["type"] in ("plot", "graph"):
            try:
                for walker in data["Walkers"]:
                    Walker(**walker)
                for barrier in data["Barriers"]:
                    Barrier(**barrier)
                for portal in data["Portals"]:
                    Portal(**portal)
                for mudspot in data["Mudspots"]:
                    Mud(**mudspot)
                int(data["Simulation"]["n"])
                if data["Simulation"]["type"] == "graph":
                    int(data["Simulation"]["iterations"])
                    int(data["Simulation"]["max_depth"])
                    int(data["Simulation"]["steps"])

                if "gravity" in data["Simulation"]:
                    if isinstance(data["Simulation"]["gravity"],int):
                        Simulation(data["Simulation"]["gravity"])
                    else:
                        raise ValueError("Something wrong with the gravity type")

                #check if the filename leads to a valid path
                split_path = data["Simulation"]["filename"].split("/")
                directory = "/".join(split_path[:-1])
                if directory == "":
                    directory = "."
                if os.path.exists(directory):
                    return True
            except Exception as e:
                print("Exception", e)
    return False

def run_from_json(filename: Optional[str] = None) -> Tuple[dict, str]:
    """
    loads a simulation from a json file and runs the desired simulation
    :param filename: the path to the json

    returns the base path to the file saved
    """
    if not filename or not os.path.exists(filename):
        filename = helper.get_filepath_to_json()
    if not filename.endswith('_simulation.json'):
        raise ValueError("Simulation filename must end with '_simulation.json'")
    data = helper.load_simulation(filename)
    filename = filename.removesuffix("_simulation.json")
    data["Simulation"]["filename"] = filename
    if not check_data(data):
        print("The data in the file is not valid for a simulation")
        raise ValueError("The data in the file is not valid for a simulation")
    else:
        print("The data is valid")
    return data, filename

def run_and_plot(data: dict, filename: str) -> str:
    """
    runs the simulation from the data given
    """
    if "gravity" in data["Simulation"]:
        simulation = Simulation(data["Simulation"]["gravity"])
    else:
        simulation = Simulation()
    for walker in data["Walkers"]:
        simulation.add_walker(Walker(**walker))
    for barrier in data["Barriers"]:
        simulation.add_barrier(Barrier(**barrier))
    for portal in data["Portals"]:
        simulation.add_portal(Portal(**portal))
    for mudspot in data["Mudspots"]:
        simulation.add_mud(Mud(**mudspot))
    if data["Simulation"]["type"] == "plot":
        n, filename = data["Simulation"]["n"], data["Simulation"]["filename"]
        simulation.plot_simulation(n, filename)
    elif data["Simulation"]["type"] == "graph":
        iterations = data["Simulation"]["iterations"]
        n = data["Simulation"]["n"]
        max_depth = data["Simulation"]["max_depth"]
        step = data["Simulation"]["steps"]
        file_name = data["Simulation"]["filename"]
        simulation.graph_simulation(iterations, n, max_depth, step, file_name)

    return filename.removesuffix("_simulation.json")

