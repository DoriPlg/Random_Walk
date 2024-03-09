"""
FILE : walker.py
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

Coordinates = Tuple[float,float]

class Walker:
    """
    A class for Walker objects in a random walker simulation
    """
    __movements = {
                    'A': "Random direction, step size 1 unit",
                    'B': "Random direction, step size chosen equally between [0.5,1.5]",
                    'C': "Random direction chosen equally between (Up,Down,Right,Left), step size 1 unit",
                    'D': "Direction chosen at Random but favoring up, step site 1 unit"
                    }
    __colors = {'R': "Red", 'G': "Green", 'Y': "Yellow", 'B': "Black"}

    def __init__(self, movement: str, location: Coordinates = (0,0), color: str = 'B') -> None:
        """
        A constructor for a Walker object.
        :param movement:    a string representing the walkers movement type from:
                            {
                            'A': "Random direction, step size 1 unit",
                            'B': "Random direction, step size chosen equally between [0.5,1.5]",
                            'C': "Random direction chosen equally between (Up,Down,Right,Left), step size 1 unit",
                            'D': "Direction chosen at Random but favoring up, step site 1 unit"
                            }
        :param location:    a tuple representing the starting place for the Walker,
                            defualts to (0,0) for (x,y)
        :param color:       a charcter representing the walker's color,
                            from {'R': "Red", 'B': "Blue", 'G': "Green", 'Y': "Yellow", 'B': "Black"},
                            defaults to black.
        """
        self.__location = location
        if movement in self.__movements:
            self.__movement = movement
        else:
            raise ValueError("Movement can only be of ('A','B','C','D')")
        if color in self.__colors:
            self.__color = color
        else:
            raise ValueError("Color can only be of ('R','G','B','Y')")

    def next_loc(self) -> Coordinates:
        """
        Rreturns the next place the walker is to go to
        """
        # For B
        DISTANCES = (0.5,1.5)

        # For C
        DIRECTIONS = {'up': math.pi/2,
                      'right': 0,
                      'down': (3/2)*math.pi,
                      'left': math.pi}
        
        if self.__movement == 'A':
            angle = 2 * math.pi * random.random()
            return (self.__location[0] + math.cos(angle), self.__location[1] + math.sin(angle))

        if self.__movement == 'B':
            angle = 2 * math.pi * random.random()
            distance = random.choice(DISTANCES)
            return (self.__location[0] + distance * math.cos(angle),
                        self.__location[1] + distance * math.sin(angle))

        if self.__movement == 'C':
            angle = random.choice(DIRECTIONS.values())
            return (self.__location[0] + math.cos(angle), self.__location[1] + math.sin(angle))

        if self.__movement == 'D':
            angle = random.gauss(math.pi, math.pi/2) - math.pi/2
            return self.__location[0] + math.cos(angle), self.__location[1] + math.sin(angle)
        
        return None

    def move(self) -> bool:
        """
        Moves the walker one step in it's own way.
        When needed, angles are in radians
        Returns True if successful, False if not.
        """
        return self.jump(self.next_loc())

    def jump(self, location: Coordinates) -> bool:
        """
        Sets anew the Walker's location. 
        Used in the move function and accessible from th API for portals.
        :param location: the desired location to wich the walker's location will be set
        """
        if location:
            self.__location = location
            return True
        return False
    
    def get_location(self) -> Coordinates:
        """
        returns a Walker's location coordinates
        """
        return self.__location
    
    def get_color(self) -> str:
        """
        returns a walkers color, as a full name
        """
        return self.__colors[self.__color]

    def pull_push(self, other, power: int = 1,gravity: bool = True) -> None:
        """
        Additional feature for a walkers that attract or push each other, for pairs
        """
        pass
