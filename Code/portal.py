"""
FILE : portal.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: A calss for portal objects within a simulation
STUDENTS I DISCUSSED THE EXERCISE WITH: 
WEB PAGES I USED:
NOTES: ...
"""

from typing import Tuple

Coordinates = Tuple[float,float]

class Portal:
    """
    A class for Portal objects in a random walker simulation.
    A portal will send a walker that has walked into it's circular zone to it's endpoint.
    Portals ore mono-directional.
    """

    def __init__(self, center: Coordinates, radius: float = 5, endpoint: Coordinates = (0,0)) -> None:
        """
        initiates a new portal object.
        :param center: the portal entry's center point.
        :param radius: the radius of the portal endpoint, defaults to 5 units.
                        negatives will be treated as absolute values
        :param endpoint: the endpoint of the portal, defaults to (0,0).
        """
        self.__center = center
        if radius == 0:
            raise ValueError("Radius cannot be 0")
        else:
            self.__radius = abs(radius)
        self.__endpoint = endpoint

    def inbounds(self, location: Coordinates) -> bool:
        """
        allows to check wether a certain location is within the portal's entrypoint
        :param location: the location to be checked
        """
        return ((self.__center[0] - location[0])**2 +
                (self.__center[1] - location[1])**2) <= self.__radius**2

    def get_end(self) -> Coordinates:
        """
        returns the endpoint of the portal
        """
        return self.__endpoint

    def get_center(self) -> Coordinates:
        """
        returns the center of the portal
        """
        return self.__center

    def get_radius(self) -> float:
        """
        returns the radius of the pportal
        """
        return self.__radius
