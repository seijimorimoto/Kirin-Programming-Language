# Kirin Programming Language
# Type class
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

class Type(object):

	def __init__(self, dim, primType):
		self.dim = dim
		self.primType = primType
	
	def __str__(self):
		return "(%d, %s)" % (self.dim, primTypeMapper.get(self.primType)) 