import src

import matplotlib.pyplot as plt


R0 = 0.02
R1 = 0.05
C1 = 0.003
Q = 1.65
soc_init = 1.0

discharge_current = 1.65
V_min = 3.0
SOC_LIB = 1.0
SOC_LIB_min = 0.0


def func_SOC_OCV(soc):
    a, b, c, d, e = [0.08367763, 1.41222269, -2.34418315, 1.24012816, 3.12778336]
    return a * soc ** 4 + b * soc ** 3 + c * soc ** 2 + d * soc + e


def func_eta(i):
    return 1 if i <= 0 else 0.9995


param = src.ParameterSet(R0=R0, R1=R1, C1=C1, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)
b_cell = src.BatteryCell(param=param, soc_init=soc_init)
cycler_instance = src.DischargeCycler(discharge_current=discharge_current, V_min=V_min,
                                      SOC_LIB_min=SOC_LIB_min, SOC_LIB=SOC_LIB)

solver = src.DTSolver(battery_cell_instance=b_cell)
sol = solver.solve(cycler_instance=cycler_instance, dt=0.1)

sol.comprehensive_plot()  # plot the results

