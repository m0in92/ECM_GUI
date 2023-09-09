"""sol_and_plot_objects
Contains the classes and functionality for the storing, preprocessing, and plotting of the simulation results.
"""

__all__ = ['Solution']

__author__ = ['Moin Ahmed']
__copyright__ = 'Copyright 2023 by Moin Ahmed. All rights reserved.'
__status__ = 'development'

from dataclasses import dataclass, field
from typing import Self, Optional

import numpy as np
import numpy.typing as npt
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.interpolate


@dataclass
class Solution:
    """
    contains the array for the relevant simulation results.
    """
    array_t: np.ndarray = field(default_factory=lambda: np.array([]))  # np array containing the time values [s]
    array_I: np.ndarray = field(default_factory=lambda: np.array([]))  # np array containing the applied current [A]
    array_soc: np.ndarray = field(default_factory=lambda: np.array([]))  # np array containing the battery cell soc
    array_V: np.ndarray = field(default_factory=lambda: np.array([]))  # np array containing the terminal potential [V]
    array_cap_discharge: np.ndarray = field(default_factory=lambda: np.array([]))  # np array containing the discharge
    # capacity [Ahr]

    @classmethod
    def read_from_csv_file(cls, filepath: str) -> Self:
        df = pd.read_csv(filepath)
        array_t = df['t [s]'].to_numpy()
        array_I = df['I [A]'].to_numpy()
        array_V = df['V [V]'].to_numpy()
        return cls(array_t=array_t, array_I=array_I, array_V=array_V)

    @classmethod
    def is_discharge(cls, i_app: float) -> bool:
        """
        Returns True if the applied current [A] leads to the battery discharge
        :param i_app: applied current [A]
        :return: (bool) True if the current leads to the battery discharge
        """
        flag = False
        if i_app < 0:
            flag = True
        return flag

    @classmethod
    def calc_cap_discharge(cls, cap_discharge_prev: float, i_app: float, dt: float) -> float:
        if cls.is_discharge(i_app=i_app):
            return cap_discharge_prev + abs(i_app * dt / 3600)
        else:
            return cap_discharge_prev

    @classmethod
    def set_matplotlib_settings(cls) -> None:
        mpl.rcParams['lines.linewidth'] = 3
        plt.rc('axes', titlesize=20)
        plt.rc('axes', labelsize=12.5)
        plt.rc('axes', labelweight='bold')
        plt.rcParams['font.size'] = 15

    def update_arrays(self, t: float, i_app: float, soc: float, v: float, cap_discharge: float) -> None:
        """
        Updates the instance's arrays with the new data values
        :param t: time value [s]
        :param i_app: applied current [A]
        :param soc: state-of-charge
        :param v: terminal voltage [V]
        :param cap_discharge: discharge capacity [A hr]
        """
        self.array_t = np.append(self.array_t, t)
        self.array_I = np.append(self.array_I, i_app)
        self.array_soc = np.append(self.array_soc, soc)
        self.array_V = np.append(self.array_V, v)
        self.array_cap_discharge = np.append(self.array_cap_discharge, cap_discharge)

    def mse(self, sol_exp: Self) -> float:
        func_v_sim = scipy.interpolate.interp1d(self.array_t, self.array_V, kind='nearest', fill_value='extrapolate')
        v_sim = func_v_sim(sol_exp.array_t)
        return np.sqrt(np.sum((v_sim - sol_exp.array_V) ** 2))

    def comprehensive_plot(self, sol_exp: Optional[Self] = None, save_dir=None) -> None:
        self.set_matplotlib_settings()
        fig = plt.figure(figsize=(6.4, 6), dpi=300)

        ax1 = fig.add_subplot(311)
        ax1.plot(self.array_t, self.array_V, label='sim')
        ax1.set_xlabel('Time [s]')
        ax1.set_ylabel('Voltage [V]')
        if sol_exp:
            ax1.plot(sol_exp.array_t, sol_exp.array_V, label='exp')
            ax1.legend()

        ax2 = fig.add_subplot(312)
        ax2.plot(self.array_t, self.array_I)
        ax2.set_xlabel('Time [s]')
        ax2.set_ylabel('Current [A]')

        ax3 = fig.add_subplot(313)
        ax3.plot(self.array_t, self.array_soc)
        ax3.set_xlabel('Time [s]')
        ax3.set_ylabel('SOC')

        if save_dir is not None:
            plt.savefig(save_dir)

        plt.tight_layout()
        plt.show()

