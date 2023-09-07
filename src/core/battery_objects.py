""" battery_objects
Provides classes and functionality for the core objects used by the equivalent circuit solvers
"""

#######################################
# Create an "__all__" list to support #
#######################################

__all__ = ['ParameterSet', 'BatteryCell']

#######################################
# Module metadata/dunder-names        #
#######################################

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by Moin Ahmed. All rights reserved.'
__status__ = 'developement'

#######################################
# Standard library imports needed     #
#######################################

from typing import Optional, Callable

#######################################
# Third-party imports needed          #
#######################################

#######################################
# Local imports needed                #
#######################################

from src.exceptions_and_warnings.exceptions import CannotPerformCalculations

#######################################
# Initialization needed before member #
#   definition can take place         #
#######################################

#######################################
# Module-level Constants              #
#######################################

#######################################
# Custom Exceptions                   #
#######################################

#######################################
# Module functions                    #
#######################################

def check_for_float_type(value: Optional[float]) -> None:
    """
    Checks for the instance of the input value and raise TypeError if it is not a float.
    :param value: input value
    :return: None
    """
    if not isinstance(value, (float)):
        raise TypeError(f"inputted value needs to be a None or float type. Provided {value}")


def check_for_callable_type(func: Optional[Callable]) -> None:
    if not callable(func):
        raise TypeError

#######################################
# ABC "interface" classes             #
#######################################

#######################################
# Abstract classes                    #
#######################################

#######################################
# Concrete classes                    #
#######################################

class ParameterSet:
    """
    Contains the variables for the ECM models
    """
    ###################################
    # Class attributes/constants      #
    ###################################
    _R0 = None
    _R1 = None
    _C1 = None
    _func_SOC_OCV = None

    ###################################
    # Property-getter methods         #
    ###################################

    def _get_R0(self) -> Optional[float]:
        return self._R0

    def _get_R1(self) -> Optional[float]:
        return self._R1

    def _get_C1(self) -> Optional[float]:
        return self._C1

    def _get_func_SOC_OCV(self) -> Optional[Callable]:
        return self._func_SOC_OCV

    ###################################
    # Property-setter methods         #
    ###################################

    def _set_R0(self, R0: float) -> None:
        """
        Sets the instance's R0 [ohms] variable
        :param R0: resistance value [ohms]
        :return: None
        """
        check_for_float_type(value=R0)
        self._R0 = R0

    def _set_R1(self, R1: float) -> None:
        """
        Sets the instance's R1 [ohms] value
        :param R1: resistance value [ohms]
        :return: None
        """
        check_for_float_type(value=R1)
        self._R1 = R1

    def _set_C1(self, C1: float) -> None:
        """
        Sets the instance's C1 value
        :param C1: capacitance value [Farads]
        :return: None
        """
        check_for_float_type(value=C1)
        self._C1 = C1

    def _set_func_SOC_OCV(self, func_SOC_OCV) -> None:
        check_for_callable_type(func_SOC_OCV)
        self._func_SOC_OCV = func_SOC_OCV

    ###################################
    # Property-deleter methods        #
    ###################################

    def _del_R0(self) -> None:
        self._R0 = None

    def _del_R1(self) -> None:
        self.R1 = None

    def _del_C1(self) -> None:
        self._C1 = None

    def _del_func_SOC_OCV(self) -> None:
        self._func_SOC_OCV = None

    ###################################
    # Instance property definitions   #
    ###################################

    R0 = property(_get_R0, _set_R0, _del_R0, 'gets, sets, or deletes the R0.')
    R1 = property(_get_R1, _set_R1, _del_R1, 'gets, sets, or deletes the R1.')
    C1 = property(_get_C1, _set_C1, _del_C1, 'gets, sets, or deletes the C1.')
    func_SOC_OCV = property(_get_func_SOC_OCV, _set_func_SOC_OCV, _del_func_SOC_OCV,
                            'gets, sets, or deletes the func_SOC_OCV')

    ###################################
    # Object initialization           #
    ###################################

    def __init__(self, R0: float, R1: float, C1: float, func_SOC_OCV: Callable):
        self._set_R0(R0=R0)
        self._set_R1(R1=R1)
        self._set_C1(C1=C1)
        self._set_func_SOC_OCV(func_SOC_OCV=func_SOC_OCV)

    ###################################
    # Object deletion                 #
    ###################################

    ###################################
    # Instance methods                #
    ###################################

    ###################################
    # Overrides of built-in methods   #
    ###################################

    ###################################
    # Class methods                   #
    ###################################

    ###################################
    # Static methods                  #
    ###################################


class BatteryCell:
    """
    Contains the parameters and methods necessary for ECM simulations
    """

    ###################################
    # Class attributes/constants      #
    ###################################
    _param = None
    _SOC = None

    ###################################
    # Property-getter methods         #
    ###################################
    def _get_param(self) -> Optional[ParameterSet]:
        return self._param

    def _get_SOC(self) -> Optional[float]:
        return self._SOC

    ###################################
    # Property-setter methods         #
    ###################################

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

    ###################################
    # Property-deleter methods        #
    ###################################

    def _del_param(self) -> None:
        self._param = None

    def _del_SOC(self) -> None:
        self._SOC = None

    ###################################
    # Instance property definitions   #
    ###################################

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

    ###################################
    # Object initialization           #
    ###################################
    def __init__(self, param: ParameterSet, soc_init: float):
        self._set_param(param=param)
        self._set_SOC(soc=soc_init)
        self.soc_init = soc_init






#######################################
# Initialization needed after member  #
#   definition is complete            #
#######################################

#######################################
# Imports needed after member         #
#   definition (to resolve circular   #
#   dependencies - avoid if at all    #
#   possible                          #
#######################################

#######################################
# Code to execute if the module is    #
#   called directly                   #
#######################################

if __name__ == '__main__':
    pass