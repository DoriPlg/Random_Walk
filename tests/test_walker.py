"""
FILE : test_walker.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
"""

import unittest
import math
import Code.walker as wk
from Code.walker import gravitate

class TestWalker(unittest.TestCase):
    """
    Test cases for the Walker class.
    """

    def test_init(self):
        """
        Test the initialization of the Walker class.

        This test method checks if the Walker class is initialized correctly with
        both default and custom values.

        Test default values:
        - Creates a Walker object with movement 'A' and checks if the movement attribute is
        set correctly.
        - Checks if the location attribute is set to (0, 0) as the default value.
        - Checks if the color attribute is set to 'blue' as the default value.

        Test custom values:
        - Creates a Walker object with movement 'C', location (3, 4), and color 'R'.
        - Checks if the movement attribute is set to 'C' as the custom value.
        - Checks if the location attribute is set to (3, 4) as the custom value.
        - Checks if the color attribute is set to 'red' as the custom value.
        """
        walker = wk.Walker('A')
        self.assertEqual(walker.movement, 'A')
        self.assertEqual(walker.location, (0, 0))
        self.assertEqual(walker.color, 'black')

        walker = wk.Walker('C', (3, 4), 'red')
        self.assertEqual(walker.movement, 'C')
        self.assertEqual(walker.location, (3, 4))
        self.assertEqual(walker.color, 'red')

    def test_next_location(self):
        """
        Test the next_location method of the Walker class.

        This test case checks if the next_location method returns a tuple of two floats.
        """
        walker = wk.Walker('A')
        next_loc = walker.next_location()
        self.assertIsInstance(next_loc, tuple)
        self.assertEqual(len(next_loc), 2)
        self.assertIsInstance(next_loc[0], float)
        self.assertIsInstance(next_loc[1], float)

    def test_directional_angle(self):
        """
        Test the `directional_angle` method of the Walker class.

        This test case checks the behavior of the `directional_angle` method in different scenarios.
        It verifies that the method returns the expected results and handles different
        input cases correctly.

        Test 1:
        - Create a Walker object with the initial position 'A'.
        - Call the `directional_angle` method.
        - Assert that the returned angle is None.

        Test 2:
        - Create a Walker object with the initial position 'C', position (3, 4), and direction 'R'.
        - Call the `directional_angle` method with the target position (5, 5).
        - Assert that the returned angle is of type float.
        """
        # Test 1: walker is on the same point as the given coordinate
        walker = wk.Walker('A')
        angle = walker.directional_angle()
        self.assertIsNone(angle)

        # Test 2: walker is not on the same point as the given coordinate
        walker = wk.Walker('C', (0, 0), 'red')
        angle = walker.directional_angle((3, 4))
        self.assertEqual(angle, math.tanh(4/3))

        # Test 3: walker is not on the same point as the given coordinate, same x
        angle = walker.directional_angle((0, 5))
        self.assertEqual(angle, math.radians(90))
        angle = walker.directional_angle((0, -5))
        self.assertEqual(angle, math.radians(-90))




    def test_move(self):
        """
        Test the move method of the Walker class.

        This test case checks if the move method updates the location attribute of the Walker object
        """
        walker = wk.Walker('A')
        initial_loc = walker.location
        moved = walker.move()
        self.assertEqual(moved, True)
        self.assertNotEqual(walker.location, initial_loc)

    def test_jump(self):
        """
        Test the jump method of the Walker class.

        This test case checks if the jump method updates the location attribute of the Walker object
        """
        walker = wk.Walker('A')
        new_loc = (5, 5)
        jumped = walker.jump(new_loc)
        self.assertEqual(jumped, True)
        self.assertEqual(walker.location, new_loc)

    def test_color_pallet(self):
        """
        Test the color_pallet method of the Walker class.

        This test case checks if the color_pallet method returns a dictionary and the
        dictionary is not empty.
        """
        color_pallet = wk.Walker.color_pallet()
        self.assertIsInstance(color_pallet, list)
        self.assertGreater(len(color_pallet), 0)

    def test_move_dict(self):
        """
        Test the move_dict method of the Walker class.

        This test case checks if the move_dict method returns a dictionary and the
        dictionary is not empty.
        """
        move_dict = wk.Walker.move_dict()
        self.assertIsInstance(move_dict, dict)
        self.assertGreater(len(move_dict), 0)

    def test_gravitate(self):
        """
        Test the gravitate function.

        This test case checks if the gravitate function updates the location attribute of
        the Walker objects in the list.
        """
        # Test case 1: Test the gravitate function with a list of 2 walkers
        # Positive gravity
        walker_list1 = []
        walker_list2 = []
        walker_list1.append(wk.Walker("A", location=(10,10)))
        walker_list2.append(wk.Walker("A", location=(10,10)))
        walker_list1.append(wk.Walker("A", location=(-10,10)))
        walker_list2.append(wk.Walker("A", location=(-10,10)))
        gravitate(walker_list1,100,1)
        gravitate(walker_list2,1,1)
        self.assertTrue(walker_list1[0].location != (10,10))
        self.assertTrue(walker_list1[0].location[0] < walker_list2[0].location[0])

        # Neqative gravity
        walker_list1 = []
        walker_list2 = []
        walker_list1.append(wk.Walker("A", location=(10,10)))
        walker_list2.append(wk.Walker("A", location=(10,10)))
        walker_list1.append(wk.Walker("A", location=(-10,10)))
        walker_list2.append(wk.Walker("A", location=(-10,10)))
        gravitate(walker_list1,100, -1)
        gravitate(walker_list2,1, -1)
        self.assertTrue(walker_list1[0].location != (10,10))
        self.assertTrue(walker_list1[0].location[0] > walker_list2[0].location[0])

        walker_list = []
        walker_list.append(wk.Walker("A", location=(10,10)))
        walker_list.append(wk.Walker("A", location=(-10,10)))
        walker_list.append(wk.Walker("A"))
        gravitate(walker_list,10**3,1)
        print(walker_list[2].location)
        self.assertTrue(1 < walker_list[2].location[1] < 7)


if __name__ == '__main__':
    unittest.main()
