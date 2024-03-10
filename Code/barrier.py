"""
FILE : barrier.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: A calss for barrier objects within a simulation
STUDENTS I DISCUSSED THE EXERCISE WITH:
WEB PAGES I USED:
NOTES: ...
"""
from typing import Tuple
import math

Coordinates = Tuple[float,float]

class Barrier:
    """
    A class building the barrier object in the random walker simulation
    Borders are straight lines which the walker can't pass to either way.
    """

    def __init__(self, center: Coordinates, length: float, angle: float) -> None:
        """
        A constructor for a new Barrier object
        :param center: the centerpoint of the Barrier.
        :param length: the length of the barrier.
        :param angle: the angle in which the barrier is set.
        """
        if length <= 0:
            raise ValueError("Length must be a positive number")
        
        # Takes the input and sets the object attributes to be two points
        # between which the barrier is stretched
        self.__point1 = (center[0] + (math.cos(angle) * length / 2),
                         center[1] + (math.sin(angle) * length / 2))
        self.__point2 = (center[0] - (math.cos(angle) * length / 2),
                         center[1] - (math.sin(angle) * length / 2))

    def intersects(self, point_a: Coordinates, point_b: Coordinates) -> bool:
        """
        A function to check wether a movement between two points crosses the Barrier
        True if crosses,  False if doesn't
        :param point_a: the first point.
        :param point_b: the second point.
        """
        barrier_function = self.get_function(self.__point1,self.__point2)
        line_function = self.get_function(point_a,point_b)
        if line_function[0] == barrier_function[0] or line_function == barrier_function:
            # line paralel to barrier
            return False
        if line_function == "vertical":
            # line vertical, relies only on it's x value and y span
            intersection_y = barrier_function[0] * point_a[0] + barrier_function[1]
            return min(point_a[1],point_b[1]) <= intersection_y \
                 <= max(point_a[1],point_b[1])
        elif barrier_function == "vertical":
            intersection_y = line_function[0] * self.__point1[0] + line_function[1]
            return min(self.__point1[1],self.__point2[1]) <= intersection_y \
                 <= max(self.__point1[1],self.__point2[1])
        intersection_x = ((barrier_function[1] - line_function[1]) /
                           (line_function[0] - barrier_function[0]))
        return min(self.__point1[0],self.__point2[0]) <= intersection_x <= max(self.__point1[0],self.__point2[0])

    @property
    def points(self) -> tuple[Coordinates,Coordinates]:
        """
        returns the points between which a barrier is strung
        """
        return (self.__point1,self.__point2)

    @staticmethod
    def get_function(a, b) -> Tuple[float, float] | str:
        """
        recieves two points and returns a tuple containing the ratio between them and
        the additional part to add to offset from the x axis as a tuple: (ratio, aditional)
        :param a: the first point in the comparison
        :param b: the second point in the comparison
        """
        if a[0] - b[0] == 0:
            return "vertical"
        ratio = (a[1] - b[1]) / (a[0] - b[0])
        additional = a[1] - ratio * a[0]
        return (ratio, additional)
