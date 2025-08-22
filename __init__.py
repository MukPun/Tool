# -*- coding: utf-8 -*-

"""
Python版本 3.0 +

"""

import sys
import os

# 添加项目根目录到系统路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from cache.test_case import run_test

if __name__ == '__main__':
	run_test()
