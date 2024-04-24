import unittest
from unittest.mock import patch
import os
from Code.helper_functions import *

class TestHelperFunctions(unittest.TestCase):

    def test_save_to_json(self):
        # Test saving data to JSON file
        data = {"name": "John", "age": 30}
        filename = "test_data.json"
        save_to_json(data, filename)
        # Assert that the file exists
        self.assertTrue(os.path.exists(filename))
        # Clean up the file
        os.system(f"rm -rf {filename}")

    def test_load_simulation(self):
        # Test loading simulation from JSON file
        file_path = "test_data.json"
        # Create a test JSON file
        with open(file_path, 'w') as f:
            json.dump({"name": "John", "age": 30}, f)
        # Load the simulation
        result = load_simulation(file_path)
        # Assert that the loaded data matches the test data
        self.assertEqual(result, {"name": "John", "age": 30})
        # Clean up the file
        os.system(f"rm -rf {file_path}")

    def test_passes_0(self):
        # Test counting the number of elements that pass the condition
        lst = [1.5, 2.7, -3.2, 0, 4.1]
        result = passes_0(lst)
        # Assert that the result is 2 (the list values pass through 0 twice)
        self.assertEqual(result, 2)

        # Test counting the number of elements that pass the condition
        lst = [1.5,-1,0,0,0, 2.7, -3.2, 0,0,0, 4.1]
        result = passes_0(lst)
        # Assert that the result is 4 (the list values pass through 0 four times)
        self.assertEqual(result, 4)

        # Test counting the number of elements that pass the condition
        lst = [1.5,1,1]
        result = passes_0(lst)
        # Assert that the result is 4 (the list values pass through 0 four times)
        self.assertEqual(result, 0)

        # Test counting the number of elements that pass the condition
        lst = [1.5]
        result = passes_0(lst)
        # Assert that the result is 4 (the list values pass through 0 four times)
        self.assertEqual(result, 0)

        # Test counting the number of elements that pass the condition
        lst = []
        result = passes_0(lst)
        # Assert that the result is 4 (the list values pass through 0 four times)
        self.assertEqual(result, 0)

    def test_is_intable(self):
        # Test checking if a value is intable
        self.assertTrue(is_intable(10))
        self.assertTrue(is_intable(3.14))
        self.assertTrue(is_intable("100"))
        self.assertFalse(is_intable("abc"))
        self.assertFalse(is_intable([1, 2, 3]))

    def test_is_int(self):
        # Test checking if a value is an integer
        # Note, some behaviours are untrue but are tailored to the program
        self.assertTrue(is_int(10))
        self.assertFalse(is_int(3.14))
        self.assertFalse(is_int("100"))
        self.assertFalse(is_int("abc"))
        self.assertFalse(is_int([1, 2, 3]))

    def test_is_float(self):
        # Test checking if a value is a float
        # Note, some behaviours are untrue but are tailored to the program
        self.assertTrue(is_float(10))
        self.assertTrue(is_float(3.14))
        self.assertTrue(is_float("100"))
        self.assertFalse(is_float("abc"))
        self.assertFalse(is_float([1, 2, 3]))

