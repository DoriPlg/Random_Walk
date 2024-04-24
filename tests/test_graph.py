import unittest
import os
from matplotlib import pyplot as plt # type: ignore
from Code.graph import *


class TestGraph(unittest.TestCase):
    """
    A test case class for testing graph-related functions.
    """

    @classmethod
    def setUpClass(cls):
        os.system("mkdir temp_results")

    @classmethod
    def tearDownClass(cls):
        os.system("rm -rf ./temp_results")
        plt.close('all')

    def test_show_walker_way(self):
        movement_log = [(0, 0), (1, 1), (2, 2)]
        barrier_data = ((0, 0), (1, 1))
        portal_data = ((0, 0), 1, (1, 1))
        mud_data = ((0, 0), 1, 2)
        obstacles = ((barrier_data, barrier_data), (portal_data, portal_data), (mud_data, mud_data))
        file_to_save = "./temp_results/temp"
        color = "black"
        self.assertIsNone(show_walker_way("Walker 1", movement_log, obstacles, file_to_save, color))

    def test_walkers_unision(self):
        graph_name = "Graph 1"
        data = {0:[(0, 0), (1, 1), (2, 2)]}
        color_list = ["red", "blue", "green"]
        barrier_data = ((0, 0), (1, 1))
        portal_data = ((0, 0), 1, (1, 1))
        mud_data = ((0, 0), 1, 2)
        obstacles = ((barrier_data, barrier_data), (portal_data, portal_data), (mud_data, mud_data))
        file_to_save = "./temp_results/temp"
        self.assertIsNone(walkers_unision(graph_name, data, color_list, obstacles, file_to_save))

    def test_show_walker_graph(self):
        data = {
            0:{
            0:{"escape":10, "distance":20},
            10:{"escape":10, "distance":20},
            20:{"escape":10, "distance":20}}}
        file_to_save = "./temp_results/temp"
        self.assertIsNone(show_walker_graph(data, file_to_save))

    def test_map_3d(self):
        walker_locations = [[(0, 0, 0), (1, 1, 1), (2, 2, 2)], [(0, 0, 0), (1, 1, 1), (2, 2, 2)]]
        barriers = [((0, 0, 0), (1, 1, 1), (2, 2, 2), (3, 3, 3))]
        portals = [((0, 0, 0), 1)]
        mudspots = [((0, 0, 0), 1, 2, 3)]
        map_3d(walker_locations, barriers, portals, mudspots)

