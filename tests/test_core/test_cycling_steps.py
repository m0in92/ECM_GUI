"""
Provides unittest for testing the cyclers
"""
import unittest

import numpy as np

from src import DischargeStep, ChargeStep, RestStep, CustomStep


class TestDischargeCycler(unittest.TestCase):
    discharge_current = 1.656
    V_min = 2.5
    SOC_LIB = 1.0
    SOC_LIB_min = 0.0

    def test_constructor(self):
        cycler_instance = DischargeStep(discharge_current=self.discharge_current,
                                          V_min=self.V_min,
                                          SOC_LIB_min=self.SOC_LIB_min, SOC_LIB=self.SOC_LIB)
        self.assertEqual(0.0, cycler_instance.time_elapsed)
        self.assertEqual(-self.discharge_current, cycler_instance.discharge_current)
        self.assertEqual(self.SOC_LIB, cycler_instance.SOC_LIB)
        self.assertEqual(self.SOC_LIB_min, cycler_instance.SOC_LIB_min)


class TestDischargeCycler(unittest.TestCase):
    charge_current = 1.656
    V_max = 3.6
    SOC_LIB = 0.0
    SOC_LIB_max = 1.0

    def test_constructor(self):
        cycler_instance = ChargeStep(charge_current=self.charge_current,
                                       V_max=self.V_max,
                                       SOC_LIB_max=self.SOC_LIB_max, SOC_LIB=self.SOC_LIB)
        self.assertEqual(0.0, cycler_instance.time_elapsed)
        self.assertEqual(self.charge_current, cycler_instance.charge_current)
        self.assertEqual(self.SOC_LIB, cycler_instance.SOC_LIB)
        self.assertEqual(self.SOC_LIB_max, cycler_instance.SOC_LIB_max)

class TestRestCycler(unittest.TestCase):
    rest_time = 3600
    SOC_LIB = 1.0

    def test_constructor(self):
        cycler_instance = RestStep(rest_time=3600, SOC_LIB=self.SOC_LIB)

        self.assertEqual(self.rest_time, cycler_instance.rest_time)
        self.assertEqual(self.SOC_LIB, cycler_instance.SOC_LIB)


class TestCustomStep(unittest.TestCase):
    V_min = 2.5
    V_max = 4.2
    SOC_LIB_min = 0.0
    SOC_LIB_max = 1.0
    SOC_LIB = 0.0

    array_t = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    array_I = -1.1 * np.ones(10)
    array_I[5:] = -2.1

    cycling_step = CustomStep(array_t=array_t, array_I=array_I, V_min=V_min, V_max=V_max,
                              SOC_LIB_min=SOC_LIB_min, SOC_LIB_max=SOC_LIB_max, SOC_LIB=SOC_LIB)

    def test_constructor(self):
        self.assertTrue(np.array_equal(self.array_t, self.cycling_step.array_t))
        self.assertTrue(np.array_equal(self.array_I, self.cycling_step.array_I))

        self.assertEqual(self.V_min, self.cycling_step.V_min)
        self.assertEqual(self.V_max, self.cycling_step.V_max)
        self.assertEqual(self.SOC_LIB_max, self.cycling_step.SOC_LIB_max)
        self.assertEqual(self.SOC_LIB_min, self.cycling_step.SOC_LIB_min)

    def test_get_current(self):
        self.assertTrue(-1.1, self.cycling_step.get_current(step_name='custom', t=1))
        self.assertTrue(-1.1, self.cycling_step.get_current(step_name='custom', t=2))
        self.assertTrue(-1.1, self.cycling_step.get_current(step_name='custom', t=3))
        self.assertTrue(-1.1, self.cycling_step.get_current(step_name='custom', t=4))
        self.assertTrue(-1.1, self.cycling_step.get_current(step_name='custom', t=5))

        self.assertTrue(-1.1, self.cycling_step.get_current(step_name='custom', t=5.5))

        self.assertTrue(-2.1, self.cycling_step.get_current(step_name='custom', t=6))
        self.assertTrue(-2.1, self.cycling_step.get_current(step_name='custom', t=7))
        self.assertTrue(-2.1, self.cycling_step.get_current(step_name='custom', t=8))
        self.assertTrue(-2.1, self.cycling_step.get_current(step_name='custom', t=9))
        self.assertTrue(-2.1, self.cycling_step.get_current(step_name='custom', t=10))
