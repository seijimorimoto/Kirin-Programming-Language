from varTable import VarTable

class FuncDirRow(object):

	def __init__(self, blockType, isIndependent, isPrivate):
		self.blockType = blockType
		self.isIndependent = isIndependent
		self.isPrivate = isPrivate