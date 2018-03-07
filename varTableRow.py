from type import Type

class VarTableRow(object):

	def __init__(self, varType, isIndependent, isPrivate):
		self.varType = varType
		self.isIndependent = isIndependent
		self.isPrivate = isPrivate