#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ベンチマーク関数を集約したクラス
関数に関しては
https://en.wikipedia.org/wiki/Test_functions_for_optimization
と
https://qiita.com/tomitomi3/items/d4318bf7afbc1c835dda#bukin-function-n6
を参考にさせていただきました
"""

__author__ = "Hidemasa Kondo (C.A.C.)"
__date__ = "created at 2021/08/24"
__version__ = "1.0.0"

import numpy as np

from function_2d import Function2D


class TestFunctions:
    """
    テスト関数を集めたクラス
    """

    @staticmethod
    def ackley_function() -> Function2D:
        """
        Ackley functionを返す関数

        Returns:
            Function2D: Ackley function
        """
        return Function2D(
            func=lambda x, y: 20
            - 20 * np.exp(-0.2 * np.sqrt(1 / 2 * (x ** 2 + y ** 2)))
            + np.e
            - np.exp(1 / 2 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y))),
            x_domain=(-10, 10),
            y_domain=(-10, 10),
            best=(0, 0),
        )

    @staticmethod
    def rosenbrock_function() -> Function2D:
        """
        Rosenbrock functionを返す関数

        Returns:
            Function2D: Rosenbrock function
        """
        return Function2D(
            func=lambda x, y: 100 * (y - (x) ** 2) ** 2 + (1 - x) ** 2,
            x_domain=(-5, 5),
            y_domain=(-5, 5),
            best=(1, 1),
        )

    @staticmethod
    def bukin_function_n6() -> Function2D:
        """
        Bukin function N.6を返す関数

        Returns:
            Function2D: Bukin function N.6
        """
        return Function2D(
            func=lambda x, y: 100 * np.sqrt(np.abs(y - 0.01 * (x ** 2)))
            + 0.01 * np.abs(x + 10),
            x_domain=(-15, -5),
            y_domain=(-3, 3),
            best=(-10, 1),
        )

    @staticmethod
    def levi_function_n13() -> Function2D:
        """
        Levi function N.13を返す関数

        Returns:
            Function2D: Levi function N.13
        """
        return Function2D(
            lambda x, y: np.sin(3 * np.pi * x) ** 2
            + ((x - 1) ** 2) * (1 + np.sin(3 * np.pi * y) ** 2)
            + ((y - 1) ** 2) * (1 + np.sin(2 * np.pi * y) ** 2),
            x_domain=(-10, 10),
            y_domain=(-10, 10),
            best=(1, 1),
        )

    @staticmethod
    def easom_function() -> Function2D:
        """
        Easom functionを返す関数

        Returns:
            Function2D: Easom function
        """
        return Function2D(
            lambda x, y: -np.cos(x)
            * np.cos(y)
            * np.exp(-((x - np.pi) ** 2 + (y - np.pi) ** 2)),
            x_domain=(-20, 20),
            y_domain=(-20, 20),
            best=(np.pi, np.pi),
        )
