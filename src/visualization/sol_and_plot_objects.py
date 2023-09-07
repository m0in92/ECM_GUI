"""sol_and_plot_objects
Contains the classes and functionality for the storing the simulation results and plottng them
"""

__all__ = ['Solution']

__author__ = ['Moin Ahmed']
__copyright__ = 'Copyright 2023 by Moin Ahmed. All rights reserved.'
__status__ = 'development'

from dataclasses import dataclass, field

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


@dataclass
class Solution:
    """
    contains the array for the relevant simulation results.
    """
    array_t: np.ndarray = field(default_factory=lambda: np.array([]))  # np array containing the time values [s]
    array_I: np.ndarray = field(default_factory=lambda: np.array([]))  # np array containing the applied current [A]
    array_soc: np.ndarray = field(default_factory=lambda: np.array([]))  # np array containing the battery cell soc
    array_V: np.ndarray = field(default_factory=lambda: np.array([]))  # np array containing the terminal potential [V]

    def update_arrays(self, t: float, i_app: float, soc: float, v: float):
        self.array_t = np.append(self.array_t, t)
        self.array_I = np.append(self.array_I, i_app)
        self.array_soc = np.append(self.array_soc, soc)
        self.array_V = np.append(self.array_V, v)

    def set_matplotlib_settings(self):
        mpl.rcParams['lines.linewidth'] = 3
        plt.rc('axes', titlesize=20)
        plt.rc('axes', labelsize=12.5)
        plt.rc('axes', labelweight='bold')
        plt.rcParams['font.size'] = 15

    def comprehensive_plot(self, save_dir=None):
        self.set_matplotlib_settings()
        fig = plt.figure(figsize=(6.4, 6), dpi=300)

        ax1 = fig.add_subplot(311)
        ax1.plot(self.array_t, self.array_V)
        ax1.set_xlabel('Time [s]')
        ax1.set_ylabel('Voltage [V]')

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

