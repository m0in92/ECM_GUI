""" kalman_filter
Contains the classes and functionalities for the implementing kalman filter
"""

__all__ = ['InvalidKFMethodType', 'SPKF']

__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2023 by Moin Ahmed. All rights reserved.'
__status__ = 'Development'


from typing import Callable

import numpy as np
import numpy.typing as npt
import scipy.linalg
import matplotlib.pyplot as plt

from src.observers.random_variables import NormalRandomVector


class InvalidKFMethodType(Exception):
    def __init__(self):
        msg = "Available method type(s) available now are: CDKF"
        super().__init__(msg)


class SPKF:
    """
    The class for sigma-point Kalman filter
    """
    def __init__(self, x: NormalRandomVector, w: NormalRandomVector, v: NormalRandomVector,
                 y_dim: int,
                 func_f: Callable, func_h: Callable,
                 method_type: str = 'CDKF') -> None:
        self.x = x
        self.w = w
        self.v = v

        self.y_dim = y_dim

        self.func_f = func_f
        self.func_h = func_h

        self.Nx = self.x.get_vector().shape[0]  # number of random variables in the x vector
        self.Nw = self.w.get_vector().shape[0]  # number of random variables in the w vector
        self.Nv = self.v.get_vector().shape[0]  # number of random variables in the v vector
        self.L = (self.Nx + self.Nw + self.Nv)  # dimensions of the augmented covariance state matrix.
        self.p = 2 * self.L  # number of sigma points - 1

        if method_type != 'CDKF':
            raise InvalidKFMethodType
        self.method_type = method_type

    @classmethod
    def calc_sqrt_matrix(cls, matrix: npt.ArrayLike) -> npt.ArrayLike:
        return scipy.linalg.cholesky(matrix, lower=True)

    @classmethod
    def plot(cls, t_array, measurement_array, sigma_array=None, truth_array=None):
        # Plots
        if truth_array is not None:
            plt.plot(t_array, truth_array, label="Truth")
        plt.plot(t_array, measurement_array, label="SPKF est.")
        if sigma_array is not None:
            plt.plot(t_array, measurement_array + sigma_array, "g:", label="Bounds")
            plt.plot(t_array, measurement_array - sigma_array, "g:")
        plt.xlabel('Iteration')
        plt.ylabel('State')
        plt.legend()
        plt.show()

    @property
    def aug_vector(self) -> npt.ArrayLike:
        return np.append(np.append(self.x.get_vector(), self.w.get_vector(), axis=0), self.v.get_vector(), axis=0)

    @property
    def aug_cov(self) -> npt.ArrayLike:
        num_rows_x = self.x.get_cov().shape[0]
        num_rows_w = self.w.get_cov().shape[0]
        num_rows_v = self.v.get_cov().shape[0]

        num_cols_x = self.x.get_cov().shape[1]
        num_cols_w = self.w.get_cov().shape[1]
        num_cols_v = self.v.get_cov().shape[1]

        num_rows = num_rows_x + num_rows_w + num_rows_v
        num_cols = num_cols_x + num_cols_w + num_cols_v

        matrix_result = np.zeros((num_rows, num_cols))
        matrix_result[:num_rows_x, :num_cols_x] = self.x.get_cov()
        matrix_result[num_rows_x:num_rows_x+num_rows_w, num_cols_x: num_cols_x+num_cols_w] = self.w.get_cov()
        matrix_result[num_rows_x+num_rows_w:, num_cols_x+num_cols_w:] = self.v.get_cov()
        return matrix_result

    @property
    def gamma(self) -> float:
        """
        A tuning parameter for SPKF. For Guassian distributions, gamma is sqrt(3)
        :return: the turning parameter
        """
        if self.method_type == 'CDKF':
            return np.sqrt(3)
        else:
            raise InvalidKFMethodType

    @property
    def h(self) -> float:
        """
        A tuning parameter for SPKF. For Guassian distributions, gamma is sqrt(3)
        :return: h tunning parameter
        """
        if self.method_type == 'CDKF':
            return np.sqrt(3)
        else:
            raise InvalidKFMethodType

    @property
    def alpha_m_0(self) -> float:
        if self.method_type == 'CDKF':
            return (self.h ** 2 - self.L) / self.h ** 2
        else:
            raise InvalidKFMethodType

    @property
    def alpha_m(self) -> float:
        if self.method_type == 'CDKF':
            return 1 / (2 * self.h ** 2)
        else:
            raise InvalidKFMethodType

    @property
    def array_alpha_m(self):
        """
        Row vector of all alpha_m entries.
        :return:
        """
        alpha_m_vec = np.array(np.tile(self.alpha_m, self.p))  # vector of all alpha_m, excluding alpha_c_0
        return np.append(self.alpha_m_0, alpha_m_vec).reshape(-1, 1)

    @property
    def alpha_c_0(self) -> float:
        if self.method_type == 'CDKF':
            return (self.h ** 2 - self.L) / self.h ** 2
        else:
            raise InvalidKFMethodType

    @property
    def alpha_c(self) -> float:
        if self.method_type == 'CDKF':
            return 1 / (2 * self.h ** 2)
        else:
            raise InvalidKFMethodType

    @property
    def array_alpha_c(self) -> npt.ArrayLike:
        """
        row vector for all the entries in alpha c
        """
        array_ = np.array(np.tile(self.alpha_c, self.p))
        return np.append(self.alpha_c_0, array_).reshape(-1, 1)

    @property
    def x_sp(self) -> npt.ArrayLike:
        """
        Returns the matrix that represents the augmented sigma points.
        :return: augmented sigma points
        """
        result_matrix = np.tile(self.aug_vector, [1, self.p + 1])
        return result_matrix + self.gamma * np.append(np.zeros(self.aug_vector.shape),
                                                      np.append(self.calc_sqrt_matrix(self.aug_cov),
                                                                -self.calc_sqrt_matrix(self.aug_cov), axis=1), axis=1)

    @property
    def x_sp_x(self):
        return self.x_sp[0: self.Nx, :]

    @property
    def x_sp_w(self):
        return self.x_sp[self.Nx: self.Nx + self.Nw, :]

    @property
    def x_sp_v(self):
        return self.x_sp[self.Nx + self.Nw:, :]

    def __state_prediction(self, u: float) -> tuple[npt.ArrayLike, npt.ArrayLike]:
        """
        This is the step 1a (first step) of the process. The state estimate is performed in this step.
        :param u: The process input.
        :return: tuple containing the augmented state matrix and the resultant state estimate. Note that the second
        element is in the numpy matrix form and hence need indexing to extract its individual elements.
        """
        # Pass the input elements of the sigma point into the state function. Then the mean estimate is calculated
        Xx = self.func_f(self.x_sp_x, u, self.x_sp_w)
        self.x.set_vector(Xx @ self.array_alpha_m)  # outputs are augmented xhat matrix and state estimate vector
        return Xx

    def __cov_prediction(self, Xx: npt.ArrayLike) -> npt.ArrayLike:
        """
        This is the step 1b (second step) of the process. The estimate covariance is estimated.
        :param Xx: Sigma-point matrix containing sigma-points for the xhat.
        :param xhat: state vector estimate as calculated from step 1a.
        :return:
        """
        Xs = Xx - np.tile(self.x.get_vector(), [1, self.p + 1])
        self.x.set_cov(Xs @ np.diag(self.array_alpha_c.flatten()) @ Xs.transpose())
        return Xs

    def __output_estimate(self, Xx: npt.ArrayLike, u: float):
        """
        Step 1c (third step), which is the output prediction.
        :param Xx:
        :param u:
        :return:
        """
        Y = self.func_h(Xx, u, self.x_sp_v)
        return Y, Y @ self.array_alpha_m

    def __estimator_gain_matrix(self, y: npt.ArrayLike, yhat: npt.ArrayLike, xs: npt.ArrayLike) -> \
            tuple[npt.ArrayLike, npt.ArrayLike]:
        """
        Step 2a
        :param Y: Output Sigma Point
        :param yhat: output variable vector
        :param Xs: difference between sigma points and state variable
        :return: SigmaY and gain estimator, Lx
        """
        Ys = y - np.tile(yhat, [1, self.p + 1])
        SigmaXY = xs @ np.diag(self.array_alpha_c.flatten()) @ Ys.transpose()
        SigmaY = Ys @ np.diag(self.array_alpha_c.flatten()) @ Ys.transpose()
        L = SigmaXY @ np.linalg.inv(SigmaY)
        return SigmaY, L

    def __state_update(self, L: npt.ArrayLike, ytrue: npt.ArrayLike, yhat: npt.ArrayLike) -> None:
        self.x.set_vector(self.x.get_vector() + (L @ (ytrue - yhat)).reshape(-1, 1))

    def __cov_measurement_update(self, Lx, SigmaY) -> None:
        self.x.set_cov(self.x.get_cov() - Lx @ SigmaY @ Lx.transpose())

    def solve(self, u: float, y_true: float) -> None:
        Xx = self.__state_prediction(u=u)  # Step 1a
        Xs = self.__cov_prediction(Xx=Xx)  # Step 1b
        y, y_hat = self.__output_estimate(Xx=Xx, u=0)  # Step 1c

        SigmaY, Lx = self.__estimator_gain_matrix(y=y, yhat=y_hat, xs=Xs)  # Step 2a
        self.__state_update(L=Lx, ytrue=y_true, yhat=y_hat)  # Step 2b
        self.__cov_measurement_update(Lx=Lx, SigmaY=SigmaY)  # Step 2c

