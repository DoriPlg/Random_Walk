import unittest
import math
from Code.td_walker import Walker3D

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
