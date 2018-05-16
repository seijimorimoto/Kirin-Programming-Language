# Kirin Programming Language
# FuncDirTable class
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

from funcDirRow import FuncDirRow
from kirinMappers import typeToCode
from kirinMappers import codeToType

class FuncDirTable(object):

	def __init__(self):
		self.table = {}

	def has(self, blockID, blockParams, blockDimsX, blockDimsY):
		return (blockID, blockParams, blockDimsX, blockDimsY) in self.table

	def add(self, blockID, blockParams, blockDimsX, blockDimsY, funcDirRow):
		self.table[(blockID, blockParams, blockDimsX, blockDimsY)] = funcDirRow
		# Print for debugging
		if blockParams is not None:
			if len(blockParams) == 0:
				blockParamsStr = "()"
			else:
				blockParamsStr = "("
				for param in blockParams:
					if type(param) is str:
						blockParamsStr = blockParamsStr + param + ", "
					else:
						blockParamsStr = blockParamsStr + codeToType.get(param) + ", "
				blockParamsStr = list(blockParamsStr.strip())
				blockParamsStr[len(blockParamsStr) - 1] = ')'
				blockParamsStr = "".join(blockParamsStr)
		else:
			blockParamsStr = "None"
		print("created function with:", blockID, blockParamsStr, funcDirRow)
	
	def getFuncDirRow(self, blockId, blockParams, blockDimsX, blockDimsY):
		return self.table[(blockId, blockParams, blockDimsX, blockDimsY)]

	def getVarTable(self, blockID, blockParams, blockDimsX, blockDimsY):
		return self.table[(blockID, blockParams, blockDimsX, blockDimsY)].varTable