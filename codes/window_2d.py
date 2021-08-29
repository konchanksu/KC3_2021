#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
粒子群最適化の結果をTkとmatplotlibを用いて表示するクラス
関数に関しては
https://en.wikipedia.org/wiki/Test_functions_for_optimization
と
https://qiita.com/tomitomi3/items/d4318bf7afbc1c835dda#bukin-function-n6
を参考にさせていただきました
"""


__author__ = "Hidemasa Kondo (C.A.C.)"
__date__ = "updated at 2021/08/24 (created at 2021/08/04)"
__version__ = "1.0.0"

import sys
from tkinter import (
    HORIZONTAL,
    DoubleVar,
    IntVar,
    Frame,
    Scale,
    Tk,
    Variable,
    messagebox,
    Menu,
    Entry,
    Toplevel,
    Label,
    Button,
    ttk,
)
from typing import Dict

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from function_2d import Function2D
from functions import TestFunctions
from particle_swarm_optimization import ParticleSwarmOptimization

matplotlib.use("tkagg")


class Window2D:
    """
    Tkinterで表示を行うクラス
    matplotlibで散布図を表示する
    """

    def __init__(self) -> None:
        """
        コンストラクタ
        """
        self.func: Function2D = Function2D()
        self.pso: ParticleSwarmOptimization = ParticleSwarmOptimization(self.func)

        self.x_point = np.empty((0, self.pso.N))
        self.y_point = np.empty((0, self.pso.N))

        self.root: Tk = Window2D.init_root()
        self.scale_var: DoubleVar = DoubleVar()

        self.contour = None

        self.figure: plt.Figure = plt.Figure()
        self.axes: plt.axes = self.figure.add_subplot(111)

        self.setting_menu: SettingMenu = SettingMenu(self.root, self)
        self.setting_menu.set_menubar()

        self.make_controurf()

    def append_scatter_data(self, x_point, y_point) -> None:
        """
        散布図データを追加する

        Args:
            x_point ([type]): [description]
            y_point ([type]): [description]
        """
        self.x_point = np.append(self.x_point, np.array([x_point]), axis=0)
        self.y_point = np.append(self.y_point, np.array([y_point]), axis=0)

    def reset(self) -> None:
        """
        散布図を更新する時の初期化処理
        """
        self.x_point = np.empty((0, self.pso.N))
        self.y_point = np.empty((0, self.pso.N))

        plt.xlim(self.func.x_domain[0], self.func.x_domain[1])
        plt.ylim(self.func.y_domain[0], self.func.y_domain[1])

        self.scale_var = DoubleVar()
        self.pso.reset()

    def set_func(self, func: Function2D) -> None:
        """
        PSOと自身に関数を設定する

        Args:
            func (Function2D): 関数オブジェクト
        """
        self.func = func
        self.pso.set_func(self.func)
        self.make_controurf()

    def learn(self) -> None:
        """
        群を学習させる
        """
        for data in self.pso.learn():
            self.append_scatter_data(*data)

    @staticmethod
    def init_root() -> Tk:
        """
        rootを初期化する

        Returns:
            Tk: tkオブジェクト
        """
        a_tk = Tk()
        a_tk.title("Plot window")
        a_tk.geometry("640x520")
        return a_tk

    def on_closing(self) -> None:
        """
        Tkを終了する
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            sys.exit()

    def display_at_tk(self) -> None:
        """
        tkを用いて表示をおこなう
        """
        frame_plt = Frame(self.root)
        frame_scale = Frame(self.root)

        a_scale = self.display_time_series_scale(frame_scale)
        a_scale.grid(row=0, column=0)

        # widgetの設定
        canvas = FigureCanvasTkAgg(self.figure, frame_plt)
        self.make_scatter(0)

        # widgetの配置
        frame_plt.grid(row=0, column=0)
        frame_scale.grid(row=1, column=0)
        canvas.get_tk_widget().grid(row=1, column=0)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def display_time_series_scale(self, frame: Frame) -> Scale:
        """
        時系列をいじることができるスケールを作成、表示する

        Args:
            frame (Frame): Tkのフレーム

        Returns:
            Scale: スケールのバーオブジェクト
        """
        return Scale(
            frame,
            variable=self.scale_var,
            orient=HORIZONTAL,
            length=400,
            resolution=1,
            from_=1,
            to=len(self.x_point),
            command=lambda event: self.make_scatter(int(self.scale_var.get()) - 1),
        )

    def make_scatter(self, number: int) -> None:
        """
        指定した番号の散布図を生成する

        Args:
            number (int): イメージ番号
        """
        self.figure.canvas.flush_events()
        self.axes.clear()
        self.draw_controurf()
        self.axes.set_xlim(self.func.x_domain[0], self.func.x_domain[1])
        self.axes.set_ylim(self.func.y_domain[0], self.func.y_domain[1])
        self.axes.scatter(self.func.best[0], self.func.best[1], c="gray")
        self.axes.scatter(self.x_point[number], self.y_point[number], c="orange")
        self.figure.canvas.draw()

    def make_controurf(self) -> None:
        """
        等高線を作成する
        """
        # データ作成
        x = np.arange(self.func.x_domain[0], self.func.x_domain[1] + 0.000001, 0.1)
        y = np.arange(self.func.y_domain[0], self.func.y_domain[1] + 0.000001, 0.1)
        x_mesh, y_mesh = np.meshgrid(x, y)
        z = np.array(
            [
                np.array(
                    list(
                        map(lambda x: self.func(x[0], x[1]), zip(x_mesh[i], y_mesh[i]))
                    )
                )
                for i in range(len(x_mesh))
            ]
        )
        self.contour = [x_mesh, y_mesh, z]

    def draw_controurf(self) -> None:
        """
        実際に等高線を描くメソッド
        """
        self.axes.contourf(*self.contour, cmap="Blues", levels=15)


class SettingMenu:
    """
    メニューバーを表示するクラス
    """

    func_dict: Dict[str, Function2D] = {
        "tmp": Function2D(),
        "Ackley Function": TestFunctions.ackley_function(),
        "Rosenbrock Function": TestFunctions.rosenbrock_function(),
        "Bukin function N.6": TestFunctions.bukin_function_n6(),
        "Levi function N.13": TestFunctions.levi_function_n13(),
        "Easom function": TestFunctions.easom_function(),
    }

    window_exist: bool = False

    def __init__(self, root: Tk, window2d: Window2D) -> None:
        """
        コンストラクタ

        Args:
            root (Tk): tkオブジェクト
            window2d (Window2D): 呼び出し元の表示ウィンドウ
        """
        self.root: Tk = root
        self.sub_root: Tk = None
        self.menubar = Menu(self.root, tearoff=False)
        self.window2d: Window2D = window2d
        self.now_func: str = "tmp"

    def set_menubar(self) -> None:
        """
        メニューバーを作成する
        """
        self.root.config(menu=self.menubar)

        menu_file = Menu(self.root)
        self.menubar.add_cascade(label="PSO設定", menu=menu_file)
        menu_file.add_command(label="PSO設定", command=self.display_window)

    @staticmethod
    def init_root() -> Tk:
        """
        Tkオブジェクトを作成

        Returns:
            Tk: [description]
        """
        a_tk = Toplevel()
        a_tk.geometry("600x400")
        a_tk.title("PSO設定")
        return a_tk

    def display_window(self) -> None:
        """
        設定ウィンドウを表示する
        """
        if SettingMenu.window_exist:
            return
        SettingMenu.window_exist = True
        self.sub_root = SettingMenu.init_root()
        frame = Frame(self.sub_root)
        frame_center = Frame(self.sub_root)
        frame.grid()
        frame_center.grid()

        input_n = IntVar(value=ParticleSwarmOptimization.N)
        SettingMenu.input_setting(frame, input_n, "N: 群に属する粒子の数", 0)

        input_loop = IntVar(value=ParticleSwarmOptimization.LOOP)
        SettingMenu.input_setting(frame, input_loop, "LOOP: 粒子一つあたりの移動回数", 1)

        input_c1 = DoubleVar(value=ParticleSwarmOptimization.Particle.C1)
        SettingMenu.input_setting(frame, input_c1, "C1: 自身の最良座標に対する係数", 2)

        input_c2 = DoubleVar(value=ParticleSwarmOptimization.Particle.C2)
        SettingMenu.input_setting(frame, input_c2, "C2: 群の最良座標に対する係数", 3)

        input_w = DoubleVar(value=ParticleSwarmOptimization.Particle.W)
        SettingMenu.input_setting(frame, input_w, "W: これまでの速度に対する重み", 4)

        combobox_func = ttk.Combobox(
            frame_center,
            height=len(SettingMenu.func_dict),
            values=tuple(SettingMenu.func_dict.keys()),
            state="readonly",
        )
        combobox_func.grid(row=0, column=0, sticky="NESW")
        combobox_func.current(combobox_func["value"].index(self.now_func))

        button_ok = Button(
            frame_center,
            text="更新",
            command=lambda: (
                self.update_setting(
                    n=input_n.get(),
                    loop=input_loop.get(),
                    c1=input_c1.get(),
                    c2=input_c2.get(),
                    func=combobox_func.get(),
                )
            ),
        )
        button_ok.grid(row=1, column=0, sticky="NESW")

        self.sub_root.grid_rowconfigure(0, weight=1)
        self.sub_root.grid_columnconfigure(0, weight=1)
        self.sub_root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.sub_root.mainloop()

    @staticmethod
    def input_setting(frame: Frame, input_var: Variable, text: str, row: int) -> None:
        """
        設定を表示する

        Args:
            frame (Frame): フレームオブジェクト
            input_var (Variable): 入力用の変数
            text (str): ラベル用のテキスト
            row (int): 表示のrow
        """
        label = Label(frame, text=text)
        label.grid(row=row, column=0, sticky="NESW")
        entry = Entry(frame, textvariable=input_var, width=20)
        entry.grid(row=row, column=1, sticky="NESW")

    def update_setting(
        self,
        n: int = None,
        loop: int = None,
        c1: float = None,
        c2: float = None,
        w: float = None,
        func: str = "tmp",
    ) -> None:
        """
        再計算

        Args:
            sub_root (Tk): Tkオブジェクト
            n (int, optional): N. Defaults to None.
            loop (int, optional): LOOP. Defaults to None.
            c1 (float, optional): C1. Defaults to None.
            c2 (float, optional): C2. Defaults to None.
            w (float, optional): W. Defaults to None.
        """
        if func in SettingMenu.func_dict:
            self.now_func = func
        self.window2d.pso.set_status(n=n, loop=loop, c1=c1, c2=c2, w=w)
        self.window2d.set_func(SettingMenu.func_dict[self.now_func])
        self.window2d.reset()
        self.window2d.learn()
        self.window2d.display_at_tk()

    def on_closing(self) -> None:
        """
        Tkを終了する
        """
        SettingMenu.window_exist = False
        self.sub_root.destroy()
