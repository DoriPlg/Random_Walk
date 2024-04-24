
"""
This module contains functions for generating and manipulating data for a simulation at random.
"""

import random
import math
import string
from typing import Any
from Code.walker import COLORS, MOVEMENTS
from Code.helper_functions import save_to_json

def data_for_simulation(
        num_walkers: int, num_barriers: int, num_portals: int, num_mudspots: int) -> dict:
    """
    This function generates data for the graphing of the simulation.
    """
    data: dict[str, Any]
    data = {"Walkers": [], "Barriers": [], "Portals": [], "Mudspots": []}
    for _ in range(num_walkers):
        data["Walkers"].append({"movement": random.choice([key for key in MOVEMENTS.keys()]),
                                "color": random.choice(COLORS),
                                "location": (round(random.uniform(-100, 100),2), round(random.uniform(-100, 100),2))})
    for _ in range(num_barriers):
        data["Barriers"].append({"center": (round(random.uniform(-100, 100),2), round(random.uniform(-100, 100),2)),
                                 "length": round(random.uniform(0.1, 50),2),
                                 "angle": round(random.uniform(0, 2 * math.pi),4)})
    for _ in range(num_portals):
        data["Portals"].append({"center": (round(random.uniform(-100, 100),2), round(random.uniform(-100, 100),2)),
                                "radius": round(random.uniform(0.1, 10),2),
                                "endpoint": (round(random.uniform(-100, 100),2), round(random.uniform(-100, 100),2))})
    for _ in range(num_mudspots):
        data["Mudspots"].append({"bottom_left": (round(random.uniform(-100, 100),2), round(random.uniform(-100, 100),2)),
                                 "height": round(random.uniform(0.1, 50),2),
                                 "width": round(random.uniform(0.1, 50),2)})
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
    reset = random.randint(1, 100)
    gravity = random.choice([1, 0, -1])
    graphing_data = {"type": "graph",
                    "iterations": iterations,
                    "max_depth": n+buffer,
                    "n": n,
                    "steps": n/steps,
                    "gravity": gravity,
                    "reset": reset,
                    "filename": f"./Results/{filename}"}
    plottings_data = {"type": "plot",
                    "n": n,
                    "gravity": gravity,
                    "reset": reset,
                    "filename": f"./Results/{filename}"}
    return graphing_data, plottings_data

def generate_data() -> tuple[dict, dict]:
    """
    This function generates data for the simulation.
    """
    graphing_data, plottings_data = simulation_variables()
    data = data_for_simulation(random.randint(1, 7), random.randint(0, 5),
                                random.randint(0, 5), random.randint(0, 5))
    graphing, plotting = data, data.copy()
    graphing["Simulation"] = graphing_data
    plotting["Simulation"] = plottings_data
    return (graphing, plotting)

def save_json(data: dict) -> None:
    """
    This function saves the data to a JSON file.
    """
    path = data["Simulation"]["filename"] + "_simulation.json"
    save_to_json(data, path)
