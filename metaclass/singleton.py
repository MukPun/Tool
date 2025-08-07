# -*- coding: utf-8 -*-


class Singleton(type):

	def __init__(self, *args, **kwargs):
		self.__instance = None
		super(Singleton, self).__init__(*args, **kwargs)

	def __call__(cls, *args, **kwargs):
		if cls.__instance is None:
			obj = cls.__new__(cls, *args, **kwargs)
			obj.__init__(*args, **kwargs)
			cls.__instance = obj
		return cls.__instance