# Kirin Programming Language
# SemanticCube class
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

from quadrupleManager import operToCode
from kirinMappers import typeToCode
from kirinMappers import operToCode

typeInt = typeToCode.get("int")
typeDouble = typeToCode.get("double")
typeChar = typeToCode.get("char")
typeBool = typeToCode.get("bool")
typeError = typeToCode.get("error")
typeNone = -1

class SemanticCube(object):

  def __init__(self):
    self.cube = {
      # 'int' with all other primitive data types.
      (typeInt, typeInt, operToCode.get("+")): typeInt,
      (typeInt, typeInt, operToCode.get("-")): typeInt,
      (typeInt, typeInt, operToCode.get("*")): typeInt,
      (typeInt, typeInt, operToCode.get("/")): typeDouble,
      (typeInt, typeInt, operToCode.get("%")): typeInt,
      (typeInt, typeInt, operToCode.get("<")): typeBool,
      (typeInt, typeInt, operToCode.get(">")): typeBool,
      (typeInt, typeInt, operToCode.get("<=")): typeBool,
      (typeInt, typeInt, operToCode.get(">=")): typeBool,
      (typeInt, typeInt, operToCode.get("==")): typeBool,
      (typeInt, typeInt, operToCode.get("<>")): typeBool,
      (typeInt, typeInt, operToCode.get("and")): typeError,
      (typeInt, typeInt, operToCode.get("or")): typeError,
      (typeInt, typeInt, operToCode.get("xor")): typeError,
      (typeInt, typeInt, operToCode.get("=")): typeInt,
      (typeNone, typeInt, operToCode.get("UMINUS")): typeInt,
      (typeNone, typeInt, operToCode.get("~")): typeError,
      
      (typeInt, typeDouble, operToCode.get("+")): typeDouble,
      (typeInt, typeDouble, operToCode.get("-")): typeDouble,
      (typeInt, typeDouble, operToCode.get("*")): typeDouble,
      (typeInt, typeDouble, operToCode.get("/")): typeDouble,
      (typeInt, typeDouble, operToCode.get("%")): typeError,
      (typeInt, typeDouble, operToCode.get("<")): typeBool,
      (typeInt, typeDouble, operToCode.get(">")): typeBool,
      (typeInt, typeDouble, operToCode.get("<=")): typeBool,
      (typeInt, typeDouble, operToCode.get(">=")): typeBool,
      (typeInt, typeDouble, operToCode.get("==")): typeBool,
      (typeInt, typeDouble, operToCode.get("<>")): typeBool,
      (typeInt, typeDouble, operToCode.get("and")): typeError,
      (typeInt, typeDouble, operToCode.get("or")): typeError,
      (typeInt, typeDouble, operToCode.get("xor")): typeError,
      (typeInt, typeDouble, operToCode.get("=")): typeInt,

      (typeInt, typeChar, operToCode.get("+")): typeError,
      (typeInt, typeChar, operToCode.get("-")): typeError,
      (typeInt, typeChar, operToCode.get("*")): typeError,
      (typeInt, typeChar, operToCode.get("/")): typeError,
      (typeInt, typeChar, operToCode.get("%")): typeError,
      (typeInt, typeChar, operToCode.get("<")): typeError,
      (typeInt, typeChar, operToCode.get(">")): typeError,
      (typeInt, typeChar, operToCode.get("<=")): typeError,
      (typeInt, typeChar, operToCode.get(">=")): typeError,
      (typeInt, typeChar, operToCode.get("==")): typeError,
      (typeInt, typeChar, operToCode.get("<>")): typeError,
      (typeInt, typeChar, operToCode.get("and")): typeError,
      (typeInt, typeChar, operToCode.get("or")): typeError,
      (typeInt, typeChar, operToCode.get("xor")): typeError,
      (typeInt, typeChar, operToCode.get("=")): typeError,

      (typeInt, typeBool, operToCode.get("+")): typeError,
      (typeInt, typeBool, operToCode.get("-")): typeError,
      (typeInt, typeBool, operToCode.get("*")): typeError,
      (typeInt, typeBool, operToCode.get("/")): typeError,
      (typeInt, typeBool, operToCode.get("%")): typeError,
      (typeInt, typeBool, operToCode.get("<")): typeError,
      (typeInt, typeBool, operToCode.get(">")): typeError,
      (typeInt, typeBool, operToCode.get("<=")): typeError,
      (typeInt, typeBool, operToCode.get(">=")): typeError,
      (typeInt, typeBool, operToCode.get("==")): typeError,
      (typeInt, typeBool, operToCode.get("<>")): typeError,
      (typeInt, typeBool, operToCode.get("and")): typeError,
      (typeInt, typeBool, operToCode.get("or")): typeError,
      (typeInt, typeBool, operToCode.get("xor")): typeError,
      (typeInt, typeBool, operToCode.get("=")): typeError,

      # 'double' with all other primitive data types.
      (typeDouble, typeDouble, operToCode.get("+")): typeDouble,
      (typeDouble, typeDouble, operToCode.get("-")): typeDouble,
      (typeDouble, typeDouble, operToCode.get("*")): typeDouble,
      (typeDouble, typeDouble, operToCode.get("/")): typeDouble,
      (typeDouble, typeDouble, operToCode.get("%")): typeError,
      (typeDouble, typeDouble, operToCode.get("<")): typeBool,
      (typeDouble, typeDouble, operToCode.get(">")): typeBool,
      (typeDouble, typeDouble, operToCode.get("<=")): typeBool,
      (typeDouble, typeDouble, operToCode.get(">=")): typeBool,
      (typeDouble, typeDouble, operToCode.get("==")): typeBool,
      (typeDouble, typeDouble, operToCode.get("<>")): typeBool,
      (typeDouble, typeDouble, operToCode.get("and")): typeError,
      (typeDouble, typeDouble, operToCode.get("or")): typeError,
      (typeDouble, typeDouble, operToCode.get("xor")): typeError,
      (typeDouble, typeDouble, operToCode.get("=")): typeDouble,
      (typeNone, typeDouble, operToCode.get("UMINUS")): typeDouble,
      (typeNone, typeDouble, operToCode.get("~")): typeError,

      (typeDouble, typeInt, operToCode.get("+")): typeDouble,
      (typeDouble, typeInt, operToCode.get("-")): typeDouble,
      (typeDouble, typeInt, operToCode.get("*")): typeDouble,
      (typeDouble, typeInt, operToCode.get("/")): typeDouble,
      (typeDouble, typeInt, operToCode.get("%")): typeError,
      (typeDouble, typeInt, operToCode.get("<")): typeBool,
      (typeDouble, typeInt, operToCode.get(">")): typeBool,
      (typeDouble, typeInt, operToCode.get("<=")): typeBool,
      (typeDouble, typeInt, operToCode.get(">=")): typeBool,
      (typeDouble, typeInt, operToCode.get("==")): typeBool,
      (typeDouble, typeInt, operToCode.get("<>")): typeBool,
      (typeDouble, typeInt, operToCode.get("and")): typeError,
      (typeDouble, typeInt, operToCode.get("or")): typeError,
      (typeDouble, typeInt, operToCode.get("xor")): typeError,
      (typeDouble, typeInt, operToCode.get("=")): typeDouble,

      (typeDouble, typeChar, operToCode.get("+")): typeError,
      (typeDouble, typeChar, operToCode.get("-")): typeError,
      (typeDouble, typeChar, operToCode.get("*")): typeError,
      (typeDouble, typeChar, operToCode.get("/")): typeError,
      (typeDouble, typeChar, operToCode.get("%")): typeError,
      (typeDouble, typeChar, operToCode.get("<")): typeError,
      (typeDouble, typeChar, operToCode.get(">")): typeError,
      (typeDouble, typeChar, operToCode.get("<=")): typeError,
      (typeDouble, typeChar, operToCode.get(">=")): typeError,
      (typeDouble, typeChar, operToCode.get("==")): typeError,
      (typeDouble, typeChar, operToCode.get("<>")): typeError,
      (typeDouble, typeChar, operToCode.get("and")): typeError,
      (typeDouble, typeChar, operToCode.get("or")): typeError,
      (typeDouble, typeChar, operToCode.get("xor")): typeError,
      (typeDouble, typeChar, operToCode.get("=")): typeError,

      (typeDouble, typeBool, operToCode.get("+")): typeError,
      (typeDouble, typeBool, operToCode.get("-")): typeError,
      (typeDouble, typeBool, operToCode.get("*")): typeError,
      (typeDouble, typeBool, operToCode.get("/")): typeError,
      (typeDouble, typeBool, operToCode.get("%")): typeError,
      (typeDouble, typeBool, operToCode.get("<")): typeError,
      (typeDouble, typeBool, operToCode.get(">")): typeError,
      (typeDouble, typeBool, operToCode.get("<=")): typeError,
      (typeDouble, typeBool, operToCode.get(">=")): typeError,
      (typeDouble, typeBool, operToCode.get("==")): typeError,
      (typeDouble, typeBool, operToCode.get("<>")): typeError,
      (typeDouble, typeBool, operToCode.get("and")): typeError,
      (typeDouble, typeBool, operToCode.get("or")): typeError,
      (typeDouble, typeBool, operToCode.get("xor")): typeError,
      (typeDouble, typeBool, operToCode.get("=")): typeError,

      # 'char' with all other primitive types
      (typeChar, typeChar, operToCode.get("+")): typeChar,
      (typeChar, typeChar, operToCode.get("-")): typeError,
      (typeChar, typeChar, operToCode.get("*")): typeError,
      (typeChar, typeChar, operToCode.get("/")): typeError,
      (typeChar, typeChar, operToCode.get("%")): typeError,
      (typeChar, typeChar, operToCode.get("<")): typeBool,
      (typeChar, typeChar, operToCode.get(">")): typeBool,
      (typeChar, typeChar, operToCode.get("<=")): typeBool,
      (typeChar, typeChar, operToCode.get(">=")): typeBool,
      (typeChar, typeChar, operToCode.get("==")): typeBool,
      (typeChar, typeChar, operToCode.get("<>")): typeBool,
      (typeChar, typeChar, operToCode.get("and")): typeError,
      (typeChar, typeChar, operToCode.get("or")): typeError,
      (typeChar, typeChar, operToCode.get("xor")): typeError,
      (typeChar, typeChar, operToCode.get("=")): typeChar,
      (typeNone, typeChar, operToCode.get("UMINUS")): typeError,
      (typeNone, typeChar, operToCode.get("~")): typeError,

      (typeChar, typeInt, operToCode.get("+")): typeError,
      (typeChar, typeInt, operToCode.get("-")): typeError,
      (typeChar, typeInt, operToCode.get("*")): typeError,
      (typeChar, typeInt, operToCode.get("/")): typeError,
      (typeChar, typeInt, operToCode.get("%")): typeError,
      (typeChar, typeInt, operToCode.get("<")): typeError,
      (typeChar, typeInt, operToCode.get(">")): typeError,
      (typeChar, typeInt, operToCode.get("<=")): typeError,
      (typeChar, typeInt, operToCode.get(">=")): typeError,
      (typeChar, typeInt, operToCode.get("==")): typeError,
      (typeChar, typeInt, operToCode.get("<>")): typeError,
      (typeChar, typeInt, operToCode.get("and")): typeError,
      (typeChar, typeInt, operToCode.get("or")): typeError,
      (typeChar, typeInt, operToCode.get("xor")): typeError,
      (typeChar, typeInt, operToCode.get("=")): typeError,

      (typeChar, typeDouble, operToCode.get("+")): typeError,
      (typeChar, typeDouble, operToCode.get("-")): typeError,
      (typeChar, typeDouble, operToCode.get("*")): typeError,
      (typeChar, typeDouble, operToCode.get("/")): typeError,
      (typeChar, typeDouble, operToCode.get("%")): typeError,
      (typeChar, typeDouble, operToCode.get("<")): typeError,
      (typeChar, typeDouble, operToCode.get(">")): typeError,
      (typeChar, typeDouble, operToCode.get("<=")): typeError,
      (typeChar, typeDouble, operToCode.get(">=")): typeError,
      (typeChar, typeDouble, operToCode.get("==")): typeError,
      (typeChar, typeDouble, operToCode.get("<>")): typeError,
      (typeChar, typeDouble, operToCode.get("and")): typeError,
      (typeChar, typeDouble, operToCode.get("or")): typeError,
      (typeChar, typeDouble, operToCode.get("xor")): typeError,
      (typeChar, typeDouble, operToCode.get("=")): typeError,

      (typeChar, typeBool, operToCode.get("+")): typeError,
      (typeChar, typeBool, operToCode.get("-")): typeError,
      (typeChar, typeBool, operToCode.get("*")): typeError,
      (typeChar, typeBool, operToCode.get("/")): typeError,
      (typeChar, typeBool, operToCode.get("%")): typeError,
      (typeChar, typeBool, operToCode.get("<")): typeError,
      (typeChar, typeBool, operToCode.get(">")): typeError,
      (typeChar, typeBool, operToCode.get("<=")): typeError,
      (typeChar, typeBool, operToCode.get(">=")): typeError,
      (typeChar, typeBool, operToCode.get("==")): typeError,
      (typeChar, typeBool, operToCode.get("<>")): typeError,
      (typeChar, typeBool, operToCode.get("and")): typeError,
      (typeChar, typeBool, operToCode.get("or")): typeError,
      (typeChar, typeBool, operToCode.get("xor")): typeError,
      (typeChar, typeBool, operToCode.get("=")): typeError,

      # 'bool' with all other data types
      (typeBool, typeBool, operToCode.get("+")): typeBool,
      (typeBool, typeBool, operToCode.get("-")): typeError,
      (typeBool, typeBool, operToCode.get("*")): typeBool,
      (typeBool, typeBool, operToCode.get("/")): typeError,
      (typeBool, typeBool, operToCode.get("%")): typeError,
      (typeBool, typeBool, operToCode.get("<")): typeError,
      (typeBool, typeBool, operToCode.get(">")): typeError,
      (typeBool, typeBool, operToCode.get("<=")): typeError,
      (typeBool, typeBool, operToCode.get(">=")): typeError,
      (typeBool, typeBool, operToCode.get("==")): typeBool,
      (typeBool, typeBool, operToCode.get("<>")): typeBool,
      (typeBool, typeBool, operToCode.get("and")): typeBool,
      (typeBool, typeBool, operToCode.get("or")): typeBool,
      (typeBool, typeBool, operToCode.get("xor")): typeBool,
      (typeBool, typeBool, operToCode.get("=")): typeBool,
      (typeNone, typeBool, operToCode.get("UMINUS")): typeError,
      (typeNone, typeBool, operToCode.get("~")): typeBool,

      (typeBool, typeInt, operToCode.get("+")): typeError,
      (typeBool, typeInt, operToCode.get("-")): typeError,
      (typeBool, typeInt, operToCode.get("*")): typeError,
      (typeBool, typeInt, operToCode.get("/")): typeError,
      (typeBool, typeInt, operToCode.get("%")): typeError,
      (typeBool, typeInt, operToCode.get("<")): typeError,
      (typeBool, typeInt, operToCode.get(">")): typeError,
      (typeBool, typeInt, operToCode.get("<=")): typeError,
      (typeBool, typeInt, operToCode.get(">=")): typeError,
      (typeBool, typeInt, operToCode.get("==")): typeError,
      (typeBool, typeInt, operToCode.get("<>")): typeError,
      (typeBool, typeInt, operToCode.get("and")): typeError,
      (typeBool, typeInt, operToCode.get("or")): typeError,
      (typeBool, typeInt, operToCode.get("xor")): typeError,
      (typeBool, typeInt, operToCode.get("=")): typeError,

      (typeBool, typeDouble, operToCode.get("+")): typeError,
      (typeBool, typeDouble, operToCode.get("-")): typeError,
      (typeBool, typeDouble, operToCode.get("*")): typeError,
      (typeBool, typeDouble, operToCode.get("/")): typeError,
      (typeBool, typeDouble, operToCode.get("%")): typeError,
      (typeBool, typeDouble, operToCode.get("<")): typeError,
      (typeBool, typeDouble, operToCode.get(">")): typeError,
      (typeBool, typeDouble, operToCode.get("<=")): typeError,
      (typeBool, typeDouble, operToCode.get(">=")): typeError,
      (typeBool, typeDouble, operToCode.get("==")): typeError,
      (typeBool, typeDouble, operToCode.get("<>")): typeError,
      (typeBool, typeDouble, operToCode.get("and")): typeError,
      (typeBool, typeDouble, operToCode.get("or")): typeError,
      (typeBool, typeDouble, operToCode.get("xor")): typeError,
      (typeBool, typeDouble, operToCode.get("=")): typeError,

      (typeBool, typeChar, operToCode.get("+")): typeError,
      (typeBool, typeChar, operToCode.get("-")): typeError,
      (typeBool, typeChar, operToCode.get("*")): typeError,
      (typeBool, typeChar, operToCode.get("/")): typeError,
      (typeBool, typeChar, operToCode.get("%")): typeError,
      (typeBool, typeChar, operToCode.get("<")): typeError,
      (typeBool, typeChar, operToCode.get(">")): typeError,
      (typeBool, typeChar, operToCode.get("<=")): typeError,
      (typeBool, typeChar, operToCode.get(">=")): typeError,
      (typeBool, typeChar, operToCode.get("==")): typeError,
      (typeBool, typeChar, operToCode.get("<>")): typeError,
      (typeBool, typeChar, operToCode.get("and")): typeError,
      (typeBool, typeChar, operToCode.get("or")): typeError,
      (typeBool, typeChar, operToCode.get("xor")): typeError,
      (typeBool, typeChar, operToCode.get("=")): typeError
    }
  
  def checkType(self, op, operType1, operType2):
    # If the types of both operands are strings (i.e. both are objects)...
    if type(operType1) is str and type(operType2) is str:
      # If both are of the same class...
      if operType1 == operType2:
        if op == operToCode.get("=="):
          return typeBool
        elif op == operToCode.get("<>"):
          return typeBool
        elif op == operToCode.get("="):
          return operType1
        # Operators different from '==', '<>' and '=' are not allowed between objects.
        else:
          return typeError
      # Cannot do operations between objects of different classes.
      # TODO: This might need to change when inheritance is implemented.
      else:
        return typeError
    
    # If one of the operands is an object and the other one is not, then it is an error.
    elif type(operType1) is str or type(operType2) is str:
      return typeError
    
    # If the key (operType1, operType2, op) is not in the internal dictionary, then it is an error.
    elif (operType1, operType2, op) not in self.cube:
      return typeError
    
    # Handles the case of the primitive types.
    return self.cube[(operType1, operType2, op)]