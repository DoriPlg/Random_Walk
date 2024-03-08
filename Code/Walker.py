#################################################################
# FILE : Walker.py
# WRITER : Dori_Peleg , dori.plg , 207685306
# EXERCISE : intro2cs final_project 2024
# DESCRIPTION: A class for the walker object
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED:
# NOTES: ...
#################################################################

from typing import Tuple, List, Dict
import math
import random

Coordinates = Tuple[int, int]

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
                            defualts to (0,0)
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

    def move(self) -> None:
        """
        Moves the walker one step in it's own way.
        When needed, angles are in radians
        """
        DIRECTIONS = {'up': math.pi/2,
                      'right': 0,
                      'down': (3/2)*math.pi,
                      'left': math.pi}
        
        if self.__movement == 'A':
            angle = 2 * math.pi * random.random()
        if self.__movement == 'B':
            pass
        if self.__movement == 'C':
            pass
        if self.__movement == 'D':
            pass

    def jump(self, location: Coordinates):
        pass

