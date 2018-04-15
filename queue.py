# Kirin Programming Language
# Queue class
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

from collections import deque

class Queue(object):

	def __init__(self):
		self.queue = deque()

	def empty(self):
		return len(self.queue) == 0

	def size(self):
		return len(self.queue)

	def front(self):
		return self.queue[0]

	def push(self, elem):
		self.queue.append(elem)

	def pop(self):
		self.queue.popleft()