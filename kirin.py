# Kirin Programming Language
# Kirin Virtual Machine
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

import sys
from stack import Stack
from queue import Queue
# from kirin_yacc import CONST_G_BEGIN_INT
# from kirin_yacc import CONST_G_BEGIN_DOUBLE
# from kirin_yacc import CONST_G_BEGIN_CHAR
# from kirin_yacc import CONST_G_BEGIN_BOOL
# from kirin_yacc import CONST_L_BEGIN_INT
# from kirin_yacc import CONST_L_BEGIN_DOUBLE
# from kirin_yacc import CONST_L_BEGIN_CHAR
# from kirin_yacc import CONST_L_BEGIN_BOOL
# from kirin_yacc import CONST_T_BEGIN_INT
# from kirin_yacc import CONST_T_BEGIN_DOUBLE
# from kirin_yacc import CONST_T_BEGIN_CHAR
# from kirin_yacc import CONST_T_BEGIN_BOOL
# from kirin_yacc import CONST_CT_BEGIN_INT
# from kirin_yacc import CONST_CT_BEGIN_DOUBLE
# from kirin_yacc import CONST_CT_BEGIN_CHAR
# from kirin_yacc import CONST_CT_BEGIN_BOOL
CONST_RETURN = -2
CONST_G_BEGIN_INT = 0
CONST_G_BEGIN_DOUBLE = 1000
CONST_G_BEGIN_CHAR = 2000
CONST_G_BEGIN_BOOL = 3000
CONST_L_BEGIN_INT = 10000
CONST_L_BEGIN_DOUBLE = 11000
CONST_L_BEGIN_CHAR = 12000
CONST_L_BEGIN_BOOL = 13000
CONST_T_BEGIN_INT = 20000
CONST_T_BEGIN_DOUBLE = 21000
CONST_T_BEGIN_CHAR = 22000
CONST_T_BEGIN_BOOL = 23000
CONST_CT_BEGIN_INT = 30000
CONST_CT_BEGIN_DOUBLE = 31000
CONST_CT_BEGIN_CHAR = 32000
CONST_CT_BEGIN_BOOL = 33000
from quadrupleManager import operToCode

# Constants indicating the start of each type of memory addresses.
CONST_GLOBAL_START = CONST_G_BEGIN_INT
CONST_LOCAL_START = CONST_L_BEGIN_INT
CONST_CONSTANT_START = CONST_CT_BEGIN_INT

# Global variables.
quadList = []
memHeap = {} # Dictionary of global memory addresses.
memStack = [{}] # Local memory stack (each position within the stack is a activationRecord dict).
memConst = {} # Dictionary of memory addresses for constants.
currentStackLevel = 0 # Keeps track of the current activationRecord.
prevStackLevel = Stack()
prevStackLevel.push(currentStackLevel)
editingContext = 0
stackDicReferences = [{}] # Holds, for each activationRecord in the local memory stack, which addresses are references and the values they reference.
queueParams = Queue() # A queue for holding the values of the params
instructionPointer = 0
prevInstructionPointer = Stack()
inputBuffer = ""
inputBufferCont = 0

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
    targetStackLevel, targetAddress = stackDicReferences[currentStackLevel][address]
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
    targetStackLevel, targetAddress = stackDicReferences[currentStackLevel][address]
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
    quadList[index][0] = int(quadList[index][0])
    quadList[index][1] = int(quadList[index][1])
    if quadList[index][2] == "true":
      quadList[index][2] = True
    elif quadList[index][2] == "false":
      quadList[index][2] = False
    try: 
      quadList[index][2] = int(quadList[index][2])
    except ValueError:
      try:
        quadList[index][2] = float(quadList[index][2])
      except ValueError:
        quadList[index][2] = quadList[index][2]
      
    quadList[index][3] = int(quadList[index][3])

# quad = A quadruple in the form of a list of 4 values.
def executeQuad(quad):
  global inputBuffer, inputBufferCont, instructionPointer, editingContext, currentStackLevel, prevStackLevel, queueParams, stackDicReferences

  # OPER -> =
  if quad[0] == operToCode.get("="):
    if getType(quad[3]) == "int":
      if getType(quad[2]) == "int":
        if quad[3] >= 30000:
          setValue(quad[3], quad[2])
        else:
          setValue(quad[3], extractValue(quad[2]))
      elif getType(quad[2]) == "double":
        if quad[3] >= 30000:
          setValue(quad[3], round(quad[2]))
        else:
          setValue(quad[3], round(extractValue(quad[2])))
      # End of quad[3] being an int.
    elif getType(quad[3]) == "double":
      if quad[3] >= 30000:
        setValue(quad[3], quad[2])
      else:
        setValue(quad[3], extractValue(quad[2]))
      # End of quad[3] being a double.
    elif getType(quad[3]) == "char":
      if quad[3] >= 30000:
        setValue(quad[3], quad[2])
      else:
        setValue(quad[3], extractValue(quad[2]))
      # End of quad[3] being a char.
      # TODO: In compilation remove the single quotes.
    elif getType(quad[3]) == "bool":
      if quad[3] >= 30000:
        setValue(quad[3], quad[2])
      else:
        setValue(quad[3], extractValue(quad[2]))
      # End of quad[3] being a bool.

  # OPER -> +
  if quad[0] == operToCode.get("+"):
    if getType(quad[1]) == "int":
      if getType(quad[2]) == "int":
        ans = extractValue(quad[1]) + extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "double":
        ans = extractValue(quad[1]) + extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an int.
    elif getType(quad[1]) == "double":
      if getType(quad[2]) == "double":
        ans = extractValue(quad[1]) + extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[1]) == "int":
        ans = extractValue(quad[1]) + extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an double.
    # TODO: If quad[1] and quad[2] are both char's, this is solved in compilation via Array Operation.
    elif getType(quad[1]) == "bool":
      if getType(quad[2]) == "bool":
        ans = extractValue(quad[1]) or extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being a bool.

  # OPER -> -
  if quad[0] == operToCode.get("-"):
    if getType(quad[1]) == "int":
      if getType(quad[2]) == "int":
        ans = extractValue(quad[1]) - extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "double":
        ans = extractValue(quad[1]) - extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an int.
    elif getType(quad[1]) == "double":
      if getType(quad[2]) == "double":
        ans = extractValue(quad[1]) - extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "int":
        ans = extractValue(quad[1]) - extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an double.

  # OPER -> *
  if quad[0] == operToCode.get("*"):
    if getType(quad[1]) == "int":
      if getType(quad[2]) == "int":
        ans = extractValue(quad[1]) * extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "double":
        ans = extractValue(quad[1]) * extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an int.
    elif getType(quad[1]) == "double":
      if getType(quad[2]) == "double":
        ans = extractValue(quad[1]) * extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "int":
        ans = extractValue(quad[1]) * extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an double.
    # TODO: If quad[1] and quad[2] are both char's, this is solved in compilation via Array Operation.
    elif getType(quad[1]) == "bool":
      if getType(quad[2]) == "bool":
        ans = extractValue(quad[1]) and extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being a bool.

  # OPER -> /
  if quad[0] == operToCode.get("/"):
    if getType(quad[1]) == "int":
      if getType(quad[2]) == "int":
        ans = extractValue(quad[1]) / extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "double":
        ans = extractValue(quad[1]) / extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an int.
    elif getType(quad[1]) == "double":
      if getType(quad[2]) == "double":
        ans = extractValue(quad[1]) / extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "int":
        ans = extractValue(quad[1]) / extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an double.

  # OPER -> %
  if quad[0] == operToCode.get("%"):
    if getType(quad[1]) == "int":
      if getType(quad[2]) == "int":
        ans = extractValue(quad[1]) % extractValue(quad[2])
        setValue(quad[3], ans)

  # OPER -> UMINUS
  if quad[0] == operToCode.get("UMINUS"):
    if getType(quad[2]) == "int":
      setValue(quad[3], -extractValue(quad[2]))
    elif getType(quad[2]) == "double":
      setValue(quad[3], -extractValue(quad[2]))

  # OPER -> >
  if quad[0] == operToCode.get(">"):
    if getType(quad[1]) == "int":
      if getType(quad[2]) == "int":
        ans = extractValue(quad[1]) > extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "double":
        ans = extractValue(quad[1]) > extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an int.
    elif getType(quad[1]) == "double":
      if getType(quad[2]) == "double":
        ans = extractValue(quad[1]) > extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "int":
        ans = extractValue(quad[1]) > extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an double.
    elif getType(quad[1]) == "char":
      if getType(quad[2]) == "char":
        ans = extractValue(quad[1]) > extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an char.

  # OPER -> >=
  if quad[0] == operToCode.get(">="):
    if getType(quad[1]) == "int":
      if getType(quad[2]) == "int":
        ans = extractValue(quad[1]) >= extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "double":
        ans = extractValue(quad[1]) >= extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an int.
    elif getType(quad[1]) == "double":
      if getType(quad[2]) == "double":
        ans = extractValue(quad[1]) >= extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "int":
        ans = extractValue(quad[1]) >= extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an double.
    elif getType(quad[1]) == "char":
      if getType(quad[2]) == "char":
        ans = extractValue(quad[1]) >= extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an char.

  # OPER -> <
  if quad[0] == operToCode.get("<"):
    if getType(quad[1]) == "int":
      if getType(quad[2]) == "int":
        ans = extractValue(quad[1]) < extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "double":
        ans = extractValue(quad[1]) < extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an int.
    elif getType(quad[1]) == "double":
      if getType(quad[2]) == "double":
        ans = extractValue(quad[1]) < extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "int":
        ans = extractValue(quad[1]) < extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an double.
    elif getType(quad[1]) == "char":
      if getType(quad[2]) == "char":
        ans = extractValue(quad[1]) < extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an char.

  # OPER -> <=
  if quad[0] == operToCode.get("<="):
    if getType(quad[1]) == "int":
      if getType(quad[2]) == "int":
        ans = extractValue(quad[1]) <= extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "double":
        ans = extractValue(quad[1]) <= extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an int.
    elif getType(quad[1]) == "double":
      if getType(quad[2]) == "double":
        ans = extractValue(quad[1]) <= extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "int":
        ans = extractValue(quad[1]) <= extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an double.
    elif getType(quad[1]) == "char":
      if getType(quad[2]) == "char":
        ans = extractValue(quad[1]) <= extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an char.

  # OPER -> ==
  if quad[0] == operToCode.get("=="):
    if getType(quad[1]) == "int":
      if getType(quad[2]) == "int":
        ans = extractValue(quad[1]) == extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "double":
        ans = extractValue(quad[1]) == extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an int.
    elif getType(quad[1]) == "double":
      if getType(quad[2]) == "double":
        ans = extractValue(quad[1]) == extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "int":
        ans = extractValue(quad[1]) == extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an double.
    elif getType(quad[1]) == "char":
      if getType(quad[2]) == "char":
        ans = extractValue(quad[1]) == extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an char.
    elif getType(quad[1]) == "bool":
      if getType(quad[2]) == "bool":
        ans = extractValue(quad[1]) == extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being a bool.

  # OPER -> <>
  if quad[0] == operToCode.get("<>"):
    if getType(quad[1]) == "int":
      if getType(quad[2]) == "int":
        ans = extractValue(quad[1]) != extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "double":
        ans = extractValue(quad[1]) != extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an int.
    elif getType(quad[1]) == "double":
      if getType(quad[2]) == "double":
        ans = extractValue(quad[1]) != extractValue(quad[2])
        setValue(quad[3], ans)
      elif getType(quad[2]) == "int":
        ans = extractValue(quad[1]) != extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an double.
    elif getType(quad[1]) == "char":
      if getType(quad[2]) == "char":
        ans = extractValue(quad[1]) != extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being an char.
    elif getType(quad[1]) == "bool":
      if getType(quad[2]) == "bool":
        ans = extractValue(quad[1]) != extractValue(quad[2])
        setValue(quad[3], ans)
      # End of quad[1] being a bool.

  # OPER -> ~
  if quad[0] == operToCode.get("~"):
    if getType(quad[2]) == "bool":
      ans = not extractValue(quad[2])
      setValue(quad[3], ans)

  # OPER -> print
  if quad[0] == operToCode.get("print"):
    # print("print")
    if quad[3] == -1:
      print()
    elif getType(quad[3]) == "int":
      print(extractValue(quad[3]), end = "")
    elif getType(quad[3]) == "double":
      print(extractValue(quad[3]), end = "")
    elif getType(quad[3]) == "char":
      print(extractValue(quad[3]), end = "")
    elif getType(quad[3]) == "bool":
      print(extractValue(quad[3]), end = "")

  # OPER -> scan
  if quad[0] == operToCode.get("scan"):
    if quad[1] == 0:    # BUFFER START
      inputBuffer = input()
      inputBufferCont = 0
      if getType(quad[3]) == "int":
        setValue(quad[3], int(inputBuffer))
      elif getType(quad[3]) == "double":
        setValue(quad[3], float(inputBuffer))
      elif getType(quad[3]) == "char":
        setValue(quad[3], inputBuffer[inputBufferCont])
        inputBufferCont = inputBufferCont + 1
      elif getType(quad[3]) == "bool":
        setValue(quad[3], inputBuffer == 'true')
    # End Buffer Start

    if quad[1] == -1:
      if getType(quad[3]) == "char":
        setValue(quad[3], inputBuffer[inputBufferCont])
        inputBufferCont = inputBufferCont + 1

    # End Buffer Fill

    if quad[1] == 1:
      if getType(quad[3]) == "char":
        setValue(quad[3], inputBuffer[inputBufferCont])
        inputBuffer = ""
        inputBufferCont = 0

    # End Buffer End 

  # OPER -> GOTO
  if quad[0] == operToCode.get("GOTO"):
    instructionPointer = quad[3] - 1

  # OPER -> GOTOF
  if quad[0] == operToCode.get("GOTOF"):
    if not extractValue(quad[1]):
      instructionPointer = quad[3] - 1

  # OPER -> GOTOT
  if quad[0] == operToCode.get("GOTOT"):
    if quad[1]:
      instructionPointer = quad[3] - 1

  # OPER -> GOSUB
  if quad[0] == operToCode.get("GOSUB"):
    prevStackLevel.push(currentStackLevel)
    currentStackLevel = editingContext
    prevInstructionPointer.push(instructionPointer)
    instructionPointer = quad[3] - 1


  # OPER -> ERA
  if quad[0] == operToCode.get("ERA"):
    editingContext = editingContext + 1
    if len(stackDicReferences) <= editingContext:
      stackDicReferences.append({})
      memStack.append({})


  # OPER -> PARAM
  if quad[0] == operToCode.get("PARAM"):
    value = extractValue(quad[3])
    queueParams.push(value)


  # OPER -> PARAM_REF
  if quad[0] == operToCode.get("PARAM_REF"):
    pass

  # OPER -> LOAD_PARAM
  if quad[0] == operToCode.get("LOAD_PARAM"):
    value = queueParams.front()
    queueParams.pop()
    setValue(quad[3], value)


  # OPER -> RETURN
  if quad[0] == operToCode.get("RETURN"):
    setValue(CONST_RETURN, extractValue(quad[1]))
    if currentStackLevel == 0:
      print("Program has finished successfully!")
      sys.exit(0)
    editingContext = editingContext - 1
    instructionPointer = prevInstructionPointer.pop()
    currentStackLevel = prevStackLevel.pop()


  # OPER -> ENDPROC
  if quad[0] == operToCode.get("ENDPROC"):
    if currentStackLevel == 0:
      print("Program has finished successfully!")
      sys.exit(0)
    editingContext = editingContext - 1
    instructionPointer = prevInstructionPointer.pop()
    currentStackLevel = prevStackLevel.pop()


  # OPER -> VER
  if quad[0] == operToCode.get("VER"):
    if extractValue(quad[1]) >= quad[3]:
      print("Runtime Error: Index out of bounds.")
      sys.exit(0)
  

  # OPER -> REF
  if quad[0] == operToCode.get("REF"):
    stackDicReferences[currentStackLevel][quad[3]] = (currentStackLevel, extractValue(quad[3]))

  
  # OPER -> DEREF
  if quad[0] == operToCode.get("DEREF"):
    if quad[3] in stackDicReferences[currentStackLevel]:
      del stackDicReferences[currentStackLevel][quad[3]]

# Main
if len(sys.argv) != 2:
  print("Error: Expected usage is %s name_of_file" %(sys.argv[0]))
  sys.exit(0)

loadQuadList(sys.argv[1])
while(True):
  # print(quadList[instructionPointer])
  executeQuad(quadList[instructionPointer])
  instructionPointer = instructionPointer + 1