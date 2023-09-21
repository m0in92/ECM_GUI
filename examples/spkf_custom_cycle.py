"""
This example script performs the ECM cycling on a custom cycling step using sigma-point kalman filter.
"""

__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2023 by Moin Ahmed. All rights reserved.'
__status__ = 'developement'


from parameter_sets.Calce123 import *
import src

# Read experimental data below
sol_exp = src.Solution().read_from_csv_file(filepath='A1-A123-Dynamics.csv')

# simulation parameters are below
soc_init = 0.0
V_min = 1
V_max = 4
SOC_LIB = soc_init
SOC_LIB_min = 0.0
SOC_LIB_max = 1.0

param = src.ParameterSet(R0=R0, R1=R1, C1=C1, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)
b_cell = src.BatteryCell(param=param, soc_init=soc_init)

solver = src.DTSolver(battery_cell=b_cell)
sol = solver.solveSPKF(sol_exp=sol_exp, cov_soc=1e-6, cov_current=1e-6, cov_sensor=1e-6, cov_process=1e-6,
                       V_min=V_min, V_max=V_max, SOC_LIB_min=SOC_LIB_min, SOC_LIB_max=SOC_LIB_max, SOC_LIB=soc_init)

print(sol.mse(sol_exp=sol_exp))

sol.comprehensive_plot(sol_exp=sol_exp)
# sol_exp.plot_tiv()
#
# print(sol_exp.array_t)