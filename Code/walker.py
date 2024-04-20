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

Coordinates = Tuple[float, float]

PI = math.pi
MOVEMENTS = {
            'A': "Random direction, step size 1 unit",
            'B': "Random direction, step size chosen equally between [0.5,1.5]",
            'C': "Random direction chosen equally between (Up,Down,Right,Left), step size 1 unit",
            'D_up': "Direction chosen at Random but favoring up, step site 1 unit",
            'D_down': "Direction chosen at Random but favoring down, step site 1 unit",
            'D_right': "Direction chosen at Random but favoring right, step site 1 unit",
            'D_left': "Direction chosen at Random but favoring left, step site 1 unit",
            'D_axis': "Direction chosen at Random but favoring axis, step site 1 unit"
            }
COLORS = ["red", "green", "yellow", "blue", "cyan", "orange","brown", "purple","olive","black"]

class Walker:
    """
    A class for Walker objects in a random walker simulation
    """

    def __init__(self, movement: str, location: Coordinates = (0,0), color: str = 'black') -> None:
        """
        A constructor for a Walker object.
        :param movement:a string representing the walkers movement type from:
                        {
                        'A': "Random direction, step size 1 unit",
                        'B': "Random direction, step size chosen equally between [0.5,1.5]",
                        'C': "Random direction chosen equally between (Up,Down,Right,Left),
                             step size 1 unit",
                        'Dup': "Direction chosen at Random but favoring up, step site 1 unit",
                        'Ddown': "Direction chosen at Random but favoring down, step site 1 unit",
                        'Dright': "Direction chosen at Random but favoring right, step site 1 unit",
                        'Dleft': "Direction chosen at Random but favoring left, step site 1 unit",
                        'Daxis': "Direction chosen at Random but favoring axis, step site 1 unit"
                        }
        :param location:a tuple representing the starting place for the Walker,
                        defualts to (0,0) for (x,y)
        :param color:   a charcter representing the walker's color, from:
                        ["red", "green", "yellow", "blue", "cyan",
                          "orange","brown", "purple","olive"],
                        defaults to black.
        """
        self.__location = location
        if movement in MOVEMENTS:
            self.__movement = movement
        else:
            raise ValueError(f"Movement can only be of {MOVEMENTS.keys()}")
        if color in COLORS:
            self.__color = color
        else:
            raise ValueError(f"Color can only be of {COLORS}")

    def next_location(self) -> Coordinates:
        """
        Rreturns the next place the walker is to go to
        """
        # For B
        DISTANCES = (0.5,1.5)

        # For C
        DIRECTIONS = {'_up': PI/2,
                      '_right': 0,
                      '_down': (3/2)*PI,
                      '_left': PI}

        if self.__movement == 'A':
            angle = 2 * PI * random.random()
            return (self.__location[0] + math.cos(angle),
                    self.__location[1] + math.sin(angle))

        if self.__movement == 'B':
            angle = 2 * PI * random.random()
            distance = random.choice(DISTANCES)
            return (self.__location[0] + distance * math.cos(angle),
                        self.__location[1] + distance * math.sin(angle))

        if self.__movement == 'C':
            angle = random.choice(list(DIRECTIONS.values()))
            return (self.__location[0] + int(math.cos(angle)),
                    self.__location[1] + int(math.sin(angle)))

        if self.__movement[0] == 'D':
            angle = random.gauss(0, PI * 2 / 3)
            inclination = self.__movement[1:]
            if inclination in DIRECTIONS:
                angle += DIRECTIONS[inclination]
            elif inclination == "_axis":
                direction = self.directional_angle()
                if direction:
                    # If walker is not on the (0,0) Coordinate
                    angle += direction
                else:
                    # If walker is on the (0,0) point, randomly
                    angle = 2 * PI * random.random()
            else:
                raise AttributeError("Somewhere the second part of inclination changed")
            return (self.__location[0] + math.cos(angle),
                    self.__location[1] + math.sin(angle))

        raise AttributeError("Somewhere the movement type changed")

    def directional_angle(self, coordinate: Coordinates = (0,0)) -> float|None:
        """
        a function to get the angle from a walker to a given coordinate
        if the walker is on the coordinate returns None
        :param coordianate: the given coordinate
        """
        x_offset = self.location[0] - coordinate[0]
        y_offset = self.location[1] - coordinate[1]
        if x_offset == y_offset == 0:
            # If the walker is precisely at the desired coordinate.
            return None
        if x_offset > 0:
            return math.tanh(y_offset / x_offset) + PI
        if x_offset < 0:
            return math.tanh(y_offset / x_offset)
        return - math.copysign(PI/2, y_offset)

    def move(self) -> bool:
        """
        Moves the walker one step in it's own way.
        When needed, angles are in radians
        Returns True if successful, False if not.
        """
        try:
            next_spot = self.next_location()
        except AttributeError:
            return False
        return self.jump(next_spot)

    def jump(self, location: Coordinates) -> bool:
        """
        Sets anew the Walker's location. 
        Used in the move function and accessible from th API for portals.
        :param location: the desired location to which the walker's location will be set
        """
        if location:
            self.__location = location
            return True
        return False

    @property
    def location(self) -> Coordinates:
        """
        returns a Walker's location coordinates
        """
        return self.__location

    @property
    def movement(self) -> str:
        """
        returns the walker's movement type
        """
        return self.__movement

    @property
    def color(self) -> str:
        """
        returns a walkers color, as a full name
        """
        return self.__color

    @staticmethod
    def color_pallet() -> list[str]:
        """
        For UI reasons, returns the list describing the walker colors
        """
        return COLORS

    @staticmethod
    def move_dict() -> dict:
        """
        For UI reasons, returns the dictionary describing the walker class movement types
        """
        return MOVEMENTS

def gravitate(walkers: list[Walker], degree: int = 2, gravity: int = 0) -> None:
    """
    Additional feature for walkers that attract or push each other
    
    :param walkers: A list of Walker objects
    :param degree: The degree of attraction or repulsion between walkers,
                    the higher the stronger. (default: 5)
    :param gravity: A boolean indicating whether to apply gravity or not (default: True)
    :return: None
    """
    if len(walkers) <= 1 or gravity == 0:
        return
    nonrelative_locations = {}
    ratio = float(degree * len(walkers) * (gravity))
    for walker in walkers:
        bearing: tuple[float,float] = (0, 0)
        # direction as in (x, y) relative to walker
        for other in walkers:
            if other is walker:
                continue
            x_difference = other.location[0] - walker.location[0]
            y_difference = other.location[1] - walker.location[1]
            current_direction = (x_difference, y_difference)
            distance_squared = x_difference**2 + y_difference**2
            angle = walker.directional_angle(
                (walker.location[0] + current_direction[0],
                 walker.location[1] + current_direction[1]))

            # To avoid too strong attraction (wormholes and such)
            if distance_squared == 0:
                continue
            atrraction = min((ratio) / (distance_squared), 3)

            if angle:
                bearing = (bearing[0] + math.cos(angle) * atrraction,
                            bearing[1] + math.sin(angle) * atrraction)

        # Get location not relative to walker
        nonrelative_locations[walker] = (walker.location[0] + bearing[0],
                                        bearing[1] + walker.location[1])


    for walker in walkers:
        walker.jump(nonrelative_locations[walker])
