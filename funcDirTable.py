from funcDirRow import FuncDirRow

class FuncDirTable(object):

	def __init__(self):
		self.table = {}

	def has(self, blockID, blockParams):
		return (blockID, blockParams) in self.table

	def add(self, blockID, blockParams, funcDirRow):
		self.table[(blockID, blockParams)] = funcDirRow