# Kirin Programming Language
# VarTableRow class
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

from semanticCube import invKeywordMapper

class VarTableRow(object):

	def __init__(self, varType, isIndependent, isPrivate, address, dimX, dimY):
		self.varType = varType
		self.isIndependent = isIndependent
		self.isPrivate = isPrivate
		self.address = address
		self.dimX = dimX
		self.dimY = dimY
	
	def __str__(self):
		varTypeStr = invKeywordMapper.get(self.varType)
		return varTypeStr + " " + str(self.isIndependent) + " " + str(self.isPrivate) + " " + str(self.address) + " " + str(self.dimX) + " " + str(self.dimY)