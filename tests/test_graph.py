import unittest
from Code.graph import *


class TestGraph(unittest.TestCase):

    def test_show_walker_way(self):
        movement_log = [(0, 0), (1, 1), (2, 2)]
        obstacles = ((0, 0), (1, 1))
        file_to_save = "./Results/scatterplot"
        color = "black"
        self.assertIsNone(show_walker_way("Walker 1", movement_log, obstacles, file_to_save, color))

    def test_walkers_unision(self):
        graph_name = "Graph 1"
        data = [(0, 0), (1, 1), (2, 2)]
        color_list = ["red", "blue", "green"]
        obstacles = ((0, 0), (1, 1))
        file_to_save = "./Results/_plot"
        self.assertIsNone(walkers_unision(graph_name, data, color_list, obstacles, file_to_save))

    def test_show_walker_graph(self):
        data = [(0, 0), (1, 1), (2, 2)]
        file_to_save = "./Results/_graph"
        self.assertIsNone(show_walker_graph(data, file_to_save))

    def test_map_3d(self):
        walker_locations = [[(0, 0, 0), (1, 1, 1), (2, 2, 2)], [(0, 0, 0), (1, 1, 1), (2, 2, 2)]]
        barriers = [((0, 0, 0), (1, 1, 1), (2, 2, 2), (3, 3, 3))]
        portals = [((0, 0, 0), 1)]
        mudspots = [((0, 0, 0), 1, 2, 3)]
        self.assertIsNone(map_3d(walker_locations, barriers, portals, mudspots))

if __name__ == '__main__':
    unittest.main()

