from parameter_sets.Calce123 import *
import src


soc_init = 0.05
charge_current = 1.65
V_max = 3.5
SOC_LIB = soc_init
SOC_LIB_max = 1.0

param = src.ParameterSet(R0=R0, R1=R1, C1=C1, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)
b_cell = src.BatteryCell(param=param, soc_init=soc_init)
cycling_step = src.ChargeStep(charge_current=charge_current, V_max=V_max,
                              SOC_LIB_max=SOC_LIB_max, SOC_LIB=SOC_LIB)

solver = src.DTSolver(battery_cell=b_cell)
sol = solver.solve(cycling_step=cycling_step, dt=0.1)

sol.comprehensive_plot()  # plot the results

