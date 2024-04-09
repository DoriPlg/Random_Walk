"""
FILE : barrier_3d.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: A calss for barrier objects within a simulation
STUDENTS I DISCUSSED THE EXERCISE WITH:
WEB PAGES I USED:
NOTES: ...
"""
from typing import Tuple
from numpy import cross,dot

Trioordinates = Tuple[float,float,float]
def subtract_vectors(a: Trioordinates, b: Trioordinates) -> Trioordinates:
    """
    A function that subtracts two vectors from each other
    :param a: the first vector
    :param b: the second vector
    """
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

class Barrier3D:
    """
    A class building the barrier object in the random walker simulation
    Borders are straight lines which the walker can't pass to either way.
    """

    def __init__(self, corner: Trioordinates,
                  point_1: Trioordinates, point_2: Trioordinates) -> None:
        """
        A constructor for a new Barrier object
        barriers are parallelogram planes, with three points defining the corners
        and another constructred to complete the parallelogram
        :param corner: the edge point of the barrier.
        :param point_1: the first point of the barrier, will be the symetry axis
        :param point_2: the second point of the barrier, will be the symetry axis
        """
        self.__corner = corner
        self.__point1 = point_1
        self.__point2 = point_2
        mid_point = ((point_1[0] + point_2[0]) / 2,
                     (point_1[1] + point_2[1]) / 2,
                     (point_1[2] + point_2[2]) / 2)
        self.__edge = (2 * mid_point[0] - corner[0],
                         2 * mid_point[1] - corner[1],
                         2 * mid_point[2] - corner[2])

    def intersects(self, point_a: Trioordinates, point_b: Trioordinates) -> bool:
        """
        A function to check wether a movement between two points crosses the Barrier
        True if crosses,  False if doesn't
        :param point_a: the first point.
        :param point_b: the second point.
        """
        # Define the plane
        plane_point = self.__corner  # One point on the plane
        plane_normal = cross(subtract_vectors(self.__corner, self.__point1),
                              subtract_vectors(self.__corner, self.__point2))  # Normal to the plane

        # Define the line
        line_direction = subtract_vectors(point_a, point_b)  # Direction of the line

        # Check if the line and plane are parallel
        if dot(line_direction, plane_normal) == 0:
            return False  # They are parallel so they don't intersect
        
        # Calculate the intersection point
        t = dot(subtract_vectors(plane_point, point_a), plane_normal) / dot(line_direction, plane_normal)
        intersection_point = (point_a[0] + t * line_direction[0],
                              point_a[1] + t * line_direction[1],
                              point_a[2] + t * line_direction[2])
        
        # Check if the intersection point is between the four corners of the barrier
        if (point_a[0] <= intersection_point[0] <= point_b[0] or\
            point_b[0] <= intersection_point[0] <= point_a[0]) and\
            (point_a[1] <= intersection_point[1] <= point_b[1] or\
            point_b[1] <= intersection_point[1] <= point_a[1]) and\
            (point_a[2] <= intersection_point[2] <= point_b[2] or\
            point_b[2] <= intersection_point[2] <= point_a[2]):
            return True
        return False


    @property
    def points(self) -> tuple[Trioordinates,Trioordinates]:
        """
        returns the points between which a barrier is strung
        """
        return (self.__point1, self.__edge, self.__point2, self.__corner)
