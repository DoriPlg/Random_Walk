from Code.td_mud import MudPatch3D
import unittest

class TestMud3D(unittest.TestCase):
    def test_point_in_area(self):
        # Test the point_in_area method of MudPatch3D
        mud = MudPatch3D((0, 0, 0), 5, 5, 5)
        # Test a location outside the mud patch
        self.assertFalse(mud.point_in_area((10, 10, 10)))
        # Test a location inside the mud patch
        self.assertTrue(mud.point_in_area((2, 2, 2)))

    def test_properties(self):
        # Test the properties property of MudPatch3D
        mud = MudPatch3D((0, 0, 0), 5, 5, 5)
        # Test the properties of the mud patch
        self.assertEqual(mud.properties, ((0, 0, 0), 5, 5, 5))

    def test_get_lag(self):
        # Test the get_lag method of MudPatch3D
        self.assertEqual(MudPatch3D.get_lag(), 0.6)