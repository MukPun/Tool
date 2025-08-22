# -*- coding: utf-8 -*-

"""元类实现的单例模式
- python 2.7
- 继承自type, 代表这个类是一个元类

- 元类的__call__被调用时,代表通过元类创建的类对象被调用,也就是CTest(),也就是CTest类的实例化过程.(__call__:当调用类的实例时调用、控制类的实例化过程。这里由于CTest是元类的实例,所以CTest()会调用到元类的__call__)
- 单例模式的原理就是控制同一个类全局只能存在一个实例化对象,所以需要在CTest()这一步进行处理,也就是需要在元类的__call__中处理
- 元类把单例对象存储在类对象的self.__instanc属性中

"""

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


