# Kirin Programming Language
# VarTableRow class
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

from type import Type

class VarTableRow(object):

	def __init__(self, varType, isIndependent, isPrivate):
		self.varType = varType
		self.isIndependent = isIndependent
		self.isPrivate = isPrivate
	
	def __str__(self):
		return str(self.varType) + " " + str(self.isIndependent) + " " + str(self.isPrivate)