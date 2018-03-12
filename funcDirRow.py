# Kirin Programming Language
# FuncDirRow class
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

from varTable import VarTable
from type import primTypeMapper

class FuncDirRow(object):

	def __init__(self, blockType, isIndependent, isPrivate):
		self.blockType = blockType
		self.isIndependent = isIndependent
		self.isPrivate = isPrivate
		self.varTable = VarTable()

	def __str__(self):
		return str(primTypeMapper.get(self.blockType)) + " " + str(self.isIndependent) + " " + str(self.isPrivate)