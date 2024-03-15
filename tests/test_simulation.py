import unittest
import os
from Code.simulation import Simulation, SimulationError, \
    check_data, run_from_json, run_and_plot
from Code.walker import Walker
from Code.portal import Portal
from Code.barrier import Barrier
from Code.mud import Mud
from Code.helper_functions import save_to_json

class TestSimulation(unittest.TestCase):

    def setUp(self):
        simulation = Simulation()

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
        for _ in range(10000):
            simulation.step()

    def test_barrier_loops(self):
        simulation = Simulation()
        barrier = Barrier((0,0), 5, 0)
        simulation.add_barrier(barrier)
        simulation.add_walker(Walker('A'))
        try:
            simulation.step()
            simulation.step()
            self.assertTrue(False)
        except SimulationError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_simulation_errors(self):
        simulation = Simulation()
        try:
            simulation.run_simulation(0,10)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)
        try:
            simulation.run_simulation(10,5)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)
        try:
            simulation.simulation_average(-1,10,5)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)
        try:
            simulation.simulation_average(1,0,5)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)
        try:
            simulation.simulation_average(1,10**5,10**2)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

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
        result = simulation.run_simulation(10)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), len(Walker.move_dict()))

    def test_simulation_average(self):
        simulation = Simulation()
        for key in Walker.move_dict():
            walker = Walker(key)
            simulation.add_walker(walker)
        simulation.simulation_average(10, 100, 1000)
        # Nothing to assert

    def test_graph_simulation(self):
        simulation = Simulation()
        for key in Walker.move_dict():
            walker = Walker(key)
            simulation.add_walker(walker)
        simulation.graph_simulation(1, 100, 200, 25, "temp_test")
        # Nothing to assert
        clear_files()

    def test_check_data(self):
        data ={
                "Walkers": 
                [
                    {"movement": "D_up", "color": "R", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "G", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "Bl", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "Or", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "P", "location": [0.0, 0.0]}
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
                "Simulation": {"type": "plot", "n": 1000, "filename": "temp_test"}
                }
        result = check_data(data)
        self.assertTrue(result)
        # Empty data
        try:
            result = check_data(None)
            self.assertTrue(False)
        except AttributeError:
            self.assertTrue(True)
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
                "Simulation": {"type": "plot", "n": 1000, "filename": "temp_test"}
                }
        result = check_data(data)
        self.assertFalse(result)
        # Missing key in sub-dictionary
        data ={
                "Walkers": 
                [
                    {"movemet": "D_up", "color": "R", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "G", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "Bl", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "Or", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "P", "location": [0.0, 0.0]}
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
                "Simulation": {"type": "plot", "n": 1000, "filename": "temp_test"}
                }
        result = check_data(data)
        self.assertFalse(result)
        # Slight problem in parameter
        data ={
                "Walkers": 
                [
                    {"movement": "D_up", "color": "Rzaza", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "G", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "Bl", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "Or", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "P", "location": [0.0, 0.0]}
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
                "Simulation": {"type": "plot", "n": 1000, "filename": "temp_test"}
                }
        result = check_data(data)
        self.assertFalse(result)
        # Problem in parameter type
        data ={
                "Walkers": 
                [
                    {"movement": "D_up", "color": "R", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "G", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "Bl", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "Or", "location":" [0.0, 0.0]"},
                    {"movement": "D_up", "color": "P", "location": [0.0, 0.0]}
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
                "Simulation": {"type": "plot", "n": 1000, "filename": "temp_test"}
                }
        result = check_data(data)
        self.assertTrue(result)
        # Simulation type with wrong variables
        data ={
                "Walkers": 
                [
                    {"movement": "D_up", "color": "R", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "G", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "Bl", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "Or", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "P", "location": [0.0, 0.0]}
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
                "Simulation": {"type": "graph", "n": 1000, "filename": "temp_test"}
                }
        result = check_data(data)
        self.assertFalse(result)

    def test_run_from_json(self):
        data ={
                "Walkers": 
                [
                    {"movement": "D_up", "color": "R", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "G", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "Bl", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "Or", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "P", "location": [0.0, 0.0]}
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
                "Simulation": {"type": "plot", "n": 1000, "filename": "temp_test"}
                }
        save_to_json(data, "temp_test_simulation.json")
        results = run_from_json("temp_test")
        self.assertIsInstance(results[0], dict)
        os.remove("temp_test_simulation.json")


    def test_run_and_plot(self):
        data ={
                "Walkers": 
                [
                    {"movement": "D_up", "color": "R", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "G", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "Bl", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "Or", "location": [0.0, 0.0]},
                    {"movement": "D_up", "color": "P", "location": [0.0, 0.0]}
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
                "Simulation": {"type": "plot", "n": 1000, "filename": "temp_test"}
                }
        result = run_and_plot(data, "temp_test")
        self.assertIsInstance(result, str)
        clear_files()

def clear_files():
    """
    Remove temporary image files generated during testing.
    """
    for i in range(len(Walker.move_dict())):
        try:
            os.remove(f"temp_test_{i}.png")
        except:
            pass
    try:
        os.remove("temp_test_all.png")
    except:
        pass
    try:
        os.remove("temp_test")
    except:
        pass
    try:
        os.remove("temp_test_5.png")
    except:
        pass

if __name__ == '__main__':
    unittest.main()
