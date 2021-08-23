#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
メインファイル
"""

__author__ = "Hidemasa Kondo (C.A.C.)"
__date__ = "(created at 2021/08/12)"
__version__ = "1.0.0"

import sys

from window_2d import Window2D


def main():
    """メイン関数やでー"""
    app = Window2D()
    app.learn()
    app.display_at_tk()


if __name__ == "__main__":
    sys.exit(main())
