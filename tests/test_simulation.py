"""
FILE : test_simulation.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
"""

import unittest
import os
import matplotlib.pyplot as plt # type: ignore
from Code.simulation import Simulation, \
    check_data, run_from_json, run_and_plot
from Code.walker import Walker
from Code.portal import Portal
from Code.barrier import Barrier
from Code.mud import Mud
from Code.helper_functions import SimulationError, save_to_json

DEST = "./temp_test"

class TestSimulation(unittest.TestCase):
    """
    A test case class for testing the Simulation class.

    This class contains test methods for various functionalities of the Simulation class,
    such as adding walkers, barriers, portals, mudspots, and performing simulation steps.

    Each test method tests a specific functionality of the Simulation class and asserts
    the expected behavior.

    Note: This class inherits from the unittest.TestCase class.

    Attributes:
        None
    """
    @classmethod
    def setUpClass(cls) -> None:
        os.system(f"mkdir {DEST}/")

    @classmethod
    def tearDownClass(cls) -> None:
        os.system(f"rm -rf {DEST}/")
        plt.close('all')

    def test_init(self):
        Simulation()
        Simulation(1)
        with self.assertRaises(ValueError):
            Simulation(2)

    def test_add_walker(self):
        simulation = Simulation()
        walker = Walker('A')
        simulation.add_walker(walker)

    def test_add_portal(self):
        simulation = Simulation()
        portal = Portal((10,10))
        simulation.add_portal(portal)

    def test_add_barrier(self):
        simulation = Simulation()
        barrier = Barrier((10,10),3,0)
        simulation.add_barrier(barrier)

    def test_add_mud(self):
        simulation = Simulation()
        mud = Mud((10,10),3,3)
        simulation.add_mud(mud)

    def test_step(self):
        simulation = Simulation()
        for key in Walker.move_dict():
            walker = Walker(key)
            simulation.add_walker(walker)
            initial_location = walker.location
            simulation.step()
            self.assertNotEqual(initial_location, walker.location)

    def test_obstacles(self):
        # Ensures the walkers are hitting obstacles
        simulation = Simulation()
        portal = Portal((0,6))
        simulation.add_portal(portal)
        barrier = Barrier((0,-2),6,0)
        simulation.add_barrier(barrier)
        mud = Mud((2,-2),3,4)
        simulation.add_mud(mud)
        simulation.add_walker(Walker('D_down'))
        simulation.add_walker(Walker('D_right'))
        simulation.add_walker(Walker('D_up'))
        for _ in range(1000):
            simulation.step()

    def test_barrier_loops(self):
        simulation = Simulation()
        barrier = Barrier((0,0), 5, 0)
        simulation.add_barrier(barrier)
        simulation.add_walker(Walker('A'))
        with self.assertRaises(SimulationError):
            simulation.step()

    def test_simulation_errors(self):
        simulation = Simulation()
        with self.assertRaises(ValueError):
            simulation.run_simulation(0,2,10)
        with self.assertRaises(ValueError):
            simulation.run_simulation(10,1,5)
        with self.assertRaises(ValueError):
            simulation.simulation_average(-1,10,1,5)
        with self.assertRaises(ValueError):
            simulation.simulation_average(1,0,1,5)
        with self.assertRaises(ValueError):
            simulation.simulation_average(1,10**5,2,10**2)

    def test_log(self):
        simulation = Simulation()
        for key in Walker.move_dict():
            walker = Walker(key)
            simulation.add_walker(walker)
            simulation.step()
            simulation.step()
            self.assertEqual(simulation.log[0][0], (0, 0))
            self.assertNotEqual(simulation.log[0][1], (0, 0))

    def test_run_simulation(self):
        simulation = Simulation()
        for key in Walker.move_dict():
            walker = Walker(key)
            simulation.add_walker(walker)
        result = simulation.run_simulation(10,2)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), len(Walker.move_dict()))

    def test_simulation_average(self):
        simulation = Simulation()
        for key in Walker.move_dict():
            walker = Walker(key)
            simulation.add_walker(walker)
        simulation.simulation_average(10, 100,1, 100)

    def test_graph_simulation(self):
        simulation = Simulation()
        for key in Walker.move_dict():
            walker = Walker(key)
            simulation.add_walker(walker)
        simulation.graph_simulation(1, 100, 200, 25, f"{DEST}/temp_test")

    def test_check_data(self):
        data ={
                "Walkers": 
                [
                    {"movement": "D_up", "color": "red", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "green", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "blue", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "orange", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "purple", "location": [0.0, 0.0]}
                ],
                "Barriers":
                [
                    {"center": [4.0, 20.0], "length": 8.0, "angle": -1.5},
                    {"center": [-4.0, 20.0], "length": 8.0, "angle": 1.5}
                ],
                "Portals":
                [
                    {"center": [0.0, 40.0], "endpoint": [0.0, 0.0], "radius": 1.5}
                ],
                "Mudspots": [{"bottom_left": [10,10], "width": 2, "height": 2}],
                "Simulation": {"type": "plot", "n": 100, "filename": f"{DEST}/_test"}
                }
        result = check_data(data)
        self.assertTrue(result)
        # Missing key
        data ={
                "Barriers":
                [
                    {"center": [4.0, 20.0], "length": 8.0, "angle": -1.5},
                    {"center": [-4.0, 20.0], "length": 8.0, "angle": 1.5}
                ],
                "Portals":
                [
                    {"center": [0.0, 40.0], "endpoint": [0.0, 0.0], "radius": 1.5}
                ],
                "Mudspots": [],
                "Simulation": {"type": "plot", "n": 100, "filename": f"{DEST}/_test"}
                }
        result = check_data(data)
        self.assertFalse(result)
        # Missing key in sub-dictionary
        data ={
                "Walkers": 
                [
                    {"movemet": "D_up", "color": "red", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "green", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "blue", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "orange", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "purple", "location": [0.0, 0.0]}
                ],
                "Barriers":
                [
                    {"center": [4.0, 20.0], "length": 8.0, "angle": -1.5},
                    {"center": [-4.0, 20.0], "length": 8.0, "angle": 1.5}
                ],
                "Portals":
                [
                    {"center": [0.0, 40.0], "endpoint": [0.0, 0.0], "radius": 1.5}
                ],
                "Mudspots": [],
                "Simulation": {"type": "plot", "n": 100, "filename": f"{DEST}/_test"}
                }
        result = check_data(data)
        self.assertFalse(result)
        # Slight problem in parameter
        data ={
                "Walkers": 
                [
                    {"movement": "D_up", "color": "Rzaza", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "green", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "blue", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "orange", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "purple", "location": [0.0, 0.0]}
                ],
                "Barriers":
                [
                    {"center": [4.0, 20.0], "length": 8.0, "angle": -1.5},
                    {"center": [-4.0, 20.0], "length": 8.0, "angle": 1.5}
                ],
                "Portals":
                [
                    {"center": [0.0, 40.0], "endpoint": [0.0, 0.0], "radius": 1.5}
                ],
                "Mudspots": [],
                "Simulation": {"type": "plot", "n": 100, "filename": f"{DEST}/_test"}
                }
        result = check_data(data)
        self.assertFalse(result)
        # Problem in parameter type
        data ={
                "Walkers": 
                [
                    {"movement": "D_up", "color": "red", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "green", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "blue", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "orange", "location":" [0.0, 0.0]"},
                    {"movement": "D_up", "color": "purple", "location": [0.0, 0.0]}
                ],
                "Barriers":
                [
                    {"center": [4.0, 20.0], "length": 8.0, "angle": -1.5},
                    {"center": [-4.0, 20.0], "length": 8.0, "angle": 1.5}
                ],
                "Portals":
                [
                    {"center": 2, "endpoint": [0.0, 0.0], "radius": 1.5}
                ],
                "Mudspots": [],
                "Simulation": {"type": "plot", "n": 100, "filename": f"{DEST}/_test"}
                }
        result = check_data(data)
        self.assertTrue(result)
        # Simulation type with wrong variables
        data ={
                "Walkers": 
                [
                    {"movement": "D_up", "color": "red", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "green", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "blue", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "orange", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "purple", "location": [0.0, 0.0]}
                ],
                "Barriers":
                [
                    {"center": [4.0, 20.0], "length": 8.0, "angle": -1.5},
                    {"center": [-4.0, 20.0], "length": 8.0, "angle": 1.5}
                ],
                "Portals":
                [
                    {"center": [0.0, 40.0], "endpoint": [0.0, 0.0], "radius": 1.5}
                ],
                "Mudspots": [{"bottom_left": [10,10], "width": 2, "height": 2}],
                "Simulation": {"type": "graph", "n": 100, "filename": f"{DEST}/_test"}
                }
        result = check_data(data)
        self.assertFalse(result)

        with self.assertRaises(AttributeError):
            check_data({})
        with self.assertRaises(TypeError):
            check_data(5)

    def test_run_from_json(self):
        data ={
                "Walkers": 
                [
                    {"movement": "D_up", "color": "red", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "green", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "blue", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "orange", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "purple", "location": [0.0, 0.0]}
                ], 
                "Barriers":
                [
                    {"center": [4.0, 20.0], "length": 8.0, "angle": -1.5},
                    {"center": [-4.0, 20.0], "length": 8.0, "angle": 1.5}
                ],
                "Portals":
                [
                    {"center": [0.0, 40.0], "endpoint": [0.0, 0.0], "radius": 1.5}
                ],
                "Mudspots": [],
                "Simulation": {"type": "plot", "n": 100, "filename": f"{DEST}/_test"}
                }
        save_to_json(data, f"{DEST}/temp_test_simulation.json")
        results = run_from_json(f"{DEST}/temp_test_simulation.json")
        self.assertIsInstance(results[0], dict)

    def test_run_and_plot_plot(self):
        data ={
                "Walkers": 
                [
                    {"movement": "D_up", "color": "red", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "green", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "blue", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "orange", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "purple", "location": [0.0, 0.0]}
                ], 
                "Barriers":
                [
                    {"center": [4.0, 20.0], "length": 8.0, "angle": -1.5},
                    {"center": [-4.0, 20.0], "length": 8.0, "angle": 1.5}
                ],
                "Portals":
                [
                    {"center": [0.0, 40.0], "endpoint": [0.0, 0.0], "radius": 1.5}
                ],
                "Mudspots": [],
                "Simulation": {"type": "plot", "n": 100, "filename": f"{DEST}/_test"}
                }
        result = run_and_plot(data, f"{DEST}/_test")
        self.assertIsInstance(result, str)

    def test_run_and_plot_graph(self):
        data ={
                "Walkers": 
                [
                    {"movement": "D_up", "color": "red", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "green", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "blue", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "orange", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "purple", "location": [0.0, 0.0]}
                ],
                "Barriers":
                [
                    {"center": [6.0, 20.0], "length": 8.0, "angle": -1.5}
                ],
                "Portals":
                [
                    {"center": [0.0, 60.0], "endpoint": [0.0, 0.0], "radius": 1.5}
                ],
                "Mudspots": [],
                "Simulation": {"type": "graph", "n": 100, "iterations": 100,
                               "max_depth":200, "steps": 25,"filename": f"{DEST}/_test"}
                }
        result = run_and_plot(data, f"{DEST}/temp_test")
        self.assertIsInstance(result, str)
