from Code.td_portal import Portal3D
from unittest import TestCase

class TestPortal(TestCase):
    def test_inbounds(self):
        # Create a portal with center at (0, 0, 0) and radius 5
        portal = Portal3D((0, 0, 0), 5)

        # Test a location outside the portal's radius
        self.assertFalse(portal.inbounds((10, 10, 10)))

        # Test a location inside the portal's radius
        self.assertTrue(portal.inbounds((2, 2, 2)))

    def test_endpoint(self):
        # Create a portal with center at (0, 0, 0) and endpoint at (1, 1, 1)
        portal = Portal3D((0, 0, 0), endpoint=(1, 1, 1))

        # Test the endpoint property
        self.assertEqual(portal.endpoint, (1, 1, 1))

    def test_center(self):
        # Create a portal with center at (2, 3, 4)
        portal = Portal3D((2, 3, 4))

        # Test the center property
        self.assertEqual(portal.center, (2, 3, 4))

    def test_radius(self):
        # Create a portal with center at (0, 0, 0) and radius 3
        portal = Portal3D((0, 0, 0), 3)

        # Test the radius property
        self.assertEqual(portal.radius, 3)
