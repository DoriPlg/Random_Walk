import unittest
import os
import tkinter as tk
from matplotlib import pyplot as plt
from Code.graph import *


class TestGraph(unittest.TestCase):
    """
    A test case class for testing graph-related functions.
    """

    def test_show_walker_way(self):
        movement_log = [(0, 0), (1, 1), (2, 2)]
        obstacles = ((((0, 0), (1, 1))), (((2, 2),1.5,(3, 3))), (((4, 4), 2.5, 5)))
        file_to_save = "./Results/temp"
        color = "black"
        self.assertIsNone(show_walker_way("Walker 1", movement_log, obstacles, file_to_save, color))

    def test_walkers_unision(self):
        graph_name = "Graph 1"
        data = [(0, 0), (1, 1), (2, 2)]
        color_list = ["red", "blue", "green"]
        obstacles = ((0, 0), (1, 1))
        file_to_save = "./Results/temp"
        self.assertIsNone(walkers_unision(graph_name, data, color_list, obstacles, file_to_save))

    def test_show_walker_graph(self):
        data = {
            0:{
            0:{"escape":10, "distance":20},
            10:{"escape":10, "distance":20},
            20:{"escape":10, "distance":20}}}
        file_to_save = "./Results/temp"
        self.assertIsNone(show_walker_graph(data, file_to_save))

    def test_map_3d(self):
        walker_locations = [[(0, 0, 0), (1, 1, 1), (2, 2, 2)], [(0, 0, 0), (1, 1, 1), (2, 2, 2)]]
        barriers = [((0, 0, 0), (1, 1, 1), (2, 2, 2), (3, 3, 3))]
        portals = [((0, 0, 0), 1)]
        mudspots = [((0, 0, 0), 1, 2, 3)]
        try:
            map_3d(walker_locations, barriers, portals, mudspots)
        except tk.TclError as e:
            if 'application has been destroyed' not in e.args[0]:
                raise

if __name__ == '__main__':
    unittest.main()
    if os.path.exists("./Results/temp"):
        os.remove("./Results/temp")
        os.remove("./Results/temp_0.png")
        os.remove("./Results/temp_1.png")
    else:
        print("File does not exist.")
