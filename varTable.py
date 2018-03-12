# Kirin Programming Language
# VarTable class
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

from varTableRow import VarTableRow

class VarTable(object):

	def __init__(self):
		self.table = {}

	def has(self, varID):
		return varID in self.table

	def add(self, varID, varTableRow):
		self.table[varID] = varTableRow
		# Print for debugging
		print("  created variable with:", varID, varTableRow)
	
	def get(self, varID):
		return self.table[varID]