# Kirin Programming Language
# VarTableRow class
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

from semanticCube import invKeywordMapper

class VarTableRow(object):

	def __init__(self, varType, isIndependent, isPrivate, address):
		self.varType = varType
		self.isIndependent = isIndependent
		self.isPrivate = isPrivate
		self.address = address
	
	def __str__(self):
		dim, primType = self.varType
		varTypeStr = "(%d, %s)" % (dim, invKeywordMapper.get(primType))
		return varTypeStr + " " + str(self.isIndependent) + " " + str(self.isPrivate) + " " + str(self.address)