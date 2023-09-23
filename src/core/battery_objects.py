""" battery_objects
Provides classes and functionality for the core objects used by the equivalent circuit solvers
"""

__all__ = ['ParameterSet', 'BatteryCell']

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by Moin Ahmed. All rights reserved.'
__status__ = 'deployed'

from typing import Optional, Callable
import abc
from dataclasses import dataclass, field

import numpy as np

from src.exceptions_and_warnings.exceptions import CannotPerformCalculations
from src.calc_helpers import constants


def check_for_float_type(value: Optional[float]) -> None:
    """
    Checks for the instance of the input value and raise TypeError if it is not a float.
    :param value: input value
    :return: None
    """
    if not isinstance(value, float):
        raise TypeError(f"inputted value needs to be a None or float type. Provided {value}")


def check_for_callable_type(func: Optional[Callable]) -> None:
    if not callable(func):
        raise TypeError


class ParameterSet:
    """
    Contains the variables for the ECM models
    """
    # Below are the parameters for the isothermal parameters
    _R0_ref = None
    _R1_ref = None
    _C1 = None
    _Q = None

    _V_min = None
    _V_max = None

    _func_SOC_OCV = None
    _func_eta = None

    # parameters below are required for the thermal modelling
    _Ea_R0 = None
    _Ea_R1 = None
    _T_ref = None
    _rho = None
    _vol = None
    _c_p = None
    _h = None
    _A = None

    _func_docvdtemp = None

    def _get_Ea_R0(self) -> Optional[float]:
        return self._Ea_R0

    def _get_Ea_R1(self) -> Optional[float]:
        return self._Ea_R1

    def _get_R0_ref(self) -> Optional[float]:
        return self._R0_ref

    def _get_R1_ref(self) -> Optional[float]:
        return self._R1_ref

    def _get_C1(self) -> Optional[float]:
        return self._C1

    def _get_cap(self) -> Optional[float]:
        return self._Q

    def _get_func_SOC_OCV(self) -> Optional[Callable]:
        return self._func_SOC_OCV

    def _get_func_eta(self) -> Optional[Callable]:
        return self._func_eta

    def _get_V_min(self) -> Optional[float]:
        return self._V_min

    def _get_V_max(self) -> Optional[float]:
        return self._V_max

    def _get_T_ref(self) -> Optional[float]:
        return self._T_ref

    def _get_rho(self) -> Optional[float]:
        return self._rho

    def _get_vol(self) -> Optional[float]:
        return self._vol

    def _get_c_p(self) -> Optional[float]:
        return self._c_p

    def _get_h(self) -> Optional[float]:
        return self._h

    def _get_A(self) -> Optional[float]:
        return self._A

    def _get_func_docvdtemp(self) -> Optional[Callable]:
        return self._func_docvdtemp

    def _set_Ea_R0(self, Ea_R0: float) -> None:
        self._Ea_R0 = Ea_R0

    def _set_Ea_R1(self, Ea_R1: float) -> None:
        self._Ea_R1 = Ea_R1

    def _set_R0_ref(self, R0_ref: float) -> None:
        """
        Sets the instance's R0 [ohms] variable
        :param R0: resistance value [ohms]
        :return: None
        """
        check_for_float_type(value=R0_ref)
        self._R0 = R0_ref

    def _set_R1_ref(self, R1_ref: float) -> None:
        """
        Sets the instance's R1 [ohms] value
        :param R1: resistance value [ohms]
        :return: None
        """
        check_for_float_type(value=R1_ref)
        self._R1 = R1_ref

    def _set_C1(self, C1: float) -> None:
        """
        Sets the instance's C1 value
        :param C1: capacitance value [Farads]
        :return: None
        """
        check_for_float_type(value=C1)
        self._C1 = C1

    def _set_Q(self, cap: float) -> None:
        """
        Sets the battery cell capacity [A hr]
        :param cap: the battery cell capacity [A hr]
        """
        check_for_float_type(value=cap)
        self._Q = cap

    def _set_func_SOC_OCV(self, func_SOC_OCV: Callable) -> None:
        check_for_callable_type(func_SOC_OCV)
        self._func_SOC_OCV = func_SOC_OCV

    def _set_func_eta(self, func_eta: Callable) -> None:
        check_for_callable_type(func_eta)
        self._func_eta = func_eta

    def _set_V_min(self, v_min: float) -> None:
        check_for_float_type(v_min)
        self._V_min = v_min

    def _set_V_max(self, v_max: float) -> None:
        check_for_float_type(v_max)
        self._V_min = v_max

    def _set_T_ref(self, temp_ref: float) -> None:
        check_for_float_type(temp_ref)
        self._T_ref = temp_ref

    def _set_rho(self, rho: float) -> None:
        check_for_float_type(rho)
        self._rho = rho

    def _set_vol(self, vol: float) -> None:
        check_for_float_type(vol)
        self._vol = vol

    def _set_c_p(self, c_p: float) -> None:
        check_for_float_type(c_p)
        self._c_p = c_p

    def _set_h(self, h: float) -> None:
        check_for_float_type(h)
        self._h = h

    def _set_A(self, area: float) -> None:
        check_for_float_type(area)
        self._A = area

    def _set_func_docvdtemp(self, func_docvdtemp) -> None:
        check_for_callable_type(func_docvdtemp)
        self._func_docvdtemp = func_docvdtemp

    def _del_Ea_R0(self) -> None:
        self._Ea_R0 = None

    def _del_Ea_R1(self) -> None:
        self._Ea_R1 = None

    def _del_R0_ref(self) -> None:
        self._R0_ref = None

    def _del_R1_ref(self) -> None:
        self._R1_ref = None

    def _del_C1(self) -> None:
        self._C1 = None

    def _del_cap(self) -> None:
        self._Q = None

    def _del_func_SOC_OCV(self) -> None:
        self._func_SOC_OCV = None

    def _del_func_eta(self) -> None:
        self._func_eta = None

    def _del_V_min(self) -> None:
        self._V_min = None

    def _del_V_max(self) -> None:
        self._V_min = None

    def _del_T_ref(self) -> None:
        self._T_ref = None

    def _del_rho(self) -> None:
        self._rho = None

    def _del_vol(self) -> None:
        self._vol = None

    def _del_c_p(self) -> None:
        self._c_p = None

    def _del_h(self) -> None:
        self._h = None

    def _del_A(self) -> None:
        self._A = None

    def _del_func_docvdtemp(self) -> None:
        self._func_docvdtemp = None

    R0_ref = property(_get_R0_ref, _set_R0_ref, _del_R0_ref, 'gets, sets, or deletes the R0.')
    R1_ref = property(_get_R1_ref, _set_R1_ref, _del_R1_ref, 'gets, sets, or deletes the R1.')
    C1 = property(_get_C1, _set_C1, _del_C1, 'gets, sets, or deletes the C1.')
    Q = property(_get_cap, _set_Q, _del_cap, 'gets, sets, or deletes the battery cell capacity.')
    func_SOC_OCV = property(_get_func_SOC_OCV, _set_func_SOC_OCV, _del_func_SOC_OCV,
                            'gets, sets, or deletes the func_SOC_OCV')
    func_eta = property(_get_func_eta, _set_func_eta, _del_func_eta,
                        'gets, sets, or deletes the func_eta')

    V_min = property(_get_V_min, _set_V_min, _del_V_min, 'gets, sets, or deletes the battery cell max. potential')
    V_max = property(_get_V_max, _set_V_max, _del_V_max, 'gets, sets, or deletes the battery cell min. potential')
    T_ref = property(_get_T_ref, _set_T_ref, _del_T_ref, 'gets, sets, or deletes the battery cell reference '
                                                         'temperature.')
    Ea_R0 = property(_get_Ea_R0, _set_Ea_R0, _del_Ea_R0, 'get sets, or deletes the activation energy for R0.')
    Ea_R1 = property(_get_Ea_R1, _set_Ea_R1, _del_Ea_R1, 'gets, sets, or deletes the activation energy for R1.')
    rho = property(_get_T_ref, _set_T_ref, _del_T_ref, 'gets, sets, or deletes the battery cell rho')
    c_p = property(_get_rho, _set_rho, _del_rho, 'gets, sets, or deletes the battery cell specific heat capacity.')
    h = property(_get_h, _set_h, _del_h, 'gets, sets, or deletes the heat transfer co-efficient')
    A = property(_get_A, _set_A, _del_A, 'gets, sets, or deletes the battery cell surface area')

    func_docvdtemp = property(_get_func_docvdtemp, _set_func_docvdtemp, _del_func_docvdtemp,
                              'gets, sets, or deletes the function representing the change of battery cell ocv with'
                              'temp')

    def __init__(self, r0_ref: float, r1_ref: float, c1: float, cap: float, func_SOC_OCV: Callable, func_eta: Callable,
                 ea_r0: float, ea_r1: float, v_min: float, v_max: float, temp_ref: float,
                 rho: float, c_p: float, h: float, area: float, func_dcvdtemp: float):
        self._set_R0_ref(R0_ref=r0_ref)
        self._set_R1_ref(R1_ref=r1_ref)
        self._set_C1(C1=c1)
        self._set_Q(cap=cap)
        self._set_func_SOC_OCV(func_SOC_OCV=func_SOC_OCV)
        self._set_func_eta(func_eta=func_eta)

        self._set_Ea_R0(ea_r0=ea_r0)
        self._set_Ea_R1(ea_r1=ea_r1)
        self._set_V_min(v_min=v_min)
        self._set_V_max(v_max=v_max)
        self._set_T_ref(temp_ref=temp_ref)
        self._set_rho(rho=rho)
        self._set_c_p(c_p=c_p)
        self._set_h(h=h)
        self._set_A(area=area)
        self._func_docvdtemp(func_dcvdtemp=func_dcvdtemp)

    def calc_R0(self, temp: float):
        return self.R0_ref * np.exp(-1 * self.Ea_R0 / constants.Constants.R * (1 / temp - 1 / self.T_ref))

    def calc_R1(self, temp: float):
        return self.R0_ref * np.exp(-1 * self.Ea_R1 / constants.Constants.R * (1 / temp - 1 / self.T_ref))


class BatteryCell:
    """
    Contains the battery cell and thermal parameters and methods necessary for ECM simulations
    """
    _param = None
    _SOC = None

    def _get_param(self) -> Optional[ParameterSet]:
        return self._param

    def _get_SOC(self) -> Optional[float]:
        return self._SOC

    def _set_param(self, param: ParameterSet) -> None:
        """
        Sets the class param variable to the inputed param object
        :param param: ParameterSet object
        :return: None
        """
        self._param = param

    def _set_SOC(self, soc: float) -> None:
        """
        Sets the class instances SOC to the SOC
        :param SOC: state-of-charge of the battery cell
        :return:
        """
        check_for_float_type(soc)
        self._SOC = soc

    def _del_param(self) -> None:
        self._param = None

    def _del_SOC(self) -> None:
        self._SOC = None

    @property
    def ocv(self) -> Optional[float]:
        """
        Open circuit potential.
        :return:
        """
        if self._param.func_SOC_OCV:
            if self._SOC:
                return self._param.func_SOC_OCV(self._SOC)
            else:
                raise CannotPerformCalculations('SOC is none.')
        else:
            raise CannotPerformCalculations('The SOC-OCV function is not defined.')

    param = property(_get_param, _set_param, _del_param, 'gets, sets, or deletes the instance param object.')
    soc = property(_get_SOC, _set_SOC, _del_SOC, 'gets, sets, or deletes the instance soc.')

    def __init__(self, param: ParameterSet, soc_init: float):
        self._set_param(param=param)
        self._set_SOC(soc=soc_init)
        self.soc_init = soc_init


if __name__ == '__main__':
    pass