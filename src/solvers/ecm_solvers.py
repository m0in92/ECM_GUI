""" ecm_solvers
This module provides classes and functionality to solve for LIB SOC and terminal voltage using ECM.
"""

__all__ = ['DTSolver']

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by Moin Ahmed. All rights reserved.'
__status__ = 'development'

from typing import Optional, Union

import numpy as np
import numpy.typing as npt

from src.core.battery_objects import BatteryCell
from src.core.cycling_steps import BaseCyclingStep, CustomStep
from src.models.battery import Thevenin1RC
from src.visualization.sol_and_plot_objects import Solution

from src.observers.kalman_filter import NormalRandomVector
from src.observers.kalman_filter import SPKF


class DTSolver:
    """
    This is the class that solves the ECM model equations for time and applied current arrays. It outputs the terminal
    SOC and voltage at the time steps specified by the input time array.

    The discrete time model for first-order Thevenin model is given by:

    z[k+1] = z[k] - delta_t*eta[k]*i_app[k]/capacity
    i_R1[k+1] = exp(-delta_t/(R1*C1))*i_R1[k] + (1-exp(-delta_t/(R1*C1))) * i_app[k]
    v[k] = OCV(z[k]) - R1*i_R1[k] - R0*i_app[k]

    Where k represents the time-point and delta_t represents the time-step between z[k+1] and z[k].
    """

    def __init__(self, battery_cell: BatteryCell, isothermal: bool = True) -> None:
        """
        The class constructor for the solver object.
        :params ECM_obj: (Thevenin1RC) ECM model object
        :params isothermal: (bool)
        :params t_app: (Numpy array) array of time.
        :params i_app: (Numpy array) array of applied battery current associated with the time array.
        :param v_exp: (Numpy array) array of experimental battery terminal voltage data.
        """
        if not isinstance(battery_cell, BatteryCell):
            raise TypeError("battery_cell_instance needs to be a BatteryCell type.")
        self.b_cell = battery_cell
        self.__dt = 0.0  # delta_t is required for SPKF solver.

        if isinstance(isothermal, bool):
            self.isothermal = isothermal
        else:
            raise TypeError('isothermal needs to be a bool type.')

    def __calc_v(self, dt: float, i_app: float, i_r1_prev: float) -> tuple[float, float]:
        i_r1_prev = Thevenin1RC.i_R1_next(dt=dt, i_app=i_app, i_R1_prev=i_r1_prev,
                                          R1=self.b_cell.param.R1, C1=self.b_cell.param.C1)
        v = Thevenin1RC.v(i_app=i_app, OCV=self.b_cell.param.func_SOC_OCV(self.b_cell.soc),
                          R0=self.b_cell.param.R0, R1=self.b_cell.param.R1, i_R1=i_r1_prev)
        return i_r1_prev, v

    def __solve_standard_cycling_steps(self, cycling_step: BaseCyclingStep, dt: float = 0.1) -> Solution:
        sol = Solution()  # initialize the solution object
        sol.update_arrays(t=0.0, i_app=0.0, soc=self.b_cell.soc, v=self.b_cell.param.func_SOC_OCV(self.b_cell.soc),
                          cap_discharge=0.0)

        t_prev = 0.0  # [s]
        i_r1_prev = 0.0  # [A]
        step_completed = False
        cap_discharge = 0.0  # [A hr]
        while not step_completed:
            t_curr = t_prev + dt
            i_app = cycling_step.get_current(step_name=cycling_step.cycle_step_name, t=t_curr)
            i_app_prev = cycling_step.get_current(step_name=cycling_step.cycle_step_name, t=t_prev)

            # break condition for the rest cycling step
            if cycling_step.cycle_step_name == 'rest' and t_curr > cycling_step.rest_time:
                step_completed = True

            # Calculate the SOC (and update the battery cell attribute), i_R1 [A], and v[V] for the current time step
            self.b_cell.soc = Thevenin1RC.soc_next(dt=dt, i_app=i_app_prev, SOC_prev=self.b_cell.soc,
                                                   Q=self.b_cell.param.Q,
                                                   eta=self.b_cell.param.func_eta(self.b_cell.soc))
            i_r1_prev, v = self.__calc_v(dt=dt, i_app=i_app, i_r1_prev=i_r1_prev)

            # loop termination criteria
            if (cycling_step.cycle_step_name == "charge") and (v > cycling_step.V_max):
                step_completed = True
            if (cycling_step.cycle_step_name == "discharge") and (v < cycling_step.V_min):
                step_completed = True

            # update the sol object
            cap_discharge = sol.calc_cap_discharge(cap_discharge_prev=cap_discharge, i_app=i_app, dt=dt)
            sol.update_arrays(t=t_curr, i_app=-i_app, soc=self.b_cell.soc, v=v, cap_discharge=cap_discharge)
            t_prev = t_curr
        return sol

    def __solve_custom_step(self, cycling_step: CustomStep, dt: float):
        sol = Solution()  # initialize the solution object
        sol.update_arrays(t=0.0, i_app=0.0, soc=self.b_cell.soc, v=self.b_cell.param.func_SOC_OCV(self.b_cell.soc),
                          cap_discharge=0.0)

        t_prev = 0.0  # [s]
        i_r1_prev = 0.0  # [A]
        step_completed = False
        cap_discharge = 0.0  # [A hr]

        while not step_completed:
            t_curr = t_prev + dt
            i_app_prev = cycling_step.get_current(step_name=cycling_step.cycle_step_name, t=t_prev)
            i_app_curr = cycling_step.get_current(step_name=cycling_step.cycle_step_name, t=t_curr)

            # Calculate the SOC (and update the battery cell attribute), i_R1 [A], and v[V] for the current time step
            self.b_cell.soc = Thevenin1RC.soc_next(dt=dt, i_app=i_app_prev, SOC_prev=self.b_cell.soc,
                                                   Q=self.b_cell.param.Q,
                                                   eta=self.b_cell.param.func_eta(self.b_cell.soc))
            i_r1_prev, v = self.__calc_v(dt=dt, i_app=i_app_curr, i_r1_prev=i_r1_prev)

            # loop termination criteria
            if v > cycling_step.V_max:
                step_completed = True
            if v < cycling_step.V_min:
                step_completed = True
            if t_curr > cycling_step.array_t[-1]:
                step_completed = True

            # update the sol object
            cap_discharge = sol.calc_cap_discharge(cap_discharge_prev=cap_discharge, i_app=i_app_curr, dt=dt)
            sol.update_arrays(t=t_curr, i_app=i_app_curr, soc=self.b_cell.soc, v=v, cap_discharge=cap_discharge)
            t_prev = t_curr
        return sol

    def solve(self, cycling_step: BaseCyclingStep, dt: float = 0.1) -> Solution:
        if isinstance(cycling_step, CustomStep):
            return self.__solve_custom_step(cycling_step=cycling_step, dt=dt)
        else:
            return self.__solve_standard_cycling_steps(cycling_step=cycling_step, dt=dt)

    def __func_f(self, x_k: npt.ArrayLike, u_k: Union[float, npt.ArrayLike], w_k: npt.ArrayLike):
        """
        State Equation.
        :param x_k: the vector containing the system state.
        :param u_k: the input (applied current in case of isothermal condition) variable
        :param w_k: the vector representing the process noise.
        :return: the vector representing the state
        """
        R1 = self.b_cell.param.R1
        C1 = self.b_cell.param.C1
        Q = self.b_cell.param.Q
        m1 = np.array([[1, 0], [0, np.exp(-self.__dt / (R1 * C1))]])
        m2 = np.array([[-self.__dt / (3600 * Q)], [1 - np.exp(-self.__dt / (R1 * C1))]])
        return m1 @ x_k + m2 * (u_k + w_k)

    def __func_h(self, x_k: npt.ArrayLike, u_k: Union[float, npt.ArrayLike], v_k: npt.ArrayLike):
        """
        Output Equation.
        :param x_k: the system state vector.
        :param u_k: the vector (or float in case of a single input) containing the system input
        :param v_k: the vector representing the sensor noise
        :return: the system output vector
        """
        return self.b_cell.param.func_SOC_OCV(x_k[0, :]) - self.b_cell.param.R1 * x_k[1, :] - \
               self.b_cell.param.R0 * u_k + v_k

    def solveSPKF(self, sol_exp: Solution, cov_soc: float, cov_current: float, cov_process: float, cov_sensor: float,
                  V_min, V_max, SOC_LIB_min, SOC_LIB_max, SOC_LIB) -> Solution:
        """
        Performs the Thevenin equivalent circuit model using the sigma point kalman filter
        :param sol_exp: Solution object from the experimental data.
        :param cov_soc: covariance of the soc
        :param cov_current: covariance of i_r1
        :param cov_process: covariance of the system process
        :param cov_sensor: covariance of the voltage sensor
        :param V_min: threshold cell terminal voltage [V]
        :param V_max: threshold cell terminal voltage [V]
        :param SOC_LIB_min: minimum LIB SOC
        :param SOC_LIB_max: maximum LIB SOC
        :param SOC_LIB: LIB SOC
        :return: (Solution) Solution object containing the results from the simulations.
        """
        sol = Solution()  # initialize the solution object

        cycling_step = CustomStep(sol_exp.array_t, sol_exp.array_I,
                                  V_min, V_max, SOC_LIB_min, SOC_LIB_max,
                                  SOC_LIB)  # current is added to the cycler object.
        array_y_true = sol_exp.array_V  # y_true is extracted from the solution object

        # create Normal Random Variables below
        i_r1_init = 0.0  # [A]
        vector_x = np.array([[self.b_cell.soc], [i_r1_init]])
        cov_x = np.array([[cov_soc, 0], [0, cov_current]])
        vector_w = np.array([[0]])
        cov_w = np.array([[cov_process]])
        vector_v = np.array([[0]])
        cov_v = np.array([[cov_sensor]])

        x = NormalRandomVector(vector_init=vector_x, cov_init=cov_x)
        w = NormalRandomVector(vector_init=vector_w, cov_init=cov_w)
        v = NormalRandomVector(vector_init=vector_v, cov_init=cov_v)

        # Create SPKF variable below
        instance_spkf = SPKF(x=x, w=w, v=v, y_dim=1, func_f=self.__func_f, func_h=self.__func_h)

        # The solution loop is run below
        t_prev = 0.0  # [s]
        step_completed = False
        # cap_discharge = 0.0  # [A hr]

        i = 1
        while not step_completed:
            t_curr = cycling_step.array_t[i]
            self.__dt = t_curr - t_prev
            i_app_prev = cycling_step.array_I[i-1]
            i_app_curr = cycling_step.array_I[i]

            instance_spkf.solve(u=i_app_prev, y_true=array_y_true[i])

            self.b_cell.soc = instance_spkf.x.get_vector()[0, 0]
            i_r1 = instance_spkf.x.get_vector()[1, 0]
            v = self.__calc_v(dt=self.__dt, i_app=i_app_curr, i_r1_prev=i_r1)[1]

            # loop termination criteria
            if v > cycling_step.V_max:
                step_completed = True
            if v < cycling_step.V_min:
                step_completed = True
            if t_curr > cycling_step.array_t[-1]:
                step_completed = True
            if i >= len(cycling_step.array_t) - 1:
                step_completed = True

            # update sol attributes
            sol.update_arrays(t=t_curr, i_app=i_app_curr, soc=self.b_cell.soc, v=v, cap_discharge=0.0)

            # update simulation parameters
            t_prev = t_curr
            i += 1

        return sol

    def solveHybridSPKF(self, dt: float):
        """
        Simulates using sigma-point kalman filter if the simulation time coincides with the experimentatl time, else it
        simulates using the regular Thevenin model.
        :param dt: time difference between calculation time step. If set to None, then the time difference
        from the experimental is used for each time step.
        :return:
        """
        pass
