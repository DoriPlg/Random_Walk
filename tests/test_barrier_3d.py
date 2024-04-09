import unittest
import math
from Code.barrier_3d import Barrier3D

class TestBarrier3D(unittest.TestCase):
    def test_init(self):
        corner = (0, 0, 0)
        point_1 = (1, 1, 1)
        point_2 = (2, 2, 3)  # Different z-coordinate
        barrier = Barrier3D(corner, point_1, point_2)

    def test_intersects(self):
        # Test case 1: Line is perpendicular to the barrier
        corner = (0, 0, 0)
        point_1 = (0, 0, 2)
        point_2 = (2, 0, 0)
        barrier = Barrier3D(corner, point_1, point_2)
        point_a = (1, 1, 1)
        point_b = (1, -1, 1)
        self.assertTrue(barrier.intersects(point_a, point_b))

        # Test case 2: Line is parallel to the barrier but does not intersect
        point_a = (1, 0, 0)
        point_b = (3, 0, 0)
        self.assertFalse(barrier.intersects(point_a, point_b))

        # Test case 3: Line is parallel to the barrier and lies on the barrier plane
        point_a = (0, 0, 1)
        point_b = (2, 0, 1)
        self.assertFalse(barrier.intersects(point_a, point_b))

        # Test case 4: Line intersects the barrier at an endpoint
        point_a = (1, 1, 0)
        point_b = (0, 0, 2)
        self.assertTrue(barrier.intersects(point_a, point_b))

        # Test case 5: Line intersects the barrier inside the barrier
        point_a = (1, -1, 1)
        point_b = (1, 1, 1)
        self.assertTrue(barrier.intersects(point_a, point_b))

        # Test case 6: Line is collinear with the barrier but does not intersect
        point_a = (1, 2, 1)
        point_b = (1, 1, 1)
        self.assertFalse(barrier.intersects(point_a, point_b))
       

if __name__ == '__main__':
    unittest.main()
    