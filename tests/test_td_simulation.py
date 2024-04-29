import unittest
from matplotlib import pyplot as plt # type: ignore
from Code.td_simulation import Simulation_3D, run_from_dict
from Code.td_mud import MudPatch3D
from Code.td_barrier import Barrier3D
from Code.td_portal import Portal3D
from Code.td_walker import Walker3D
from Code.helper_functions import SimulationError

class TestSimulation3D(unittest.TestCase):

    def test_add_walker(self) -> None:
        simulation = Simulation_3D()
        walker = Walker3D((0, 0, 0))
        simulation.add_walker(walker)

    def test_add_portal(self) -> None:
        simulation = Simulation_3D()
        portal = Portal3D((0, 0, 0), 1, (1, 1, 1))
        simulation.add_portal(portal)

    def test_add_barrier(self) -> None:
        simulation = Simulation_3D()
        barrier = Barrier3D((0, 0, 0), (0,1, 1), (1, 1, 1))
        simulation.add_barrier(barrier)

    def test_add_mud(self) -> None:
        simulation = Simulation_3D()
        mud = MudPatch3D((0, 0, 0), 1, 1, 1)
        simulation.add_mud(mud)

    def test_step(self) -> None:
        # Add walkers, portals, barriers, and mud patches to the simulation
        simulation = Simulation_3D()
        mud = MudPatch3D((0, 0, 0), 1, 1, 1)
        walker = Walker3D((0, -10, 0))
        barrier = Barrier3D((0, 10, 0), (20,1, 1), (10, 1, 1))
        portal = Portal3D((30, 0, 0), 1, (1, 1, 1))
        simulation.add_walker(walker)
        simulation.add_portal(portal)
        simulation.add_barrier(barrier)
        simulation.add_mud(mud)

        # Perform a simulation step
        steps_one = simulation.step()
        steps_after = simulation.step()

        # Assert that the walker has moved to a new location
        self.assertNotEqual(steps_one, steps_after)

    def test_run_simulation(self) -> None:
        # Add walkers, portals, barriers, and mud patches to the simulation
        simulation = Simulation_3D()
        mud = MudPatch3D((0, 0, 0), 1, 1, 1)
        walker = Walker3D((0, -10, 0))
        barrier = Barrier3D((0, 10, 0), (20,1, 1), (10, 1, 1))
        portal = Portal3D((30, 0, 0), 1, (1, 1, 1))
        simulation.add_walker(walker)
        simulation.add_portal(portal)
        simulation.add_barrier(barrier)
        simulation.add_mud(mud)

        # Run the simulation for a specified number of iterations
        n = 10
        simulation.run_simulation(n)

        # Assert that the simulation has performed the specified number of iterations
        self.assertEqual(simulation.step(), n+1)

    def test_value_error_test(self) -> None:
        # Test that the simulation raises a ValueError when the gravity value is not -1, 0, or 1
        with self.assertRaises(ValueError):
            Simulation_3D(gravity=2)

        # Test that the simulation raises a ValueError when the reset value is negative
        with self.assertRaises(ValueError):
            Simulation_3D(reset=-1)

    def test_trapped(self) -> None:
        simulation = Simulation_3D()

        # Add barriers to the simulation that will trap the walker
        barriers = (
            Barrier3D((0, 0, 0), (0, 0, 0.5), (0, 0.5, 0)),
            Barrier3D((0, 0, 0), (0.5, 0, 0), (0, 0, 0.5)),
            Barrier3D((0, 0, 0), (0, 0.5, 0), (0.5, 0, 0)),
            Barrier3D((0.5, 0.5, 0.5), (0.5, 0.5, 0), (0.5, 0, 0.5)),
            Barrier3D((0.5, 0.5, 0.5), (0.5, 0, 0.5), (0, 0.5, 0.5)),
            Barrier3D((0.5, 0.5, 0.5), (0, 0.5, 0.5), (0.5, 0.5, 0))
        )
        for barrier in barriers:
            simulation.add_barrier(barrier)

        # Add a walker to the simulation
        walker = Walker3D((0.5, 0.5, 0.5))
        simulation.add_walker(walker)

        # Assert that the walker is trapped
        with self.assertRaises(SimulationError):
            simulation.step()

    def test_reset(self) -> None:
        simulation = Simulation_3D(reset=1)

        walker = Walker3D((0, 0, 0))
        simulation.add_walker(walker)
        for _ in range(10):
            simulation.step()
        self.assertIn((0, 0, 0), walker.log[1:])

    def test_load_dict(self) -> None:
        data = {
            "Walkers": [{"position": (0, 0, 0)}],
            "Portals": [{"center": (10, 0, 0), "radius": 1, "endpoint": (1, 1, 1)}],
            "Barriers": [{"corner": (50, 0, 0), "point_1": (50, 1, 1), "point_2": (50, 1, 1)}],
            "Mudspots": [{"bottom_left": (0, 0, 0), "height": 1, "width": 1, "depth": 1}],
            "Simulation": {"gravity": 1, "reset": 1, "n": 10}
        }
        run_from_dict(data)
        data["Simulation"] = {"gravity": 1, "n": 10}
        run_from_dict(data)
        data["Simulation"] = {"reset": 1, "n": 10}
        run_from_dict(data)
        data["Simulation"] = {"n": 10}
        run_from_dict(data)
        plt.close('all')

        