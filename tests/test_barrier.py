import unittest
import math
import Code.barrier as br

class TestBarrier(unittest.TestCase):
    """
    A test case class for testing the functionality of the Barrier class.
    """

    def test_init(self):
        # Test case for initializing a horizontal barrier
        center = (0, 0)
        length = 5
        angle = 0
        barrier = br.Barrier(center, length, angle)
        points = ((-2.5,0), (2.5,0))
        self.assertTrue(barrier.points == points or barrier.points == points[::-1])

        # Test case for initializing a vertical barrier
        corner = (0, 0)
        length = 5
        angle = math.pi/2
        barrier = br.Barrier(corner, length, angle)
        points = ((0,-2.5), (0,2.5))
        print(barrier.points)
        self.assertTrue(
            (math.isclose(barrier.points[0][0],points[0][0], abs_tol=0.01) and\
             math.isclose(barrier.points[0][1],points[0][1], abs_tol=0.01)) or\
            (math.isclose(barrier.points[0][0],points[1][0], abs_tol=0.01) and\
             math.isclose(barrier.points[1][1],points[0][1], abs_tol=0.01)))

        # Test case for bad input
        corner = (0, 0)
        length = -5
        angle = math.pi/4
        with self.assertRaises(ValueError):
            barrier = br.Barrier(corner, length, angle)

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

        # Test case where the barrier is vertical and the line is diagonal
        barrier = br.Barrier((0, 0), 5, math.pi/2)
        point_a = (-3, -3)
        point_b = (3, 3)
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
