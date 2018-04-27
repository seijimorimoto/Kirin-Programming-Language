# Kirin Programming Language
# FuncDirRow class
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

from varTable import VarTable
from kirinMappers import codeToType

class FuncDirRow(object):

	def __init__(self, blockType, isIndependent, isPrivate, startPos):
		self.blockType = blockType
		self.isIndependent = isIndependent
		self.isPrivate = isPrivate
		self.startPos = startPos
		self.varTable = VarTable()

	def __str__(self):
		# The blockType will be a string if the function returns an object (the blockType will be the name of the class of the
		# object to be returned).
		if type(self.blockType) is str:
			blockTypeStr = self.blockType
		else:
			blockTypeStr = codeToType.get(self.blockType)
		return blockTypeStr + " " + str(self.isIndependent) + " " + str(self.isPrivate) + " " + str(self.startPos)