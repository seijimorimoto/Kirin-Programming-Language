# Kirin Programming Language
# VarTableRow class
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

from kirinMappers import codeToType

class VarTableRow(object):

	def __init__(self, varType, isIndependent, isPrivate, address, dimX, dimY, objVarTable):
		self.varType = varType
		self.isIndependent = isIndependent
		self.isPrivate = isPrivate
		self.address = address
		self.dimX = dimX
		self.dimY = dimY
		self.objVarTable = objVarTable
	
	def __str__(self):
		# The varType will be a string if the variable is an object (the varType will be the name of the class
		# of the object).
		if type(self.varType) is str:
			varTypeStr = self.varType
		else:
			varTypeStr = codeToType.get(self.varType)
		return varTypeStr + " " + str(self.isIndependent) + " " + str(self.isPrivate) + " " + str(self.address) + " " + str(self.dimX) + " " + str(self.dimY)