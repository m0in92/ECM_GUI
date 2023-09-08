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
        t1 = 0.1
        i_app1 = -1.656
        soc1 = 0.7
        v1 = 3.98
        cap_discharge1 = -1.656*0.1/3600

        self.sol.update_arrays(t=t1, i_app=i_app1, soc=soc1, v=v1, cap_discharge=cap_discharge1)
        self.assertTrue(np.array_equal(np.array([t1]), self.sol.array_t))
        self.assertTrue(np.array_equal(np.array([i_app1]), self.sol.array_I))
        self.assertTrue(np.array_equal(np.array([v1]), self.sol.array_V))
        self.assertTrue(np.array_equal(np.array([cap_discharge1]), self.sol.array_cap_discharge))

        t2 = 0.2
        i_app2 = -1.656
        soc2 = 0.69
        v2 = 3.78
        cap_discharge2 = -1.656*0.2/3600

        self.sol.update_arrays(t=t2, i_app=i_app2, soc=soc2, v=v2, cap_discharge=cap_discharge2)
        self.assertTrue(np.array_equal(np.array([t1, t2]), self.sol.array_t))
        self.assertTrue(np.array_equal(np.array([i_app1, i_app2]), self.sol.array_I))
        self.assertTrue(np.array_equal(np.array([soc1, soc2]), self.sol.array_soc))
        self.assertTrue(np.array_equal(np.array([cap_discharge1, cap_discharge2]), self.sol.array_cap_discharge))

    def test_is_discharge(self):
        i_app_discharge = -1.656
        i_app_charge = 1.656

        self.assertTrue(Solution().is_discharge(i_app=i_app_discharge))
        self.assertFalse(Solution().is_discharge(i_app=i_app_charge))

    def test_calc_discharge_cap(self):
        i_app_discharge = -1.656
        i_app_charge = 1.656
        dt = 0.1
        cap_discharge_prev = 0.0

        self.assertEqual(0.0 + abs(i_app_discharge * dt / 3600),
                         Solution().calc_cap_discharge(cap_discharge_prev=cap_discharge_prev,
                                                       dt=dt, i_app=i_app_discharge))
        self.assertEqual(0.0,
                         Solution().calc_cap_discharge(cap_discharge_prev=cap_discharge_prev,
                                                       dt=dt, i_app=i_app_charge))


