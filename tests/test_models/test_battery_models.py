"""
Provides the unittests for the ECM model objects.
"""

import unittest

from src.models.battery import Thevenin1RC


class TestThevenin1RC(unittest.TestCase):
    dt = 0.1
    i_app = 1.656
    SOC_prev = 0.5
    Q = 1.656
    eta = 1
    i_R1_prev = 0.0
    R0 = 0.002
    R1 = 0.02
    C1 = 50
    OCV = 3.8

    def test_soc_next(self):
        res1 = Thevenin1RC.soc_next(dt=self.dt, i_app=self.i_app, SOC_prev=self.SOC_prev, Q=self.Q, eta=self.eta)
        self.assertEqual(0.4999722222222222, res1)

    def test_ir1_next(self):
        res1 = Thevenin1RC.i_R1_next(dt=self.dt, i_app=self.i_app, i_R1_prev=0.0, R1=self.R1, C1=self.C1)
        self.assertEqual(0.15758923573245104, res1)

    def test_v(self):
        res1 = Thevenin1RC.v(i_app=self.i_app, OCV=self.OCV, R0=self.R0, R1=self.R1, i_R1=0.15758923573245104)
        self.assertEqual(3.7935362152853505, res1)

