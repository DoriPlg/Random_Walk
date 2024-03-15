import unittest
from Code.portal import Portal
import Code.portal as prt

class TestPortal(unittest.TestCase):

    def test_inbounds(self):
        portal = Portal((0, 0), 5, (10, 10))
        self.assertTrue(portal.inbounds((5, 0)))
        self.assertTrue(portal.inbounds((0, 5)))
        self.assertTrue(portal.inbounds((3, 4)))
        self.assertFalse(portal.inbounds((15, 15)))

    def test_endpoint(self):
        portal = Portal((0, 0), 5, (10, 10))
        self.assertEqual(portal.endpoint, (10, 10))

    def test_center(self):
        portal = Portal((0, 0), 5, (10, 10))
        self.assertEqual(portal.center, (0, 0))

    def test_radius(self):
        portal = Portal((0, 0), 5, (10, 10))
        self.assertEqual(portal.radius, 5)

if __name__ == '__main__':
    unittest.main()
