# Kirin Programming Language
# FuncDirTable class
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

from funcDirRow import FuncDirRow

class FuncDirTable(object):

	def __init__(self):
		self.table = {}

	def has(self, blockID, blockParams):
		return (blockID, blockParams) in self.table

	def add(self, blockID, blockParams, funcDirRow):
		self.table[(blockID, blockParams)] = funcDirRow
		# Print for debugging
		if blockParams is not None:
			if len(blockParams) == 0:
				blockParamsStr = "()"
			else:
				blockParamsStr = "("
				for param in blockParams:
					blockParamsStr = blockParamsStr + str(param) + ", "
				blockParamsStr = list(blockParamsStr.strip())
				blockParamsStr[len(blockParamsStr) - 1] = ')'
				blockParamsStr = "".join(blockParamsStr)
		else:
			blockParamsStr = "None"
		print("created function with:", blockID, blockParamsStr, funcDirRow)
	
	def getVarTable(self, blockID, blockParams):
		return self.table[(blockID, blockParams)].varTable