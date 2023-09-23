""" thermal.py
Contains classes and functionality for thermal battery cell model
"""

__all__ = ['ECMLumped']

__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2023 by Moin Ahmed. All rights reserved.'
__status__ = 'developement'

from typing import Callable


class ECMLumped:
    """
    Contains equations for conducting the lumped thermal battery cell model
    """
    def reversible_heat(self, i_app: float, temp: float, docvdtemp: float) -> float:
        return i_app * temp * docvdtemp

    def irreversible_heat(self, i_app: float, v: float, ocv: float) -> float:
        return i_app * (v - ocv)

    def heat_flux(self, temp: float, h: float, area: float, temp_amb: float):
        return h * area * (temp - temp_amb)

    def heat_balance(self, v: float, i_app: float, rho: float, vol: float, c_p: float,
                     ocv: float, docvdtemp, h, area, temp_amb) -> Callable:
        def func_heat_balance(temp: float, t: float) -> float:
            main_coeff = 1 / (rho * vol * c_p)
            return main_coeff * (self.reversible_heat(i_app=i_app, temp=temp, docvdtemp=docvdtemp) + \
                                 self.irreversible_heat(i_app=i_app, v=v, ocv=ocv) - \
                                 self.heat_flux(temp=temp, h=h, area=area, temp_amb=temp_amb))
        return func_heat_balance