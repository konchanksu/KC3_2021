#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
メイン関数
"""

__author__ = "Hidemasa Kondo (C.A.C.)"
__date__ = "updated at 2021/08/30 (created at 2021/08/12)"
__version__ = "1.0.0"

import sys

from window_2d import Window2D


def main():
    """メイン関数やでー"""
    app = Window2D()
    app.learn()
    app.display_at_tk()
    app.mainloop()


if __name__ == "__main__":
    sys.exit(main())
