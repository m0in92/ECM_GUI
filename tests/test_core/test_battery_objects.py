"""
Contains the unittest for the classes in the battery_objects module
"""

import unittest

from src.core.battery_objects import ParameterSet, BatteryCell, DischargeCycler


R0 = 0.02
R1 = 0.05
C1 = 0.003


def func_SOC_OCV(soc):
    return 0.7 * soc - 4.2


class TestParameterSets(unittest.TestCase):
    def test_constructor(self):
        param = ParameterSet(R0=R0, R1=R1, C1=C1, func_SOC_OCV=func_SOC_OCV)
        self.assertEqual(R0, param.R0)
        self.assertEqual(R1, param.R1)
        self.assertEqual(C1, param.C1)

    def test_constructor2(self):
        with self.assertRaises(TypeError):
            param = ParameterSet(R0=None, R1=R1, C1=C1, func_SOC_OCV=func_SOC_OCV)

    def test_constructor3(self):
        with self.assertRaises(TypeError):
            ParameterSet(R0=R0, R1=R1, C1=C1, func_SOC_OCV=None)

    def test_func_SOC_OCV(self):
        param = ParameterSet(R0=R0, R1=R1, C1=C1, func_SOC_OCV=func_SOC_OCV)
        self.assertEqual(func_SOC_OCV(0.5), param.func_SOC_OCV(0.5))


class TestBatteryCell(unittest.TestCase):
    soc_init = 0.5
    param = ParameterSet(R0=R0, R1=R1, C1=C1, func_SOC_OCV=func_SOC_OCV)

    def test_constructor(self):
        b_cell = BatteryCell(param=self.param, soc_init=self.soc_init)

        self.assertEqual(R0, b_cell.param.R0)
        self.assertEqual(R1, b_cell.param.R1)
        self.assertEqual(C1, b_cell.param.C1)
        self.assertEqual(self.soc_init, b_cell.soc_init)
        self.assertEqual(self.soc_init, b_cell.soc)
        self.assertEqual(func_SOC_OCV(soc=self.soc_init), b_cell.ocv)

    def test_constructor2(self):
        with self.assertRaises(TypeError):
            BatteryCell(param=self.param, soc_init=None)


class TestDischargeCycler(unittest.TestCase):
    discharge_current = 1.656
    V_min = 2.5
    SOC_LIB = 1.0
    SOC_LIB_min = 0.0

    def test_constructor(self):
        cycler_instance = DischargeCycler(discharge_current=self.discharge_current,
                                          V_min=self.V_min,
                                          SOC_LIB_min=self.SOC_LIB_min, SOC_LIB=self.SOC_LIB)
        self.assertEqual(0.0, cycler_instance.time_elapsed)
        self.assertEqual(-self.discharge_current, cycler_instance.discharge_current)
        self.assertEqual(self.SOC_LIB, cycler_instance.SOC_LIB)
        self.assertEqual(self.SOC_LIB_min, cycler_instance.SOC_LIB_min)



