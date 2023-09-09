import pandas as pd

from parameter_sets.Calce123 import *
import src


# Read experimental data below
# t_lim_index = 10000
df = pd.read_csv('A1-A123-Dynamics.csv')
df['Test_Time(s)'] = df['Test_Time(s)'] - df['Test_Time(s)'].iloc[0]
t = df['Test_Time(s)'].to_numpy()
I = df['Current(A)'].to_numpy()
V = df['Voltage(V)'].to_numpy()

# simulation parameters are below
soc_init = 0.95
V_min = 2.5
V_max = 3.65
SOC_LIB = soc_init
SOC_LIB_min = 0.0
SOC_LIB_max = 1.0

param = src.ParameterSet(R0=R0, R1=R1, C1=C1, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)
b_cell = src.BatteryCell(param=param, soc_init=soc_init)
cycle_step = src.CustomStep(array_t=t, array_I=I,
                            V_min=V_min, V_max=V_max, SOC_LIB_min=SOC_LIB_min, SOC_LIB_max=SOC_LIB_max, SOC_LIB=SOC_LIB)

solver = src.DTSolver(battery_cell=b_cell)
sol = solver._solve_custom_step(cycling_step=cycle_step, dt=10)

sol.comprehensive_plot()  # plot the results