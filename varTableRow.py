# Kirin Programming Language
# VarTableRow class
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

# It is the inverse version of the keywordMapper in 'kirin_yacc.py'.
# It is just used for debugging purposes.
primTypeMapper = {
	1: 'int',
	2: 'double',
	3: 'char',
	4: 'bool',
	5: 'object',
	6: 'class',
	7: 'void'
}

class VarTableRow(object):

	def __init__(self, varType, isIndependent, isPrivate):
		self.varType = varType
		self.isIndependent = isIndependent
		self.isPrivate = isPrivate
	
	def __str__(self):
		dim, primType = self.varType
		varTypeStr = "(%d, %s)" % (dim, primTypeMapper.get(primType))
		return varTypeStr + " " + str(self.isIndependent) + " " + str(self.isPrivate)