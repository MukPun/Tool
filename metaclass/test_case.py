# -*- coding: utf-8 -*-

from .singleton import Singleton

# 用法及测试用例
class CTest:
	__metaclass__ = Singleton

	def __init__(self):
		print("init")

t1 = CTest()
t2 = CTest()
print(t1 is t2)