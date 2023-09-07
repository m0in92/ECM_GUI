"""
Contains the unittest for the classes in the sol_and_plot_objects module
"""

import unittest

import numpy as np

from src.visualization.sol_and_plot_objects import Solution


class TestSolution(unittest.TestCase):
    sol = Solution()

    def test_constructor(self):
        self.assertTrue(np.array_equal(np.array([]), self.sol.array_t))
        self.assertTrue(np.array_equal(np.array([]), self.sol.array_I))
        self.assertTrue(np.array_equal(np.array([]), self.sol.array_soc))
        self.assertTrue(np.array_equal(np.array([]), self.sol.array_V))

    def test_update_arrays(self):
        self.sol.update_arrays(t=0.1, i_app=-1.656, soc=0.7, v=4.2)
        print(self.sol.array_t)
