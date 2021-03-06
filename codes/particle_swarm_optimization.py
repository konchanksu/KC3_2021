#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
粒子群最適化の実装
"""


__author__ = "Hidemasa Kondo (C.A.C.)"
__date__ = "updated at 2021/08/30 (created at 2021/08/04)"
__version__ = "1.0.0"

import random
from copy import copy
from typing import Final, List, Tuple

from function_2d import Function2D


class ParticleSwarmOptimization:
    """粒子群を定義する"""

    N: float = 10  # 群に属する個体数
    LOOP: float = 100  # 学習回数

    class Particle:
        """粒子を定義するクラス"""

        N_DIM: Final = 2  # 次元数
        C1: float = 0.95  # 自身の最良に対する係数
        C2: float = 0.95  # 群の最良に対する係数
        W: float = 0.9  # 慣性定数

        def __init__(self, func: Function2D) -> None:
            """
            コンストラクタ

            Args:
                func (Function2D): 目的関数
            """
            self.func: Function2D = func
            self.point: List[float] = [self.init_x(), self.init_y()]
            self.velocity: List[float] = [
                random.uniform(0, 1)
                for _ in range(ParticleSwarmOptimization.Particle.N_DIM)
            ]
            self.my_best_point: List[float] = copy(self.point)
            self.my_best_score: float = self.func(*self.point)

        def init_x(self) -> float:
            """xを定義域の中でランダムに初期化する"""
            return random.uniform(*self.func.x_domain)

        def init_y(self) -> float:
            """xを定義域の中でランダムに初期化する"""
            return random.uniform(*self.func.y_domain)

        def move(self) -> None:
            """粒子が次の位置に移動する"""
            for i in range(self.N_DIM):
                self.point[i] += self.velocity[i]
            self.point = list(self.func.set_point_in_domain(*self.point))

        def update_velocity(self, group_best_point: List[float]) -> None:
            """速度を更新する"""
            for i in range(ParticleSwarmOptimization.Particle.N_DIM):
                self.velocity[i] = (
                    ParticleSwarmOptimization.Particle.W * self.velocity[i]
                    + ParticleSwarmOptimization.Particle.C1
                    * random.random()
                    * (self.my_best_point[i] - self.point[i])
                    + ParticleSwarmOptimization.Particle.C2
                    * random.random()
                    * (group_best_point[i] - self.point[i])
                )

        def eval(self) -> None:
            """現在の座標を評価し、これまでの最も良い座標であれば更新する"""
            result = self.func(*self.point)
            if self.my_best_score > result:
                self.my_best_score = result
                self.my_best_point = copy(self.point)

    def __init__(self, func: Function2D) -> None:
        """
        コンストラクタ

        Args:
            func (Function2D): 目的関数
        """
        self.func: Function2D = func
        self.particles: List[self.Particle] = [
            self.Particle(self.func) for _ in range(ParticleSwarmOptimization.N)
        ]
        self.group_best_point: List[float] = []
        self.group_best_score: float = float("inf")

    def set_func(self, func: Function2D) -> None:
        """
        関数を設定する

        Args:
            func (Function2D): 目的関数
        """
        self.func = func

    def learn(self) -> List[Tuple[List[float]]]:
        """
        群を動かす
        """
        scatter_data = []
        for _ in range(ParticleSwarmOptimization.LOOP):
            self.eval()
            self.update_velocity()
            self.move()
            scatter_data.append(
                (
                    list(map(lambda particle: particle.point[0], self.particles)),
                    list(map(lambda particle: particle.point[1], self.particles)),
                )
            )
        return scatter_data

    def eval(self) -> None:
        """全ての粒子を評価する"""
        for particle in self.particles:
            particle.eval()
            if particle.my_best_score < self.group_best_score:
                self.group_best_score = particle.my_best_score
                self.group_best_point = copy(particle.my_best_point)

    def move(self) -> None:
        """全ての粒子を移動させる"""
        for particle in self.particles:
            particle.move()

    def update_velocity(self) -> None:
        """全ての粒子の速度を更新する"""
        for particle in self.particles:
            particle.update_velocity(self.group_best_point)

    @staticmethod
    def set_status(
        n: int = None,
        loop: int = None,
        c1: float = None,
        c2: float = None,
        w: float = None,
    ) -> None:
        """
        変数を設定する

        Args:
            N (int, optional): N. Defaults to None.
            LOOP (int, optional): LOOP. Defaults to None.
            C1 (float, optional): それぞれの粒子のC1. Defaults to None.
            C2 (float, optional): それぞれの粒子のC2. Defaults to None.
            W (float, optional): それぞれの粒子のW. Defaults to None.
        """
        try:
            n = int(n)
        except (ValueError, TypeError):
            pass
        else:
            if n > 0:
                ParticleSwarmOptimization.N = n

        try:
            loop = int(loop)
        except (ValueError, TypeError):
            pass
        else:
            if loop > 0:
                ParticleSwarmOptimization.LOOP = loop

        try:
            c1 = float(c1)
        except (ValueError, TypeError):
            pass
        else:
            ParticleSwarmOptimization.Particle.C1 = c1

        try:
            c2 = float(c2)
        except (ValueError, TypeError):
            pass
        else:
            ParticleSwarmOptimization.Particle.C2 = c2

        try:
            w = float(w)
        except (ValueError, TypeError):
            pass
        else:
            ParticleSwarmOptimization.Particle.W = w

    def reset(self) -> None:
        """
        学習を初期化する
        """
        self.particles = [
            self.Particle(self.func) for _ in range(ParticleSwarmOptimization.N)
        ]
        self.group_best_point = []
        self.group_best_score = float("inf")
