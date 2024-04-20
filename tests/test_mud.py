import unittest
from Code.mud import Mud, Coordinates

class TestMud(unittest.TestCase):

    def test_point_in_area(self):
        mud = Mud((0, 0), 5, 5)
        self.assertTrue(mud.point_in_area((2, 2)))
        self.assertTrue(mud.point_in_area((4, 4)))
        self.assertFalse(mud.point_in_area((6, 6)))
        self.assertFalse(mud.point_in_area((-1, -1)))

    def test_properties(self):
        mud = Mud((0, 0), 5, 5)
        self.assertEqual(mud.properties, ((0, 0), 5, 5))

    def test_get_lag(self):
        self.assertEqual(Mud.get_lag(), 0.6)

