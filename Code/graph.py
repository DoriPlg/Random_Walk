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
from mpl_toolkits.mplot3d.art3d import Poly3DCollection # type: ignore
from mpl_toolkits.mplot3d import Axes3D # type: ignore
import numpy as np

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

def map_3d(walker_locations: list[list[Triordinates]],
           barriers: list[tuple[Triordinates,Triordinates,Triordinates,Triordinates]],
           portals: list[tuple[Triordinates,float]],
           mudspots: list[tuple[Triordinates,float,float,float]]) -> None:
    """
    A function that plots on a 3D graph the data picked up by the walker.
    :param locations: a list containing the locations of the walkers
    """
    fig = plt.figure()
    ax: Axes3D
    ax = fig.add_subplot(111, projection='3d')

    for walker in walker_locations:
        w_x = [i[0] for i in walker]
        w_y = [i[1] for i in walker]
        w_z = [i[2] for i in walker]
        ax.plot(w_x, w_y, w_z)
        ax.scatter(w_x[1:], w_y[1:], w_z[1:])

    for barrier in barriers:

        # Create a polygon from the points and add it to the plot
        polygon = Poly3DCollection([np.array([barrier[0],
                                              barrier[1],
                                              barrier[2],
                                              barrier[3]])],
                                               color="black",alpha=0.5)
        ax.add_collection3d(polygon)

    for portal in portals:
        # Show portal as a 3D sphere
        portal_center = portal[0]
        portal_radius = portal[1]

        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        p_x: np.ndarray
        p_y: np.ndarray
        p_z: np.ndarray
        p_x = portal_center[0] + portal_radius * np.outer(np.cos(u), np.sin(v))
        p_y = portal_center[1] + portal_radius * np.outer(np.sin(u), np.sin(v))
        p_z = portal_center[2] + portal_radius * np.outer(np.ones(np.size(u)), np.cos(v))

        ax.plot_surface(p_x, p_y, p_z, color='purple', alpha=0.5)

    for mud in mudspots:
        # Show mud as a 3D rectangle
        bottom_left = mud[0]
        width = mud[1]
        height = mud[2]
        depth = mud[3]

        mud_cube = (bottom_left,
                    (bottom_left[0] + width, bottom_left[1], bottom_left[2]),
                    (bottom_left[0], bottom_left[1] + height, bottom_left[2]),
                    (bottom_left[0] + width, bottom_left[1] + height, bottom_left[2]),
                    (bottom_left[0], bottom_left[1], bottom_left[2] + depth),
                    (bottom_left[0] + width, bottom_left[1], bottom_left[2] + depth),
                    (bottom_left[0], bottom_left[1] + height, bottom_left[2] + depth),
                    (bottom_left[0] + width, bottom_left[1] + height, bottom_left[2] + depth))
        verts = [[mud_cube[0], mud_cube[1], mud_cube[5], mud_cube[4]],
                 [mud_cube[2], mud_cube[3], mud_cube[7], mud_cube[6]],
                 [mud_cube[0], mud_cube[1], mud_cube[3], mud_cube[2]],
                 [mud_cube[4], mud_cube[5], mud_cube[7], mud_cube[6]],
                 [mud_cube[0], mud_cube[4], mud_cube[6], mud_cube[2]],
                 [mud_cube[1], mud_cube[5], mud_cube[7], mud_cube[3]]]
        rectangle = Poly3DCollection(verts, facecolors="brown", alpha=0.5)
        ax.add_collection3d(rectangle)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()
    fig.show()
    fig.savefig(f"{DESTINATION_PATH}3d_plot.png")