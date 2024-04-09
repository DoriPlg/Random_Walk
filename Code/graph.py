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
Triordinates = Tuple[float, float, float]

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
                                       radius=portal[1], edgecolor='purple')
        endpoints_x.append(portal[2][0])
        endpoints_y.append(portal[2][1])
        ax.add_patch(circle)

    for mud in muds:
        rectangle = patches.Rectangle(*mud)
        ax.add_patch(rectangle)
    ax.axis('equal')
    ax.scatter(endpoints_x,endpoints_y, marker= "*")
    ax.scatter(0, 0, color='black', marker='x')
    # fig.show()
    fig.savefig(file_to_save+".png")

def walkers_unision(graph_name, data, color_list: list|None = None,
                    obstacles: tuple|None = None , file_to_save: str = f"{DESTINATION_PATH}_plot") -> None:
    """
    A function that plots on a graph the data picked up by the walker.
    :param graph_name: the title of the graph
    :param data: a dictionary containing the data to be plotted
    :param file_to_save: the desired filepath in which to save the path taken by the walker
    """
    fig, ax = plt.subplots()
    plt.title(graph_name)


    if not color_list:
        color_list = ["black", "blue", "red", "green", "yellow", "purple", "orange", "pink", "cyan", "magenta"]
    for walker in data:
        x = [i[0] for i in data[walker]]
        y = [i[1] for i in data[walker]]
        try:
            ax.scatter(x[1:], y[1:], color=color_list[walker])
            ax.plot(x, y, color=color_list[walker])
        except IndexError:
            ax.scatter(x[1:], y[1:], color="black")
            ax.plot(x, y, color="black")

    if obstacles:
        barriers = obstacles[0]
        portals = obstacles[1]
        muds = obstacles[2]
    else:
        barriers = []
        portals = []
        muds = []

    for barrier in barriers:
        ax.plot([barrier[0][0],barrier[1][0]],[barrier[0][1],barrier[1][1]], color='black')
    endpoints_x = []
    endpoints_y = []
    for portal in portals:
        circle = patches.Circle((portal[0][0], portal[0][1]),
                                       radius=portal[1], edgecolor='purple')
        
        endpoints_x.append(portal[2][0])
        endpoints_y.append(portal[2][1])
        ax.add_patch(circle)
    for mud in muds:
        rectangle = patches.Rectangle(*mud)
        
        ax.add_patch(rectangle)
       
    ax.axis('equal')
    ax.scatter(endpoints_x,endpoints_y, marker= "*")
    ax.scatter(0, 0, color='black', marker='x')
    fig.savefig(file_to_save+".png")

def show_walker_graph(data, file_to_save: str = f"{DESTINATION_PATH}_graph") -> None:
    """
    A function that plots on a graph the data picked up by the walker.
    :param data: a dictionary containing the data to be plotted
    :param file_to_save: the desired filepath in which to save the path taken by the walker
    :param color: the color to trace the course
    """
    x = [int(k) for k in data[0]]
    walkers = list(data.keys())
    for index, graph_type in enumerate(data[walkers[0]][x[0]]):
        fig = plt.figure()
        plt.xlabel("Amount of steps")
        if graph_type == "distance_axis":
            y_label = "Distance from the origin"
        elif graph_type == "crosses":
            y_label = "Amount of times the walker crossed the y-axis"
        elif graph_type == "escape":
            y_label = "Amount of time it took the walker to escape"
        elif graph_type == "distance_0":
            y_label = "Distance from the origin"
        plt.ylabel(y_label)
        plt.title(f"Graph of {graph_type}")
        for walker in data:
            to_plot = [data[walker][i][graph_type] for i in x]
            plt.plot(x, to_plot, label=f"Walker {walker}")
        plt.legend(loc="upper left")
        # fig.show()
        fig.savefig(file_to_save+f"_{index}.png")

def map_3d(walker_locations: list[list[Triordinates]]) -> None:
    """
    A function that plots on a 3D graph the data picked up by the walker.
    :param locations: a list containing the locations of the walkers
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    for walker in walker_locations:
        x = [i[0] for i in walker]
        y = [i[1] for i in walker]
        z = [i[2] for i in walker]
        ax.plot(x, y, z)
        ax.scatter(x[1:], y[1:], z[1:])

    plt.show()
    fig.show()
    fig.savefig(f"{DESTINATION_PATH}3d_plot.png")