import unittest
import sys
print(sys.path)
from .. import walker as wk

class TestWalker(unittest.TestCase):
    def test_init(self):
        # Test default values
        walker = Walker('A')
        self.assertEqual(walker.movement, 'A')
        self.assertEqual(walker.location, (0, 0))
        self.assertEqual(walker.color, 'B')

        # Test custom values
        walker = Walker('C', (3, 4), 'R')
        self.assertEqual(walker.movement, 'C')
        self.assertEqual(walker.location, (3, 4))
        self.assertEqual(walker.color, 'R')

    def test_next_location(self):
        walker = Walker('A')
        next_loc = walker.next_location()
        self.assertIsInstance(next_loc, tuple)
        self.assertEqual(len(next_loc), 2)
        self.assertIsInstance(next_loc[0], float)
        self.assertIsInstance(next_loc[1], float)

    def test_directional_angle(self):
        walker = Walker('A')
        angle = walker.directional_angle()
        self.assertIsNone(angle)

        walker = Walker('C', (3, 4), 'R')
        angle = walker.directional_angle((5, 5))
        self.assertIsInstance(angle, float)


    def test_move(self):
        walker = Walker('A')
        initial_loc = walker.location
        moved = walker.move()
        self.assertEqual(moved, True)
        self.assertNotEqual(walker.location, initial_loc)

    def test_jump(self):
        walker = Walker('A')
        new_loc = (5, 5)
        jumped = walker.jump(new_loc)
        self.assertEqual(jumped, True)
        self.assertEqual(walker.location, new_loc)

    def test_color_pallet(self):
        color_pallet = Walker.color_pallet()
        self.assertIsInstance(color_pallet, dict)
        self.assertGreater(len(color_pallet), 0)

    def test_move_dict(self):
        move_dict = Walker.move_dict()
        self.assertIsInstance(move_dict, dict)
        self.assertGreater(len(move_dict), 0)

if __name__ == '__main__':
    unittest.main()
    
