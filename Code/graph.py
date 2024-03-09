"""
FILE : graph.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: This page will make a graph from the motion of a walker
STUDENTS I DISCUSSED THE EXERCISE WITH: 
WEB PAGES I USED:
NOTES: ...
"""

from typing import Tuple
import matplotlib.pyplot as plt

Coordinates = Tuple[float,float]

DESTINATION_PATH = "/home/dori/Documents/UNI/Intro/final_project/Results/"


def show_walker_way(movement_log: list[Coordinates],
                    file_to_save: str = f"{DESTINATION_PATH}scatterplot") -> None:
    """
    A function that plots on a graph the path a waker went through.
    :param movement_log: a list containing ordered moves made by the walker
    :param file_to_save: the desired filepath in which to save the path taken by the walker
    """
    x = [i[0] for i in movement_log]
    y = [i[1] for i in movement_log]

    fig = plt.figure()
    ax = plt.axes()

    ax.plot(x, y)
    fig.savefig(file_to_save+".png")
