""" thermal_solver
Contains the classes and functionailites to solver for the thermal model.
"""

__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2023 by Moin Ahmed. All rights are reserved.'
__status__ = 'developement'

from src.calc_helpers.ode_solvers import rk4
from src.models.thermal import ECMLumped


def calc_cell_temp(t_prev: float, dt: float, temp_prev: float, v: float, i_app: float, rho: float, vol: float,
                   c_p: float, ocv: float, docvdtemp: float, h: float, area: float, temp_amb: float) -> float:
    """
    Solves for the heat balance using the ODE rk4 solver for the ECM model.
    :param t_prev: time at the previous time step [s]
    :param dt: time difference between the current and the previous time steps [s]
    :param temp_prev: temperature at the previous time step [K]
    :param v: Battery cell potential at the current time step [V]
    :param i_app: Applied battery current [A]
    :param rho: battery density (mostly for thermal modelling), kg/m3
    :param vol: battery cell volume, m3
    :param c_p: specific heat capacity, J / (K kg)
    :param ocv: Open-circiut potential [V]
    :param docvdtemp: change of OCV with respect to the change in temperature [V/K]
    :param h: heat transfer coefficient, J / (S K)
    :param area: surface area, m2
    :param temp_amb: ambient temperature [K]
    :return: (float) Battery cell temperature [K]
    """
    t_model = ECMLumped()
    func_heat_balance = t_model.heat_balance(v=V, i_app=i_app, rho=rho, vol=vol, c_p=c_p, ocv=ocv, docvdtemp=docvdtemp,
                                             h=h, area=area,temp_amb=temp_amb)
    return rk4(func=func_heat_balance, t_prev=t_prev, y_prev=temp_prev, step_size=dt)
