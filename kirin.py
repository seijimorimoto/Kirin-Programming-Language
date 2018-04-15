# Kirin Programming Language
# Kirin Virtual Machine
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

import sys
from kirin_yacc import CONST_G_BEGIN_INT
from kirin_yacc import CONST_G_BEGIN_DOUBLE
from kirin_yacc import CONST_G_BEGIN_CHAR
from kirin_yacc import CONST_G_BEGIN_BOOL
from kirin_yacc import CONST_L_BEGIN_INT
from kirin_yacc import CONST_L_BEGIN_DOUBLE
from kirin_yacc import CONST_L_BEGIN_CHAR
from kirin_yacc import CONST_L_BEGIN_BOOL
from kirin_yacc import CONST_T_BEGIN_INT
from kirin_yacc import CONST_T_BEGIN_DOUBLE
from kirin_yacc import CONST_T_BEGIN_CHAR
from kirin_yacc import CONST_T_BEGIN_BOOL
from kirin_yacc import CONST_CT_BEGIN_INT
from kirin_yacc import CONST_CT_BEGIN_DOUBLE
from kirin_yacc import CONST_CT_BEGIN_CHAR
from kirin_yacc import CONST_CT_BEGIN_BOOL
from quadrupleManager import operToCode

# Constants indicating the start of each type of memory addresses.
CONST_GLOBAL_START = CONST_G_BEGIN_INT
CONST_LOCAL_START = CONST_L_BEGIN_INT
CONST_CONSTANT_START = CONST_CT_BEGIN_INT

# Global variables.
quadList = []
memHeap = {} # Dictionary of global memory addresses.
memStack = [] # Local memory stack (each position within the stack is a activationRecord dict).
memConst = {} # Dictionary of memory addresses for constants.
currentStackLevel = 0 # Keeps track of the current activationRecord.
stackDicReferences = [{}] # Holds, for each activationRecord in the local memory stack, which addresses are references and the values they reference.
queueParams = [] # A queue for holding the values of the params
instructionPointer = 0

# Returns the type (as string) associated to a given address.
def getType(address):
  if address < CONST_G_BEGIN_DOUBLE:
    return "int"
  if address < CONST_G_BEGIN_CHAR:
    return "double"
  if address < CONST_G_BEGIN_BOOL:
    return "char"
  if address < CONST_L_BEGIN_INT:
    return "bool"
  if address < CONST_L_BEGIN_DOUBLE:
    return "int"
  if address < CONST_L_BEGIN_CHAR:
    return "double"
  if address < CONST_L_BEGIN_BOOL:
    return "char"
  if address < CONST_T_BEGIN_INT:
    return "bool"
  if address < CONST_T_BEGIN_DOUBLE:
    return "int"
  if address < CONST_T_BEGIN_CHAR:
    return "double"
  if address < CONST_T_BEGIN_BOOL:
    return "char"
  if address < CONST_CT_BEGIN_INT:
    return "bool"
  if address < CONST_CT_BEGIN_DOUBLE:
    return "int"
  if address < CONST_CT_BEGIN_CHAR:
    return "double"
  if address < CONST_CT_BEGIN_BOOL:
    return "char"
  return "bool"

# Returns the value associated to a given address (can be global, local or constant).
def extractValue(address):
  # Verify if the address is global.
  if address < CONST_LOCAL_START:
    return memHeap[address]
  
  # Verify if the address is constant.
  if address >= CONST_CONSTANT_START:
    return memConst[address]

  # From here on, we know the address is local.
  # Check if the address is a reference to another address.
  if address in stackDicReferences[currentStackLevel]:
    targetStackLevel, targetAddress = stackDicReferences[currentStackLevel]
    # Return value contained in the reference.
    return memStack[targetStackLevel][targetAddress]

  # Return value contained in address.
  return memStack[currentStackLevel][address]

# Sets the value associated to a given address (can be global, local or constant).
def setValue(address, value):
  # Verify if the address is global.
  if address < CONST_LOCAL_START:
    memHeap[address] = value
  
  # Verify if the address is constant.
  elif address >= CONST_CONSTANT_START:
    memConst[address] = value

  # From here on, we know the address is local.
  # Check if the address is a reference to another address.
  elif address in stackDicReferences[currentStackLevel]:
    targetStackLevel, targetAddress = stackDicReferences[currentStackLevel]
    # Set the value in the referenced address.
    memStack[targetStackLevel][targetAddress] = value
  
  # Set the value in address.
  else:
    memStack[currentStackLevel][address] = value

# Loads the quadruples from an object file named fileName into the quadList.
def loadQuadList(fileName):
  global quadList
  file = open(fileName, 'r')
  quadList = file.readlines()
  for index in range(len(quadList)):
    quadList[index] = quadList[index].split(" ")

# quad = A quadruple in the form of a list of 4 values.
def executeQuad(quad):
  if quad[0] == operToCode.get("="):
    if getType(quad[3]) == "int":
      if getType(quad[2]) == "int":
        setValue(quad[3], extractValue(quad[2]))
      elif getType(quad[2]) == "double":
        setValue(quad[3], round(extractValue(quad[2])))
      # End of quad[3] being an int.
    elif getType(quad[3]) == "double":
      setValue(quad[3], extractValue(quad[2]))
      # End of quad[3] being a double.
    elif getType(quad[3]) == "char":
      setValue(quad[3], extractValue(quad[2]))
      # End of quad[3] being a char.
      # TODO: In compilation remove the single quotes.
    elif getType(quad[4]) == "bool":
      setValue(quad[3], extractValue(quad[2]))
      # End of quad[3] being a bool.

# Main
if len(sys.argv) != 2:
  print("Error: Expected usage is %s name_of_file" %(sys.argv[0]))
  sys.exit(0)

loadQuadList(sys.argv[1])
while(True):
  executeQuad(quadList[instructionPointer])
  instructionPointer = instructionPointer + 1