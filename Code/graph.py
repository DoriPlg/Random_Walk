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

DESTINATION_PATH = "./Results/"


def show_walker_way(name:str, movement_log: list[Coordinates], obstacles: Tuple,
                    file_to_save: str = f"{DESTINATION_PATH}scatterplot", color: str = "black") -> None:
    """
    A function that plots on a graph the path a waker went through.
    :param name: the title of the Graph
    :param movement_log: a list containing ordered moves made by the walker
    :param file_to_save: the desired filepath in which to save the path taken by the walker
    :param obstacles: tuple containing:
                            A list containing pairs of coordinates, between which 
                            each barrier is spread
                            A list containing tuples of Coordinates (rep. centeres),
                            floats (rep. radii) and Coordinates (rep. endpoints)
                            A list containg bottom_left corners, widths and
                            heights of mudspots
    :param file_to_save: the name of the desired saving space for the plots
    :param color: the color to trace the course of the walker
    """
    x = [i[0] for i in movement_log]
    y = [i[1] for i in movement_log]

    barriers = obstacles[0]
    portals = obstacles[1]
    muds = obstacles[2]

    fig = plt.figure()
    ax = plt.axes()

    plt.title(name)

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
    for mud in muds:
        rectangle = patches.Rectangle(*mud, facecolor="brown")
        ax.add_patch(rectangle)

    ax.axis('equal')
    ax.scatter(endpoints_x,endpoints_y, marker= "*")
    ax.scatter(0, 0, color='black', marker='x')
    # fig.show()
    fig.savefig(file_to_save+".png")

def show_walker_graph(data, file_to_save: str = f"{DESTINATION_PATH}graph") -> None:
    """
    A function that plots on a graph the data picked up by the walker.
    :param data: a dictionary containing the data to be plotted
    :param file_to_save: the desired filepath in which to save the path taken by the walker
    :param color: the color to trace the course
    """
    data = {1:{"0": {"distance_0": 12.829550312031577, "escape": 134.8, "distance_axis": [10.446449317460795, 5.314618044112166], "crosses": 16.0}, "1": {"distance_0": 17.356898839317008, "escape": 93.2, "distance_axis": [9.819990267498948, 12.478367202045224], "crosses": 11.6}, "2": {"distance_0": 28.2, "escape": 157.6, "distance_axis": [28.2, 3.113052163432568e-14], "crosses": 8.4}, "3": {"distance_0": 66.92273883291057, "escape": 35.2, "distance_axis": [6.819226583392487, 65.95841562042902], "crosses": 41.2}},
2:{"0": {"distance_0": 12.829550312031577, "escape": 134.8, "distance_axis": [10.446449317460795, 5.314618044112166], "crosses": 16.0}, "1": {"distance_0": 17.356898839317008, "escape": 93.2, "distance_axis": [9.819990267498948, 12.478367202045224], "crosses": 11.6}, "2": {"distance_0": 28.2, "escape": 157.6, "distance_axis": [28.2, 3.113052163432568e-14], "crosses": 8.4}, "3": {"distance_0": 66.92273883291057, "escape": 35.2, "distance_axis": [6.819226583392487, 65.95841562042902], "crosses": 41.2}},
3:{"0": {"distance_0": 12.829550312031577, "escape": 134.8, "distance_axis": [10.446449317460795, 5.314618044112166], "crosses": 16.0}, "1": {"distance_0": 17.356898839317008, "escape": 93.2, "distance_axis": [9.819990267498948, 12.478367202045224], "crosses": 11.6}, "2": {"distance_0": 28.2, "escape": 157.6, "distance_axis": [28.2, 3.113052163432568e-14], "crosses": 8.4}, "3": {"distance_0": 66.92273883291057, "escape": 35.2, "distance_axis": [6.819226583392487, 65.95841562042902], "crosses": 41.2}},
4:{"0": {"distance_0": 12.829550312031577, "escape": 134.8, "distance_axis": [10.446449317460795, 5.314618044112166], "crosses": 16.0}, "1": {"distance_0": 17.356898839317008, "escape": 93.2, "distance_axis": [9.819990267498948, 12.478367202045224], "crosses": 11.6}, "2": {"distance_0": 28.2, "escape": 157.6, "distance_axis": [28.2, 3.113052163432568e-14], "crosses": 8.4}, "3": {"distance_0": 66.92273883291057, "escape": 35.2, "distance_axis": [6.819226583392487, 65.95841562042902], "crosses": 41.2}},
5:{"0": {"distance_0": 12.829550312031577, "escape": 134.8, "distance_axis": [10.446449317460795, 5.314618044112166], "crosses": 16.0}, "1": {"distance_0": 17.356898839317008, "escape": 93.2, "distance_axis": [9.819990267498948, 12.478367202045224], "crosses": 11.6}, "2": {"distance_0": 28.2, "escape": 157.6, "distance_axis": [28.2, 3.113052163432568e-14], "crosses": 8.4}, "3": {"distance_0": 66.92273883291057, "escape": 35.2, "distance_axis": [6.819226583392487, 65.95841562042902], "crosses": 41.2}},
}
    x = [int(k) for k in data]
    walkers = list(data[x[0]].keys())
    for graph_type in data[x[0]][walkers[0]]:
        fig = plt.figure()
        ax = plt.axes()
        plt.title(f"Graph of {graph_type}")
        for walker in data[x[0]]:
            print(walker)
            to_plot = [data[i][walker][graph_type] for i in x]
            ax.plot(x, to_plot, label=f"Walker {walker}")
        fig.show()


show_walker_graph(2)
input()
