import unittest
import math
from Code.td_walker import Walker3D, random_vector, gravitate

class TestWalker3D(unittest.TestCase):
    def test_position(self):
        # Test the position property of Walker
        position = (1.0, 2.0, 3.0)
        walker = Walker3D(position)
        self.assertEqual(walker.position, position)

    def test_jump(self):
        # Test the jump method of Walker
        position = (0.0, 0.0, 0.0)
        walker = Walker3D(position)
        walker.jump(walker.next_location())
        new_position = walker.position
        self.assertNotEqual(new_position, position)
        self.assertAlmostEqual(walker.get_distance(position), 1.0)

    def test_get_distance(self):
        # Test the get_distance method of Walker
        position = (0.0, 0.0, 0.0)
        walker = Walker3D(position)
        location = (1.0, 2.0, 3.0)
        distance = walker.get_distance(location)
        expected_distance = math.sqrt(14)
        self.assertAlmostEqual(distance, expected_distance)

    def test_str(self):
        # Test the __str__ method of Walker
        position = (1.0, 2.0, 3.0)
        walker = Walker3D(position)
        self.assertEqual(str(walker), "Walker3D at position (1.0, 2.0, 3.0)")

    def test_random_vector(self):
        # Test the random_vector function
        vector = random_vector()
        self.assertAlmostEqual(math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2), 1.0)

    def test_gravitate(self):
        # Test the gravitate function
        walker1 = Walker3D((0.0, 0.0, 0.0))
        walker2 = Walker3D((1.0, 1.0, 1.0))
        walkers = [walker1, walker2]
        gravitate(walkers, degree=1, gravity=1)
        self.assertNotEqual(walker1.position, (0.0, 0.0, 0.0))
        self.assertNotEqual(walker2.position, (1.0, 1.0, 1.0))