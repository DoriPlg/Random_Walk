import unittest
import math
import Code.barrier as br

class TestBarrier(unittest.TestCase):
    """
    A test case class for testing the functionality of the Barrier class.
    """

    def test_intersects(self):
        # Test case where a horizontal line intersects the barrier
        barrier = br.Barrier((0, 0), 5, 0)
        point_a = (0, -3)
        point_b = (0, 3)
        self.assertTrue(barrier.intersects(point_a, point_b))

        # Test case where a vertical line intersects the barrier
        barrier = br.Barrier((0, 0), 5, math.pi/2)
        point_a = (-3, 0)
        point_b = (3, 0)
        self.assertTrue(barrier.intersects(point_a, point_b))

        # Test case where a diagonal line intersects the barrier
        barrier = br.Barrier((0, 0), 5, math.pi/4)
        point_a = (3, -3)
        point_b = (-3, 3)
        self.assertTrue(barrier.intersects(point_a, point_b))

        # Test case where a perpendicular line does not intersect the barrier
        barrier = br.Barrier((0, 0), 5, 0)
        point_a = (0, 6)
        point_b = (0, 4)
        self.assertFalse(barrier.intersects(point_a, point_b))

        # Test case where the line does not intersect the barrier
        barrier = br.Barrier((0, 0), 5, 0)
        point_a = (-6, 0)
        point_b = (-4, 0)
        self.assertFalse(barrier.intersects(point_a, point_b))

    def test_points(self):
        # Test case for getting the points of the barrier
        barrier = br.Barrier((0, 0), 5, 0)
        expected_points = ((-2.5, 0), (2.5, 0))
        self.assertTrue(
            (barrier.points[0] == expected_points[0] and\
             barrier.points[1] == expected_points[1]) or\
            (barrier.points[0] == expected_points[1] and\
              barrier.points[1] == expected_points[0]))

    def test_get_function(self):
        # Test case for getting the function of a horizontal barrier
        barrier = br.Barrier((0, 0), 5, 0)
        self.assertEqual(barrier.get_function(barrier.points[0],barrier.points[1]), (0,0))

        # Test case for getting the function of a diagonal barrier
        barrier = br.Barrier((0, 0), 5, math.pi/4)
        barrier_func = tuple([round(number) for number in barrier.get_function(barrier.points[0],barrier.points[1])])
        self.assertEqual(barrier_func, (1,0))

        # Test case for getting the function of a diagonal barrier
        barrier = br.Barrier((0, 1), 5, math.pi/4)
        barrier_func = tuple([round(number) for number in barrier.get_function(barrier.points[0],barrier.points[1])])
        self.assertEqual(barrier_func, (1,1))

        # Test case for getting the function of a vertical line
        self.assertEqual(barrier.get_function((0,1),(0,-1)), "vertical")

if __name__ == '__main__':
    unittest.main()
    
    
