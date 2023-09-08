"""
Provides unittest for testing the cyclers
"""
import unittest

from src import DischargeStep, ChargeStep, RestStep


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
