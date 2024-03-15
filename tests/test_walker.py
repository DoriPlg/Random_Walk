import unittest
import Code.walker as wk

class TestWalker(unittest.TestCase):
    def test_init(self):
        # Test default values
        walker = wk.Walker('A')
        self.assertEqual(walker.movement, 'A')
        self.assertEqual(walker.location, (0, 0))
        self.assertEqual(walker.color, 'blue')

        # Test custom values
        walker = wk.Walker('C', (3, 4), 'R')
        self.assertEqual(walker.movement, 'C')
        self.assertEqual(walker.location, (3, 4))
        self.assertEqual(walker.color, 'red')

    def test_next_location(self):
        walker = wk.Walker('A')
        next_loc = walker.next_location()
        self.assertIsInstance(next_loc, tuple)
        self.assertEqual(len(next_loc), 2)
        self.assertIsInstance(next_loc[0], float)
        self.assertIsInstance(next_loc[1], float)

    def test_directional_angle(self):
        walker = wk.Walker('A')
        angle = walker.directional_angle()
        self.assertIsNone(angle)

        walker = wk.Walker('C', (3, 4), 'R')
        angle = walker.directional_angle((5, 5))
        self.assertIsInstance(angle, float)


    def test_move(self):
        walker = wk.Walker('A')
        initial_loc = walker.location
        moved = walker.move()
        self.assertEqual(moved, True)
        self.assertNotEqual(walker.location, initial_loc)

    def test_jump(self):
        walker = wk.Walker('A')
        new_loc = (5, 5)
        jumped = walker.jump(new_loc)
        self.assertEqual(jumped, True)
        self.assertEqual(walker.location, new_loc)

    def test_color_pallet(self):
        color_pallet = wk.Walker.color_pallet()
        self.assertIsInstance(color_pallet, dict)
        self.assertGreater(len(color_pallet), 0)

    def test_move_dict(self):
        move_dict = wk.Walker.move_dict()
        self.assertIsInstance(move_dict, dict)
        self.assertGreater(len(move_dict), 0)

if __name__ == '__main__':
    unittest.main()
    
