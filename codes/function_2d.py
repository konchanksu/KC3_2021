#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
2変数(x, y)を入力とする関数を実装するクラス
"""


__author__ = "Hidemasa Kondo (C.A.C.)"
__date__ = "updated at 2021/08/24 (created at 2021/08/11)"
__version__ = "1.0.0"

from typing import Callable, Tuple


class Function2D:
    """2次元平面上の関数を表すクラス"""

    def __init__(
        self,
        func: Callable[[float, float], float] = lambda x, y: (x - 5) ** 2
        + (y - 5) ** 2,
        x_domain: Tuple[int, int] = (0, 10),
        y_domain: Tuple[int, int] = (0, 10),
        best: Tuple[int, int] = (5, 5),
    ):
        """
        コンストラクタ

        Args:
            func (Callable[[float, float], float], optional):
                2次元平面上で実数値を取る何らかの関数. Defaults to lambdax.
            x_domain (Tuple[int, int], optional): 関数のx軸の定義域. Defaults to (0, 10).
            y_domain (Tuple[int, int], optional): 関数のy軸の定義域. Defaults to (0, 10).
            best (Tuple[int, int], optional): func(x, y)が最小となるx, y. Defaults to (5, 5).
        """
        self.x_domain: Tuple[int, int] = x_domain
        self.y_domain: Tuple[int, int] = y_domain
        self.func: Callable[[float, float], float] = func
        self.best: Tuple[int, int] = best

    def __call__(self, x: float, y: float) -> float:
        """
        引数を与えてf(x, y)を計算する(関数の評価を行う)

        Args:
            x (float): x座標の値
            y (float): y座標の値

        Returns:
            float: func(x, y)
        """
        x, y = self.set_point_in_domain(x, y)
        return self.func(x, y)

    def set_point_in_domain(self, x: float, y: float) -> Tuple[float, float]:
        """
        座標を定義域の内側に無理やり調整する関数

        Args:
            x (float): x座標の値
            y (float): y座標の値

        Returns:
            Tuple[float, float]: 定義域内に調整された(x, y)
        """
        x = self.set_x_in_domain(x)
        y = self.set_y_in_domain(y)
        return x, y

    def set_x_in_domain(self, x: float) -> float:
        """
        x座標を定義域の内側に無理やり調整する関数

        Args:
            x (float): x座標の値

        Returns:
            float: 調整後のx座標の値
        """
        if x < self.x_domain[0]:
            x = self.x_domain[0]
        elif x > self.x_domain[1]:
            x = self.x_domain[1]
        return x

    def set_y_in_domain(self, y: float) -> float:
        """
        y座標を定義域の内側に無理やり調整する関数

        Args:
            y (float): y座標の値

        Returns:
            float: 調整後のy座標の値
        """
        if y < self.y_domain[0]:
            y = self.y_domain[0]
        elif y > self.y_domain[1]:
            y = self.y_domain[1]
        return y
