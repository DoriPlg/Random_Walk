import unittest
import os
from Code.LLM.data_generator import generate_data, save_data
from Code.simulation import check_data

class TestDataGen(unittest.TestCase):
    """
    This class contains unit tests for the data generation functionality.

    Methods:
    - test_generate_data: Tests the generate_data function.
    - test_check_data: Tests the check_data function.
    """

    def test_generate_data(self):
        """
        Tests the generate_data function.
        """
        for _ in range(10):
            data1, data2 = generate_data()
            self.assertTrue(check_data(data1))
            self.assertTrue(check_data(data2))

    def test_save_data(self):
        """
        Tests the save_data function.
        """
        save_data(10, "temp.dat")
        os.remove("temp.dat")

        