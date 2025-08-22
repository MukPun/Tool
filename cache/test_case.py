# -*- coding: utf-8 -*-

from cache.lru import CLRUCache

def run_test():
	# 初始化缓存对象
	CACHE_SIZE = 10
	oCache = CLRUCache(CACHE_SIZE)

	# 存入缓存
	guid = 1001
	   # 例子数据
	dData = {"guid": guid}
	oCache.Add(guid, dData)

	# 获取缓存
	dData = oCache.Get(guid)
	print(dData)

	for _ in range(CACHE_SIZE + 2):
		guid += 1
		dData1 = {"guid": guid}
		oCache.Add(guid, dData1)
	
	print(oCache.Get(1001))

	for key, val, last_get in oCache.raw_cache_iteritems():
		print(key, val, last_get)