"""
FILE : walker_3d.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: A class for the walker object
STUDENTS I DISCUSSED THE EXERCISE WITH: None
WEB PAGES I USED:
NOTES: ...
"""

from typing import Tuple
import math
import random

Triordinates = Tuple[float, float, float]
COLORS = ["red", "green", "yellow", "blue", "cyan", "orange","brown", "purple","olive"]
PI = math.pi

class Walker3D:
    def __init__(self, position: Triordinates):
        self.__position = position
        self.__log: list[Triordinates] = []

    @property
    def position(self) -> Triordinates:
        return self.__position
    
    @property
    def log(self) -> list:
        return self.__log

    def next_location(self) -> Triordinates:
        x, y, z = self.position
        dx, dy, dz = random_vector()
        return x + dx, y + dy, z + dz

    def jump(self, location: Triordinates):
        self.__log.append(self.position)
        self.__position = (location)

    def get_distance(self, location: Triordinates) -> float:
        x1, y1, z1 = self.position
        x2, y2, z2 = location
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
        return distance

    def __str__(self):
        return f"Walker3D at position {self.__position}"
    
def random_vector() -> Triordinates:
    """
    A function that returns a random vector in 3D space, with a length of 1 unit
    """
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    z = random.uniform(-1, 1)
    length = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    return x / length, y / length, z / length

def gravitate(walkers: list[Walker3D], degree: int = 2, gravity: int = 0) -> None:
    """
    A function that applies gravity to a list of walkers in 3D space.
    :param walkers: a list of Walker3D objects
    :param degree: an integer representing the degree of gravity, defaults to 5
    :param gravity: an integer representing the direction of gravity, defaults to 0
    """
    if len(walkers) <= 1 or gravity == 0:
        return
    nonrelative_locations = {}
    ratio  = float(degree * len(walkers) * (gravity))
    for walker in walkers:
        bearing: tuple[float, float, float] = (0.0, 0.0, 0.0)
        for other_walker in walkers:
            if other_walker is walker:
                continue
            x_difference = other_walker.position[0] - walker.position[0]
            y_difference = other_walker.position[1] - walker.position[1]
            z_difference = other_walker.position[2] - walker.position[2]
            distance_squared = x_difference ** 2 + y_difference ** 2 + z_difference ** 2

            #to avoid too strong attraction (wormholes and such)
            if distance_squared == 0:
                continue
            attraction = min((ratio) / (distance_squared), 3)

            direction = (x_difference / math.sqrt(distance_squared),
                         y_difference / math.sqrt(distance_squared),
                         z_difference / math.sqrt(distance_squared))
            bearing = (direction[0] * attraction,
                        direction[1] * attraction,
                        direction[2] * attraction)

        nonrelative_locations[walker] = (walker.position[0] + bearing[0],
                                         walker.position[1] + bearing[1],
                                         walker.position[2] + bearing[2])

    for walker in walkers:
        walker.jump(nonrelative_locations[walker])
