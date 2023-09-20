"""
Provides the unittest for ECM solvers
"""

import unittest
import pickle

import numpy as np

from src import ParameterSet, BatteryCell, DischargeStep, CustomStep, Solution
from src import DTSolver

R0 = 0.02
R1 = 0.05
C1 = 0.003
Q = 1.65
soc_init = 0.5

discharge_current = 1.656
V_min = 3.7
SOC_LIB = 1.0
SOC_LIB_min = 0.0


def func_SOC_OCV(soc):
    return 4.2 - 1.2 * soc


def func_eta(soc):
    if soc < 0.5:
        return 1
    else:
        return 0.95


class TestDTSolver(unittest.TestCase):
    param = ParameterSet(R0=R0, R1=R1, C1=C1, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)
    b_cell = BatteryCell(param=param, soc_init=soc_init)
    standard_cycler = DischargeStep(discharge_current=discharge_current, V_min=V_min,
                                    SOC_LIB_min=SOC_LIB_min, SOC_LIB=SOC_LIB)

    def test_constructor(self):
        solver = DTSolver(battery_cell=self.b_cell)
        self.assertEqual(type(self.b_cell), type(solver.b_cell))
        self.assertEqual(soc_init, solver.b_cell.soc_init)
        self.assertEqual(R0, solver.b_cell.param.R0)
        self.assertEqual(R1, solver.b_cell.param.R1)
        self.assertEqual(C1, solver.b_cell.param.C1)
        self.assertEqual(func_SOC_OCV(soc_init), solver.b_cell.param.func_SOC_OCV(solver.b_cell.soc_init))

    def test_constructor2(self):
        with self.assertRaises(TypeError):
            DTSolver(battery_cell=None)

    def test_solver_standard_cycler(self):
        solver = DTSolver(battery_cell=self.b_cell)
        sol = solver.solve(cycling_step=self.standard_cycler, dt=0.1)
        self.assertTrue(np.allclose(np.array([0, 0.1]), sol.array_t))
        self.assertTrue(np.allclose(np.array([0, -1.656]), sol.array_I))
        self.assertTrue(np.allclose(np.array([0.5, 0.49997352]), sol.array_soc))
        self.assertTrue(np.allclose([3.6, 3.48411178], sol.array_V))

    def test_custom_solver(self):
        from parameter_sets.Calce123 import R0, R1, C1, Q, func_SOC_OCV, func_eta

        # Read experimental data below
        sol_exp = Solution().read_from_csv_file(filepath='tests/test_solvers/A1-A123-Dynamics.csv')

        # simulation parameters are below
        soc_init = 0.38775
        V_min = 2
        V_max = 4
        SOC_LIB = soc_init
        SOC_LIB_min = 0.0
        SOC_LIB_max = 1.0

        param = ParameterSet(R0=R0, R1=R1, C1=C1, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)
        b_cell = BatteryCell(param=param, soc_init=soc_init)
        cycle_step = CustomStep(array_t=sol_exp.array_t, array_I=sol_exp.array_I,
                                V_min=V_min, V_max=V_max, SOC_LIB_min=SOC_LIB_min, SOC_LIB_max=SOC_LIB_max,
                                SOC_LIB=SOC_LIB)

        solver = DTSolver(battery_cell=b_cell)
        sol = solver.solve(cycling_step=cycle_step, dt=10)

        with open("tests/test_solvers/array_V_sim", "rb") as file:
            std_sol = pickle.load(file)

        self.assertTrue(np.array_equal(sol.array_V, std_sol))
