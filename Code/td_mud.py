"""
FILE : mud_3d.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: A class for 3D mud objects within a simulation
STUDENTS I DISCUSSED THE EXERCISE WITH:
WEB PAGES I USED:
NOTES: ...
"""

from typing import Tuple

Triordinates = Tuple[float, float, float]

SLOWDOWN = 0.6


class MudPatch3D:
    """
    A class building the mud object in the random walker simulation
    Mud pathces are cubical areas where the movement of the walker is slowed down
    """


    def __init__(self, bottom_left: Triordinates, width: float, height: float, depth: float) -> None:
        """
        initiates a new mudpatch object.
        :param bottom_left: the mudpatch bottom left corner
        :param width: the width of the mudpatch
        :param height: the height of the mudpatch
        """
        self.__bottom_left = bottom_left
        if width <= 0 or height <= 0 or depth <= 0:
            raise ValueError("The width and height can only be positive")
        self.__width = width
        self.__height = height
        self.__depth = depth

    def point_in_area(self, point: Triordinates) -> bool:
        """
        Checks wether a location is in the patch
        :param point: the location to check
        """
        return (self.__bottom_left[0] <= point[0] <= (self.__bottom_left[0] + self.__width) and \
                self.__bottom_left[1] <= point[1] <= (self.__bottom_left[1] + self.__height) and \
                self.__bottom_left[2] <= point[2] <= (self.__bottom_left[2] + self.__depth))

    @property
    def properties(self) -> Tuple[Triordinates, float, float]:
        """
        gets a tuple of the properties of the patch
        (bottom_left, width, height, depth)
        """
        return (self.__bottom_left, self.__width, self.__height, self.__depth)
    
    @staticmethod
    def get_lag() -> float:
        """
        gets the slow down buffer of the mud patch
        """
        return SLOWDOWN
