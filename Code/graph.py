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
import matplotlib.patches as patches

Coordinates = Tuple[float,float]

DESTINATION_PATH = "/home/dori/Documents/UNI/Intro/final_project/Results/"


def show_walker_way(movement_log: list[Coordinates], barriers: list[tuple[Coordinates]], portals: list,
                    file_to_save: str = f"{DESTINATION_PATH}scatterplot", color: str = "black") -> None:
    """
    A function that plots on a graph the path a waker went through.
    :param movement_log: a list containing ordered moves made by the walker
    :param file_to_save: the desired filepath in which to save the path taken by the walker
    :param barriers: a list containing pairs of coordinates, between which each barrier is spread
    :param portals: a list containing tuples of Coordinates (rep. centeres), floats (rep. radii) and Coordinates (rep. endpoints)
    """
    x = [i[0] for i in movement_log]
    y = [i[1] for i in movement_log]

    fig = plt.figure()
    ax = plt.axes()

    ax.scatter(x[1:], y[1:], color=color)
    ax.plot(x, y, color=color)
    for barrier in barriers:
        ax.plot([barrier[0][0],barrier[1][0]],[barrier[0][1],barrier[1][1]], color='black')
    endpoints_x = []
    endpoints_y = []
    for portal in portals:
        circle = patches.Circle((portal[0][0], portal[0][1]),
                                       radius=portal[1], edgecolor='purple', facecolor='none')
        endpoints_x.append(portal[2][0])
        endpoints_y.append(portal[2][1])
        ax.add_patch(circle)
    ax.scatter(endpoints_x,endpoints_y, marker= "*")
    ax.scatter(0, 0, color='black', marker='x')
    fig.savefig(file_to_save+".png")
