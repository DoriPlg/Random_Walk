"""
FILE : mud.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: A calss for mud objects within a simulation
STUDENTS I DISCUSSED THE EXERCISE WITH:
WEB PAGES I USED:
NOTES: ...
"""

from typing import Tuple

Coordinates = Tuple[float,float]

SLOWDOWN = 0.6


class Mud:
    """
    A class building the mud object in the random walker simulation
    Mud pathces are rectangular areas where the movement of the walker is slowed down
    """


    def __init__(self, bottom_left: Coordinates, width: float, height: float) -> None:
        """
        initiates a new mudpatch object.
        :param bottom_left: the mudpatch bottom left corner
        :param width: the width of the mudpatch
        :param height: the height of the mudpatch
        """
        self.__bottom_left = bottom_left
        if width <= 0 or height <= 0:
            raise ValueError("The width and height can only be positive")
        self.__width = width
        self.__height = height

    def point_in_area(self, point: Coordinates) -> bool:
        """
        Checks wether a location is in the patch
        :param point: the location to check
        """
        return (self.__bottom_left[0] <= point[0] <= (self.__bottom_left[0] + self.__width) and \
                self.__bottom_left[1] <= point[1] <= (self.__bottom_left[1] + self.__height))

    @property
    def properties(self) -> Tuple[Coordinates, float, float]:
        """
        gets a tuple of the properties of the patch
        (bottom_left, width, height)
        """
        return (self.__bottom_left, self.__width, self.__height)
    
    @staticmethod
    def get_lag() -> float:
        """
        gets the slow down buffer of the mud patch
        """
        return SLOWDOWN
