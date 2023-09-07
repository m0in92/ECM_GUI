import unittest

from src.core.battery_objects import ParameterSet, BatteryCell


R0 = 0.02
R1 = 0.05
C1 = 0.003


def func_SOC_OCV(soc):
    return 0.7 * soc - 4.2


class TestParameterSets(unittest.TestCase):
    # R0 = 0.02
    # R1 = 0.05
    # C1 = 0.003

    # def func_SOC_OCV(self, soc):
    #     return 0.7 * soc - 4.2

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



