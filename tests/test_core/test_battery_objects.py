"""
Contains the unittest for the classes in the battery_objects module
"""

import unittest

from src import ParameterSet, BatteryCell


R0 = 0.02
R1 = 0.05
C1 = 0.003
Q = 1.65


def func_SOC_OCV(soc):
    return 4.2 - 0.7 * soc


def func_eta(soc):
    if soc < 0.5:
        return 1
    else:
        return 0.95


class TestParameterSets(unittest.TestCase):
    def test_constructor(self):
        param = ParameterSet(R0=R0, R1=R1, C1=C1, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)
        self.assertEqual(R0, param.R0)
        self.assertEqual(R1, param.R1)
        self.assertEqual(C1, param.C1)
        self.assertEqual(Q, param.Q)

    def test_constructor2(self):
        with self.assertRaises(TypeError):
            param = ParameterSet(R0=None, R1=R1, C1=C1, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)

    def test_constructor3(self):
        with self.assertRaises(TypeError):
            param = ParameterSet(R0=R0, R1=None, C1=C1, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)

    def test_constructor4(self):
        with self.assertRaises(TypeError):
            param = ParameterSet(R0=R0, R1=R1, C1=None, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)

    def test_constructor5(self):
        with self.assertRaises(TypeError):
            ParameterSet(R0=R0, R1=R1, C1=C1, Q=None, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)

    def test_constructor6(self):
        with self.assertRaises(TypeError):
            ParameterSet(R0=R0, R1=R1, C1=C1, Q=Q, func_SOC_OCV=None, func_eta=func_eta)

    def test_constructor7(self):
        with self.assertRaises(TypeError):
            ParameterSet(R0=R0, R1=R1, C1=C1, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=None)

    def test_func_SOC_OCV(self):
        param = ParameterSet(R0=R0, R1=R1, C1=C1, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)
        self.assertEqual(func_SOC_OCV(0.5), param.func_SOC_OCV(0.5))

    def test_func_eta(self):
        param = ParameterSet(R0=R0, R1=R1, C1=C1, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)
        self.assertEqual(func_eta(0.5), param.func_eta(0.5))


class TestBatteryCell(unittest.TestCase):
    soc_init = 0.5
    param = ParameterSet(R0=R0, R1=R1, C1=C1, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)

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





