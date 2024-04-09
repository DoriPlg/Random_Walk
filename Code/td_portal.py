"""
FILE : portal_3d.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: A class for 3D portal objects within a simulation
STUDENTS I DISCUSSED THE EXERCISE WITH: 
WEB PAGES I USED:
NOTES: ...
"""

from typing import Tuple

Triordinates = Tuple[float, float, float]

class Portal3D:
    """
    A class for Portal objects in a random walker simulation.
    A portal will send a walker that has walked into it's circular zone to it's endpoint.
    Portals ore mono-directional.
    """

    def __init__(self, center: Triordinates, radius: float = 5, endpoint: Triordinates = (0,0,0)) -> None:
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

    def inbounds(self, location: Triordinates) -> bool:
        """
        allows to check wether a certain location is within the portal's entrypoint
        :param location: the location to be checked
        """
        return ((self.__center[0] - location[0])**2 +
                (self.__center[1] - location[1])**2 +
                (self.__center[2] - location[2])**2) <= self.__radius**2

    @property
    def endpoint(self) -> Triordinates:
        """
        returns the endpoint of the portal
        """
        return self.__endpoint

    @property
    def center(self) -> Triordinates:
        """
        returns the center of the portal
        """
        return self.__center

    @property
    def radius(self) -> float:
        """
        returns the radius of the pportal
        """
        return self.__radius
