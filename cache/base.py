"""
缓存相关的基础对象

"""

class CCacheItem:
	"""缓存项
	类似链表结构中的节点
	"""

	def __init__(self, obj):
		self.obj = obj			# 缓存的元素
		self.prev = None		# 前一个缓存项
		self.next = None		# 后一个缓存项


class CCacheListIter:

	def __init__(self, cache_list):
		self.head = cache_list.head
		self.current = self.head.next
	
	def __next__(self):
		if self.current == self.head:
			# 意味着缓存列表已经遍历完毕
			raise StopIteration()
		item = self.current
		self.current = self.current.next
		return item

class CCacheList:
	"""缓存链表
	代表同一类别的缓存元素集合

	作用:
		1.管理缓存项
		2.封装缓存项的操作接口
	
	"""

	def __init__(self, i_max_count=10, func_lru_handle=None):
		self.head = CCacheItem(None)					# 头结点
		self.head.prev = self.head.next = self.head	# 构建循环链表	(这样真的不会循环引用吗？)			
		self.tail = self.head						# 尾节点
		self.item_count = 0							# 缓存项数量

		self.max_count = i_max_count				# 最大缓存项数量
		self.lru_handle = func_lru_handle			# 触发LRU时的处理函数

	def __iter__(self):
		"""
		# 返回迭代器对象, 使CCacheList变成迭代器, 成为可迭代对象
		# 使缓存项可以遍历
		"""
		return CCacheListIter(self)

	def Clear(self):
		self.head.prev = self.head.next = self.head
		self.tail = self.head
		self.item_count = 0

	def AddObject(self, obj):
		if self.item_count >= self.max_count:
			self._DoLRU()
		new_item = CCacheItem(obj)
		self._AddToTail(new_item)
		self.item_count += 1
		return new_item

	def GetObjectFromItem(self, o_item : CCacheItem, last_get_time):
		if o_item.prev is None or o_item.next is None:
			return None

		if not o_item is self.tail:
			# 只要不是尾部的节点, 都刷新到尾部
			self._RefreshItem(o_item)
		o_item.obj.last_get = last_get_time
		return o_item.obj


	def DelItem(self, o_item : CCacheItem):
		if o_item.prev is None or o_item.next is None:
			return
		assert o_item != self.head	# 禁止删除头节点
		self._Unlink(o_item)
		self.item_count -= 1

	# ========================== 私有方法 Start ==========================

	def _Unlink(self, o_item : CCacheItem):
		prev = o_item.prev
		next = o_item.next

		prev.next = next
		next.prev = prev
		o_item.prev = o_item.next = None
		if o_item == self.tail:
			self.tail = prev

	def _AddToTail(self, o_item : CCacheItem):
		o_item.prev = self.tail
		o_item.next = self.head

		self.head.prev = o_item
		self.tail.next = o_item
		self.tail = o_item

	def _DoLRU(self):
		assert self.item_count >= 1	
		head_item = self.head.next
		self.DelItem(head_item)
		if self.lru_handle is not None:
			self.lru_handle(head_item.obj)

	def _RefreshItem(self, o_item : CCacheItem):
		self._Unlink(o_item)
		self._AddToTail(o_item)

	# =========================== 私有方法 End ==========================


class CCacheObject:
	"""缓存对象
	用于缓存数据, 缓存的最小单元,包含实际的缓存数据
	
	"""
	def __init__(self, k, v, now):
		self.key = k
		self.value = v
		self.last_get = now				# 最后一次被使用的时间