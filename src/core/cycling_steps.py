""" cycling_steps
Contains the class and functionalities for the cycling steps
"""

__all__ = ['BaseCyclingStep', 'DischargeStep', 'ChargeStep', 'RestStep', 'CustomStep']

__author__ = 'Moin Ahmed'
__copyright__ = 'Copywrite 2023 by Moin Ahmed. All rights reserved.'
__status__ = 'development'


import abc
from dataclasses import dataclass, field
from typing import Optional

import numpy as np


@dataclass
class BaseCyclingStep(metaclass=abc.ABCMeta):
    """
    Abstract parent class for various battery cell cycling protocols.
    """
    time_elapsed: float = field(default=0.0)
    SOC_LIB: float = field(default=1.0)
    SOC_LIB_min: float = field(default=0.0)
    SOC_LIB_max: float = field(default=1.0)
    SOC_LIB_init: float = field(default=1.0)
    charge_current: Optional[float] = field(default=None)
    discharge_current: Optional[float] = field(default=None)
    rest_time: Optional[float] = field(default=None)
    V_max: Optional[float] = field(default=None)
    V_min: Optional[float] = field(default=None)
    cycle_step_name: Optional[str] = field(default=None)

    def get_current(self, step_name: str, t: float) -> float:
        """
        Returns the current for a particular cycling step. It is only valid for constant current situations.
        :param step_name: (string) The cycling step name.
        :param t: (float) the time value at the current time step [s]
        :return: (double) The current value.
        """
        if step_name == "rest":
            return 0.0
        elif step_name == "charge":
            return self.charge_current
        elif step_name == "discharge":
            return self.discharge_current
        else:
            raise TypeError("Not a valid step name")

    def reset(self) -> None:
        """
        Resets the cycler instance
        :return: None
        """
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init


class DischargeStep(BaseCyclingStep):
    """
    Battery Cycler with the discharge step only
    """
    def __init__(self, discharge_current: float, V_min: float, SOC_LIB_min: float, SOC_LIB: float) -> None:
        super().__init__(discharge_current=-discharge_current, V_min=V_min, SOC_LIB_min=SOC_LIB_min,
                         SOC_LIB=SOC_LIB)
        self.num_cycle = 1
        self.cycle_step_name = 'discharge'
        self.SOC_LIB_init = SOC_LIB


class ChargeStep(BaseCyclingStep):
    """
    Battery Cycler with the charge cycling step only
    """
    def __init__(self, charge_current: float, V_max: float, SOC_LIB_max: float, SOC_LIB: float) -> None:
        super().__init__(charge_current=charge_current, V_max=V_max, SOC_LIB=SOC_LIB, SOC_LIB_max=SOC_LIB_max)
        self.num_cycle = 1
        self.cycle_step_name = 'charge'
        self.SOC_LIB_init = SOC_LIB


class RestStep(BaseCyclingStep):
    """
    Battery rest cycling step where no current is applied and lasts until the inputted rest time
    """
    def __init__(self, rest_time: float, SOC_LIB: float) -> None:
        super().__init__(rest_time=rest_time, SOC_LIB=SOC_LIB)
        self.cycle_step_name = 'rest'
        self.SOC_LIB_init = self.SOC_LIB


class CustomStep:
    pass