import unittest
import os
import Code.data_generator as dgen
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
            data1, data2 = dgen.generate_data()
            self.assertTrue(check_data(data1))
            self.assertTrue(check_data(data2))

    def test_save(self):
        """
        Tests the save_to_json function.
        """
        data1, data2 = dgen.generate_data()
        dgen.save_to_json(data1, "test1.json")
        dgen.save_to_json(data2, "test2.json")
        self.assertTrue(os.path.exists("test1.json"))
        self.assertTrue(os.path.exists("test2.json"))
        os.system("rm -rf test2.json")
        os.system("rm -rf test1.json")

    def test_save_json(self):
        """
        Tests the save_json function.
        """
        data1, data2 = dgen.generate_data()
        dgen.save_json(data1)
        dgen.save_json(data2)
        self.assertTrue(os.path.exists(data1["Simulation"]["filename"] + "_simulation.json"))
        self.assertTrue(os.path.exists(data2["Simulation"]["filename"] + "_simulation.json"))
        os.system(f"rm -rf {data1['Simulation']['filename']}_simulation.json")
        os.system(f"rm -rf {data2['Simulation']['filename']}_simulation.json")

    def test_random_simulation(self):
        """
        Tests the random_simulation function.
        """
        for _ in range(10):
            filename = dgen.random_simulation()
            self.assertTrue(os.path.exists(filename + "_simulation.json"))
            os.system(f"rm -rf {filename}_simulation.json")
        