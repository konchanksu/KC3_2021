#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
メイン関数
"""

__author__ = "Hidemasa Kondo (C.A.C.)"
__date__ = "(created at 2021/08/12)"
__version__ = "1.0.0"

import sys
import asyncio

from window_2d import Window2D


async def main():
    """メイン関数やでー"""
    app = Window2D()
    app.learn()
    print("b")
    await asyncio.sleep(1)
    print("a")
    app.display_at_tk()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
