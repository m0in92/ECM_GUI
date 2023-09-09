from parameter_sets.Calce123 import *
import src



soc_init = 0.95
discharge_current = 1.65
V_min = 3.0
SOC_LIB = soc_init
SOC_LIB_min = 0.0

param = src.ParameterSet(R0=R0, R1=R1, C1=C1, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)
b_cell = src.BatteryCell(param=param, soc_init=soc_init)
cycle_step = src.DischargeStep(discharge_current=discharge_current, V_min=V_min,
                               SOC_LIB_min=SOC_LIB_min, SOC_LIB=SOC_LIB)

solver = src.DTSolver(battery_cell=b_cell)
sol = solver.solve(cycling_step=cycle_step, dt=0.1)

sol.comprehensive_plot()  # plot the results

