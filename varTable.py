from varTableRow import VarTableRow

class VarTable(object):

	def __init__(self):
		self.table = {}

	def has(self, varID):
		return varID in self.table

	def add(self, varID, tableRow):
		self.globalVars[varID] = tableRow

