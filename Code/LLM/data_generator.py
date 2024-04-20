import random
import math
import string
from Code.helper_functions import save_to_json
from Code.walker import COLORS, MOVEMENTS

def data_for_simulation(
        num_walkers: int, num_barriers: int, num_portals: int, num_mudspots: int) -> dict:
    """
    This function generates data for the graphing of the simulation.
    """
    data = {"Walkers": [], "Barriers": [], "Portals": [], "Mudspots": []}
    for _ in range(num_walkers):
        data["Walkers"].append({"movement": random.choice([key for key in MOVEMENTS.keys()]),
                                "color": random.choice(COLORS),
                                "location": (random.uniform(-100, 100), random.uniform(-100, 100))})
    for _ in range(num_barriers):
        data["Barriers"].append({"center": (random.uniform(-100, 100), random.uniform(-100, 100)),
                                 "length": random.uniform(0, 50),
                                 "angle": random.uniform(0, 2 * math.pi)})
    for _ in range(num_portals):
        data["Portals"].append({"center": (random.uniform(-100, 100), random.uniform(-100, 100)),
                                "radius": random.uniform(0, 10),
                                "endpoint": (random.uniform(-100, 100), random.uniform(-100, 100))})
    for _ in range(num_mudspots):
        data["Mudspots"].append({"bottom_left": (random.uniform(-100, 100), random.uniform(-100, 100)),
                                 "height": random.uniform(0, 50),
                                 "width": random.uniform(0, 50)})
    return data

def simulation_variables() -> tuple[dict,dict]:
    """
    This function generates the variables for the simulation.
    """
    letters = string.ascii_lowercase
    filename = ''.join(random.choice(letters) for i in range(6))
    iterations = random.randint(1, 10)
    buffer = random.randint(1, 100)
    n = random.randint(1, 1000)
    steps = random.randint(3, 14)
    graphing_data = {"type": "graph",
                    "iterations": iterations,
                    "max_depth": n+buffer,
                    "n": n,
                    "steps": n/14,
                    "filename": f"./{filename}"}
    plottings_data = {"type": "plot",
                      "n": n,
                      "filename": f"./{filename}"}
    return graphing_data, plottings_data

def generate_data(size) -> dict:
    """
    This function generates data for the simulation.
    """
    great_big_data = {}
    for i in range(0,size,2):
        graphing_data, plottings_data = simulation_variables()
        data = data_for_simulation(random.randint(1, 7), random.randint(1, 7),
                                   random.randint(1, 7), random.randint(1, 7))
        great_big_data[i] = data
        great_big_data[i]["Simulation"] = graphing_data
        great_big_data[i+1] = data
        great_big_data[i+1]["Simulation"] = plottings_data
    return great_big_data

def save_data(size: int, filename: str = "data.json") -> None:
    """
    This function saves the data to a JSON file.
    """
    save_to_json(generate_data(size=size), filename)

