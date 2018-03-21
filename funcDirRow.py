# Kirin Programming Language
# FuncDirRow class
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

from varTable import VarTable
from semanticCube import invKeywordMapper

class FuncDirRow(object):

	def __init__(self, blockType, isIndependent, isPrivate):
		self.blockType = blockType # Numeric code representation of a type.
		self.isIndependent = isIndependent
		self.isPrivate = isPrivate
		self.varTable = VarTable()

	def __str__(self):
		return str(invKeywordMapper.get(self.blockType)) + " " + str(self.isIndependent) + " " + str(self.isPrivate)