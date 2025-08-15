# -*- coding: utf-8 -*-


"""LRU缓存策略
- 基于LRU缓存策略的缓存管理模块
- LRU(Least Recently Used) 是一种缓存淘汰算法，全称为"最近最少使用"。它的核心思想是：​​当缓存空间不足时，优先淘汰最近最少使用的数据​​。


"""

import time

from .base import CCacheObject, CCacheList

class CLRUCache:
	
	def __init__(self, capacity, lru_handle=None, update_interval=0):
		"""
		初始化LRU缓存管理器
		:param capacity: 需要进行缓存的容器对象最大数量
		:param lru_handle: 缓存对象处理函数
		:param update_interval: 缓存对象更新间隔		# 启动定时器,定时刷新 self._now(本意是用于每次访问缓存、增加缓存时使用的时间戳,避免每次操作时都进行时间获取,提高效率。由于与定时器功能耦合,增加即时获取时间戳的方案。)
		"""
		
		self._dict = {}		 		# 用于快速检索缓存项的hash表(要在使用层注意key的唯一性,否则会进行覆盖,且被覆盖的缓存需要等到下一次LRU时才会被清除)
		self._cache_list = CCacheList(capacity, func_lru_handle=self.OnDiscard)
		self._lru_handle = lru_handle
		self._now = int(time.time())

		if update_interval > 0:
			pass
		else:
			self._update_timer = None

	# ====================== 魔术方法 Start ======================

	def __len__(self):
		"""允许通过len(obj)获取缓存数量
		"""
		return len(self._dict)

	def __contains__(self, key):
		"""允许通过key in obj判断缓存中是否存在key
		"""
		return key in self._dict
	
	# ====================== 魔术方法 End ======================


	def Add(self, key, value):
		""" 添加缓存
		要在使用层注意key的唯一性,否则会进行覆盖,且被覆盖的缓存需要等到下一次LRU时才会被清除
		"""
		cache_item = self._cache_list.AddObject(CCacheObject(key, value, self._GetTime()))
		self._dict[key] = cache_item

	def Pop(self, key):
		""" 弹出缓存
		"""
		cache_item = self._dict.pop(key, None)
		if cache_item is None:
			return None
		self._cache_list.DelItem(cache_item)
		return cache_item.obj.value

	def Get(self, key):
		""" 访问缓存
		"""
		cache_item = self._dict.get(key)
		if cache_item is None:
			return None
		cache_obj = self._cache_list.GetObjectFromItem(cache_item, self._GetTime())
		return cache_obj.value 

	def OnDiscard(self, pair: CCacheObject):
		""" 缓存对象被丢弃时调用
		"""
		self._dict.pop(pair.key, None)
		if self._lru_handle is not None:
			self._lru_handle(pair.value)


	def raw_cache_iteritems(self):
		""" 按head到tail的顺序 迭代缓存对象的所有属性
		"""
		for cache_item in self._cache_list:
			cache_obj = cache_item.obj
			yield cache_obj.key, cache_obj.value, cache_obj.last_get

	def itervalues(self):
		""" 迭代所有缓存对象的值
		"""
		for cache_item in self._dict.itervalues():
			yield cache_item.obj.value

	def iterkeys(self):
		""" 迭代所有缓存的键
		"""
		for key in self._dict.iterkeys():
			yield key

	def iteritems(self):
		""" 迭代所有缓存对象的键值对
		"""
		for key, cache_item in self._dict.iteritems():
			yield key, cache_item.obj.value




	# ====================== 私有方法 Start ======================
	def _GetTime(self):
		if self._update_timer:
			return self._now
		return int(time.time())
	# ====================== 私有方法 End ======================