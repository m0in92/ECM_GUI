import pandas as pd

from parameter_sets.Calce123 import *
import src


# Read experimental data below
sol_exp = src.Solution().read_from_csv_file(filepath='A1-A123-Dynamics.csv')

# simulation parameters are below
soc_init = 0.38775
V_min = 2
V_max = 4
SOC_LIB = soc_init
SOC_LIB_min = 0.0
SOC_LIB_max = 1.0

param = src.ParameterSet(R0=R0, R1=R1, C1=C1, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)
b_cell = src.BatteryCell(param=param, soc_init=soc_init)
cycle_step = src.CustomStep(array_t=sol_exp.array_t, array_I=sol_exp.array_I,
                            V_min=V_min, V_max=V_max, SOC_LIB_min=SOC_LIB_min, SOC_LIB_max=SOC_LIB_max, SOC_LIB=SOC_LIB)

solver = src.DTSolver(battery_cell=b_cell)
sol = solver.solve(cycling_step=cycle_step, dt=10)

print(sol.mse(sol_exp=sol_exp))

sol.comprehensive_plot(sol_exp=sol_exp)  # plot the results