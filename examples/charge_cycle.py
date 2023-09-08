import src


R0 = 0.02
R1 = 0.05
C1 = 0.003
Q = 1.65
soc_init = 0.05

charge_current = 1.65
V_max = 3.5
SOC_LIB = soc_init
SOC_LIB_max = 1.0


def func_SOC_OCV(soc):
    a, b, c, d, e, f, g, h, i, j, k, l, m = \
    [3.39803735e+04, -1.86083253e+05, 4.40650925e+05, -5.86500338e+05,
     4.74171271e+05, -2.29840038e+05, 5.53052667e+04, 3.05616190e+03,
     -6.45471514e+03,  1.99278174e+03, -2.99381888e+02, 2.29345284e+01,
     2.53496894e+00]

    return a * soc ** 12 + b * soc ** 11 + c * soc ** 10 + \
           d * soc ** 9 + e * soc ** 8 + f * soc ** 7 + \
           g * soc ** 6 + h * soc ** 5 + i * soc ** 4 + \
           j * soc ** 3 + k * soc ** 2 + l * soc + m


def func_eta(i):
    return 1 if i <= 0 else 0.9995


param = src.ParameterSet(R0=R0, R1=R1, C1=C1, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)
b_cell = src.BatteryCell(param=param, soc_init=soc_init)
cycling_step = src.ChargeStep(charge_current=charge_current, V_max=V_max,
                              SOC_LIB_max=SOC_LIB_max, SOC_LIB=SOC_LIB)

solver = src.DTSolver(battery_cell=b_cell)
sol = solver.solve(cycling_step=cycling_step, dt=0.1)

sol.comprehensive_plot()  # plot the results

