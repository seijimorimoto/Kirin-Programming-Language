# Kirin Programming Language
# SemanticCube class
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

from quadrupleManager import operatorMapper

keywordMapper = {
	'int': 1,
	'double': 2,
	'char': 3,
	'bool': 4,
	'object': 5,
	'class': 6,
	'void': 7,
  'error': 8
}

invKeywordMapper = {
  1: 'int',
	2: 'double',
	3: 'char',
	4: 'bool',
	5: 'object',
	6: 'class',
	7: 'void',
  8: 'error'
}

class SemanticCube(object):

  def __init__(self):
    typeInt = keywordMapper.get("int")
    typeDouble = keywordMapper.get("double")
    typeChar = keywordMapper.get("char")
    typeBool = keywordMapper.get("bool")
    typeError = keywordMapper.get("error")
    typeNone = -1
    self.cube = {
      # 'int' with all other primitive data types.
      (typeInt, typeInt, operatorMapper.get("+")): typeInt,
      (typeInt, typeInt, operatorMapper.get("-")): typeInt,
      (typeInt, typeInt, operatorMapper.get("*")): typeInt,
      (typeInt, typeInt, operatorMapper.get("/")): typeInt,
      (typeInt, typeInt, operatorMapper.get("%")): typeInt,
      (typeInt, typeInt, operatorMapper.get("<")): typeBool,
      (typeInt, typeInt, operatorMapper.get(">")): typeBool,
      (typeInt, typeInt, operatorMapper.get("<=")): typeBool,
      (typeInt, typeInt, operatorMapper.get(">=")): typeBool,
      (typeInt, typeInt, operatorMapper.get("==")): typeBool,
      (typeInt, typeInt, operatorMapper.get("<>")): typeBool,
      (typeInt, typeInt, operatorMapper.get("and")): typeError,
      (typeInt, typeInt, operatorMapper.get("or")): typeError,
      (typeInt, typeInt, operatorMapper.get("xor")): typeError,
      (typeInt, typeInt, operatorMapper.get("=")): typeInt,
      (typeNone, typeInt, operatorMapper.get("UMINUS")): typeInt,
      (typeNone, typeInt, operatorMapper.get("~")): typeError,
      
      (typeInt, typeDouble, operatorMapper.get("+")): typeDouble,
      (typeInt, typeDouble, operatorMapper.get("-")): typeDouble,
      (typeInt, typeDouble, operatorMapper.get("*")): typeDouble,
      (typeInt, typeDouble, operatorMapper.get("/")): typeDouble,
      (typeInt, typeDouble, operatorMapper.get("%")): typeError,
      (typeInt, typeDouble, operatorMapper.get("<")): typeBool,
      (typeInt, typeDouble, operatorMapper.get(">")): typeBool,
      (typeInt, typeDouble, operatorMapper.get("<=")): typeBool,
      (typeInt, typeDouble, operatorMapper.get(">=")): typeBool,
      (typeInt, typeDouble, operatorMapper.get("==")): typeBool,
      (typeInt, typeDouble, operatorMapper.get("<>")): typeBool,
      (typeInt, typeDouble, operatorMapper.get("and")): typeError,
      (typeInt, typeDouble, operatorMapper.get("or")): typeError,
      (typeInt, typeDouble, operatorMapper.get("xor")): typeError,
      (typeInt, typeDouble, operatorMapper.get("=")): typeInt,

      (typeInt, typeChar, operatorMapper.get("+")): typeError, # Change to typeChar when vectors and matrices are implemented.
      (typeInt, typeChar, operatorMapper.get("-")): typeError,
      (typeInt, typeChar, operatorMapper.get("*")): typeChar,
      (typeInt, typeChar, operatorMapper.get("/")): typeError,
      (typeInt, typeChar, operatorMapper.get("%")): typeError,
      (typeInt, typeChar, operatorMapper.get("<")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeInt, typeChar, operatorMapper.get(">")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeInt, typeChar, operatorMapper.get("<=")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeInt, typeChar, operatorMapper.get(">=")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeInt, typeChar, operatorMapper.get("==")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeInt, typeChar, operatorMapper.get("<>")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeInt, typeChar, operatorMapper.get("and")): typeError,
      (typeInt, typeChar, operatorMapper.get("or")): typeError,
      (typeInt, typeChar, operatorMapper.get("xor")): typeError,
      (typeInt, typeChar, operatorMapper.get("=")): typeError,

      (typeInt, typeBool, operatorMapper.get("+")): typeError,
      (typeInt, typeBool, operatorMapper.get("-")): typeError,
      (typeInt, typeBool, operatorMapper.get("*")): typeError,
      (typeInt, typeBool, operatorMapper.get("/")): typeError,
      (typeInt, typeBool, operatorMapper.get("%")): typeError,
      (typeInt, typeBool, operatorMapper.get("<")): typeError,
      (typeInt, typeBool, operatorMapper.get(">")): typeError,
      (typeInt, typeBool, operatorMapper.get("<=")): typeError,
      (typeInt, typeBool, operatorMapper.get(">=")): typeError,
      (typeInt, typeBool, operatorMapper.get("==")): typeError,
      (typeInt, typeBool, operatorMapper.get("<>")): typeError,
      (typeInt, typeBool, operatorMapper.get("and")): typeError,
      (typeInt, typeBool, operatorMapper.get("or")): typeError,
      (typeInt, typeBool, operatorMapper.get("xor")): typeError,
      (typeInt, typeBool, operatorMapper.get("=")): typeError,

      # 'double' with all other primitive data types.
      (typeDouble, typeDouble, operatorMapper.get("+")): typeDouble,
      (typeDouble, typeDouble, operatorMapper.get("-")): typeDouble,
      (typeDouble, typeDouble, operatorMapper.get("*")): typeDouble,
      (typeDouble, typeDouble, operatorMapper.get("/")): typeDouble,
      (typeDouble, typeDouble, operatorMapper.get("%")): typeError,
      (typeDouble, typeDouble, operatorMapper.get("<")): typeBool,
      (typeDouble, typeDouble, operatorMapper.get(">")): typeBool,
      (typeDouble, typeDouble, operatorMapper.get("<=")): typeBool,
      (typeDouble, typeDouble, operatorMapper.get(">=")): typeBool,
      (typeDouble, typeDouble, operatorMapper.get("==")): typeBool,
      (typeDouble, typeDouble, operatorMapper.get("<>")): typeBool,
      (typeDouble, typeDouble, operatorMapper.get("and")): typeError,
      (typeDouble, typeDouble, operatorMapper.get("or")): typeError,
      (typeDouble, typeDouble, operatorMapper.get("xor")): typeError,
      (typeDouble, typeDouble, operatorMapper.get("=")): typeDouble,
      (typeNone, typeDouble, operatorMapper.get("UMINUS")): typeDouble,
      (typeNone, typeDouble, operatorMapper.get("~")): typeError,

      (typeDouble, typeInt, operatorMapper.get("+")): typeDouble,
      (typeDouble, typeInt, operatorMapper.get("-")): typeDouble,
      (typeDouble, typeInt, operatorMapper.get("*")): typeDouble,
      (typeDouble, typeInt, operatorMapper.get("/")): typeDouble,
      (typeDouble, typeInt, operatorMapper.get("%")): typeError,
      (typeDouble, typeInt, operatorMapper.get("<")): typeBool,
      (typeDouble, typeInt, operatorMapper.get(">")): typeBool,
      (typeDouble, typeInt, operatorMapper.get("<=")): typeBool,
      (typeDouble, typeInt, operatorMapper.get(">=")): typeBool,
      (typeDouble, typeInt, operatorMapper.get("==")): typeBool,
      (typeDouble, typeInt, operatorMapper.get("<>")): typeBool,
      (typeDouble, typeInt, operatorMapper.get("and")): typeError,
      (typeDouble, typeInt, operatorMapper.get("or")): typeError,
      (typeDouble, typeInt, operatorMapper.get("xor")): typeError,
      (typeDouble, typeInt, operatorMapper.get("=")): typeDouble,

      (typeDouble, typeChar, operatorMapper.get("+")): typeError, # Change to typeChar when vectors and matrices are implemented.
      (typeDouble, typeChar, operatorMapper.get("-")): typeError,
      (typeDouble, typeChar, operatorMapper.get("*")): typeError,
      (typeDouble, typeChar, operatorMapper.get("/")): typeError,
      (typeDouble, typeChar, operatorMapper.get("%")): typeError,
      (typeDouble, typeChar, operatorMapper.get("<")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeDouble, typeChar, operatorMapper.get(">")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeDouble, typeChar, operatorMapper.get("<=")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeDouble, typeChar, operatorMapper.get(">=")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeDouble, typeChar, operatorMapper.get("==")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeDouble, typeChar, operatorMapper.get("<>")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeDouble, typeChar, operatorMapper.get("and")): typeError,
      (typeDouble, typeChar, operatorMapper.get("or")): typeError,
      (typeDouble, typeChar, operatorMapper.get("xor")): typeError,
      (typeDouble, typeChar, operatorMapper.get("=")): typeError,

      (typeDouble, typeBool, operatorMapper.get("+")): typeError,
      (typeDouble, typeBool, operatorMapper.get("-")): typeError,
      (typeDouble, typeBool, operatorMapper.get("*")): typeError,
      (typeDouble, typeBool, operatorMapper.get("/")): typeError,
      (typeDouble, typeBool, operatorMapper.get("%")): typeError,
      (typeDouble, typeBool, operatorMapper.get("<")): typeError,
      (typeDouble, typeBool, operatorMapper.get(">")): typeError,
      (typeDouble, typeBool, operatorMapper.get("<=")): typeError,
      (typeDouble, typeBool, operatorMapper.get(">=")): typeError,
      (typeDouble, typeBool, operatorMapper.get("==")): typeError,
      (typeDouble, typeBool, operatorMapper.get("<>")): typeError,
      (typeDouble, typeBool, operatorMapper.get("and")): typeError,
      (typeDouble, typeBool, operatorMapper.get("or")): typeError,
      (typeDouble, typeBool, operatorMapper.get("xor")): typeError,
      (typeDouble, typeBool, operatorMapper.get("=")): typeError,

      # 'char' with all other primitive types
      (typeChar, typeChar, operatorMapper.get("+")): typeError, # Change to typeChar when vectors and matrices are implemented.
      (typeChar, typeChar, operatorMapper.get("-")): typeError,
      (typeChar, typeChar, operatorMapper.get("*")): typeError,
      (typeChar, typeChar, operatorMapper.get("/")): typeError,
      (typeChar, typeChar, operatorMapper.get("%")): typeError,
      (typeChar, typeChar, operatorMapper.get("<")): typeBool,
      (typeChar, typeChar, operatorMapper.get(">")): typeBool,
      (typeChar, typeChar, operatorMapper.get("<=")): typeBool,
      (typeChar, typeChar, operatorMapper.get(">=")): typeBool,
      (typeChar, typeChar, operatorMapper.get("==")): typeBool,
      (typeChar, typeChar, operatorMapper.get("<>")): typeBool,
      (typeChar, typeChar, operatorMapper.get("and")): typeError,
      (typeChar, typeChar, operatorMapper.get("or")): typeError,
      (typeChar, typeChar, operatorMapper.get("xor")): typeError,
      (typeChar, typeChar, operatorMapper.get("=")): typeChar,
      (typeNone, typeChar, operatorMapper.get("UMINUS")): typeError,
      (typeNone, typeChar, operatorMapper.get("~")): typeError,

      (typeChar, typeInt, operatorMapper.get("+")): typeError, # Change to typeChar when vectors and matrices are implemented.
      (typeChar, typeInt, operatorMapper.get("-")): typeError,
      (typeChar, typeInt, operatorMapper.get("*")): typeChar,
      (typeChar, typeInt, operatorMapper.get("/")): typeError,
      (typeChar, typeInt, operatorMapper.get("%")): typeError,
      (typeChar, typeInt, operatorMapper.get("<")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeChar, typeInt, operatorMapper.get(">")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeChar, typeInt, operatorMapper.get("<=")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeChar, typeInt, operatorMapper.get(">=")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeChar, typeInt, operatorMapper.get("==")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeChar, typeInt, operatorMapper.get("<>")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeChar, typeInt, operatorMapper.get("and")): typeError,
      (typeChar, typeInt, operatorMapper.get("or")): typeError,
      (typeChar, typeInt, operatorMapper.get("xor")): typeError,
      (typeChar, typeInt, operatorMapper.get("=")): typeError, # Change to typeChar when vectors and matrices are implemented.

      (typeChar, typeDouble, operatorMapper.get("+")): typeError, # Change to typeChar when vectors and matrices are implemented.
      (typeChar, typeDouble, operatorMapper.get("-")): typeError,
      (typeChar, typeDouble, operatorMapper.get("*")): typeError,
      (typeChar, typeDouble, operatorMapper.get("/")): typeError,
      (typeChar, typeDouble, operatorMapper.get("%")): typeError,
      (typeChar, typeDouble, operatorMapper.get("<")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeChar, typeDouble, operatorMapper.get(">")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeChar, typeDouble, operatorMapper.get("<=")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeChar, typeDouble, operatorMapper.get(">=")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeChar, typeDouble, operatorMapper.get("==")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeChar, typeDouble, operatorMapper.get("<>")): typeError, # Change to typeBool when vectors and matrices are implemented.
      (typeChar, typeDouble, operatorMapper.get("and")): typeError,
      (typeChar, typeDouble, operatorMapper.get("or")): typeError,
      (typeChar, typeDouble, operatorMapper.get("xor")): typeError,
      (typeChar, typeDouble, operatorMapper.get("=")): typeError, # Change to typeChar when vectors and matrices are implemented.

      (typeChar, typeBool, operatorMapper.get("+")): typeError, # Change to typeChar when vectors and matrices are implemented.
      (typeChar, typeBool, operatorMapper.get("-")): typeError,
      (typeChar, typeBool, operatorMapper.get("*")): typeError,
      (typeChar, typeBool, operatorMapper.get("/")): typeError,
      (typeChar, typeBool, operatorMapper.get("%")): typeError,
      (typeChar, typeBool, operatorMapper.get("<")): typeError,
      (typeChar, typeBool, operatorMapper.get(">")): typeError,
      (typeChar, typeBool, operatorMapper.get("<=")): typeError,
      (typeChar, typeBool, operatorMapper.get(">=")): typeError,
      (typeChar, typeBool, operatorMapper.get("==")): typeError,
      (typeChar, typeBool, operatorMapper.get("<>")): typeError,
      (typeChar, typeBool, operatorMapper.get("and")): typeError,
      (typeChar, typeBool, operatorMapper.get("or")): typeError,
      (typeChar, typeBool, operatorMapper.get("xor")): typeError,
      (typeChar, typeBool, operatorMapper.get("=")): typeError, # Change to typeChar when vectors and matrices are implemented.

      # 'bool' with all other data types
      (typeBool, typeBool, operatorMapper.get("+")): typeBool,
      (typeBool, typeBool, operatorMapper.get("-")): typeError,
      (typeBool, typeBool, operatorMapper.get("*")): typeBool,
      (typeBool, typeBool, operatorMapper.get("/")): typeError,
      (typeBool, typeBool, operatorMapper.get("%")): typeError,
      (typeBool, typeBool, operatorMapper.get("<")): typeError,
      (typeBool, typeBool, operatorMapper.get(">")): typeError,
      (typeBool, typeBool, operatorMapper.get("<=")): typeError,
      (typeBool, typeBool, operatorMapper.get(">=")): typeError,
      (typeBool, typeBool, operatorMapper.get("==")): typeBool,
      (typeBool, typeBool, operatorMapper.get("<>")): typeBool,
      (typeBool, typeBool, operatorMapper.get("and")): typeBool,
      (typeBool, typeBool, operatorMapper.get("or")): typeBool,
      (typeBool, typeBool, operatorMapper.get("xor")): typeBool,
      (typeBool, typeBool, operatorMapper.get("=")): typeBool,
      (typeNone, typeBool, operatorMapper.get("UMINUS")): typeError,
      (typeNone, typeBool, operatorMapper.get("~")): typeBool,

      (typeBool, typeInt, operatorMapper.get("+")): typeError,
      (typeBool, typeInt, operatorMapper.get("-")): typeError,
      (typeBool, typeInt, operatorMapper.get("*")): typeError,
      (typeBool, typeInt, operatorMapper.get("/")): typeError,
      (typeBool, typeInt, operatorMapper.get("%")): typeError,
      (typeBool, typeInt, operatorMapper.get("<")): typeError,
      (typeBool, typeInt, operatorMapper.get(">")): typeError,
      (typeBool, typeInt, operatorMapper.get("<=")): typeError,
      (typeBool, typeInt, operatorMapper.get(">=")): typeError,
      (typeBool, typeInt, operatorMapper.get("==")): typeError,
      (typeBool, typeInt, operatorMapper.get("<>")): typeError,
      (typeBool, typeInt, operatorMapper.get("and")): typeError,
      (typeBool, typeInt, operatorMapper.get("or")): typeError,
      (typeBool, typeInt, operatorMapper.get("xor")): typeError,
      (typeBool, typeInt, operatorMapper.get("=")): typeError,

      (typeBool, typeDouble, operatorMapper.get("+")): typeError,
      (typeBool, typeDouble, operatorMapper.get("-")): typeError,
      (typeBool, typeDouble, operatorMapper.get("*")): typeError,
      (typeBool, typeDouble, operatorMapper.get("/")): typeError,
      (typeBool, typeDouble, operatorMapper.get("%")): typeError,
      (typeBool, typeDouble, operatorMapper.get("<")): typeError,
      (typeBool, typeDouble, operatorMapper.get(">")): typeError,
      (typeBool, typeDouble, operatorMapper.get("<=")): typeError,
      (typeBool, typeDouble, operatorMapper.get(">=")): typeError,
      (typeBool, typeDouble, operatorMapper.get("==")): typeError,
      (typeBool, typeDouble, operatorMapper.get("<>")): typeError,
      (typeBool, typeDouble, operatorMapper.get("and")): typeError,
      (typeBool, typeDouble, operatorMapper.get("or")): typeError,
      (typeBool, typeDouble, operatorMapper.get("xor")): typeError,
      (typeBool, typeDouble, operatorMapper.get("=")): typeError,

      (typeBool, typeChar, operatorMapper.get("+")): typeError, # Change to typeChar when vectors and matrices are implemented.
      (typeBool, typeChar, operatorMapper.get("-")): typeError,
      (typeBool, typeChar, operatorMapper.get("*")): typeError,
      (typeBool, typeChar, operatorMapper.get("/")): typeError,
      (typeBool, typeChar, operatorMapper.get("%")): typeError,
      (typeBool, typeChar, operatorMapper.get("<")): typeError,
      (typeBool, typeChar, operatorMapper.get(">")): typeError,
      (typeBool, typeChar, operatorMapper.get("<=")): typeError,
      (typeBool, typeChar, operatorMapper.get(">=")): typeError,
      (typeBool, typeChar, operatorMapper.get("==")): typeError,
      (typeBool, typeChar, operatorMapper.get("<>")): typeError,
      (typeBool, typeChar, operatorMapper.get("and")): typeError,
      (typeBool, typeChar, operatorMapper.get("or")): typeError,
      (typeBool, typeChar, operatorMapper.get("xor")): typeError,
      (typeBool, typeChar, operatorMapper.get("=")): typeError,
    }
  
  def checkType(self, op, operType1, operType2):
    return self.cube[(operType1, operType2, op)]