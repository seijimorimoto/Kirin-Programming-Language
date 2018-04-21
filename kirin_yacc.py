# Kirin Programming Language
# Syntax File
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

import sys
import ply.yacc as yacc

from kirin_lex import tokens
from funcDirTable import FuncDirTable
from funcDirRow import FuncDirRow
from varTableRow import VarTableRow
from semanticCube import keywordMapper
from semanticCube import invKeywordMapper
from semanticCube import SemanticCube
from quadrupleManager import QuadrupleManager
from quadrupleManager import operToCode
from quadrupleManager import codeToOper
from stack import Stack

# Constants for initializing memory addresses.
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

# Initialization of global counters
gInt = CONST_G_BEGIN_INT
gDouble = CONST_G_BEGIN_DOUBLE
gChar = CONST_G_BEGIN_CHAR
gBool = CONST_G_BEGIN_BOOL
lInt = CONST_L_BEGIN_INT
lDouble = CONST_L_BEGIN_DOUBLE
lChar = CONST_L_BEGIN_CHAR
lBool = CONST_L_BEGIN_BOOL
tInt = CONST_T_BEGIN_INT
tDouble = CONST_T_BEGIN_DOUBLE
tChar = CONST_T_BEGIN_CHAR
tBool = CONST_T_BEGIN_BOOL
ctInt = CONST_CT_BEGIN_INT
ctDouble = CONST_CT_BEGIN_DOUBLE
ctChar = CONST_CT_BEGIN_CHAR
ctBool = CONST_CT_BEGIN_BOOL

# Initialize global variables with default values
classDirTable = {}
funcDirTable = FuncDirTable()
quadManager = QuadrupleManager()
semanticCube = SemanticCube()
currentClass = ""
currentMethod = ""
currentMethodType = 0
currentType = 0
currentDim = 0
currentVarId = "" # The last variable seen in the parsing process.
currentVarIdToAssign = "" # The last variable seen in the left side of an assignment in the parsing process.
currentVarIds = []
currentParamId = ""
currentParamIds = []
currentParamTypes = []
currentParamDimsX = []
currentParamDimsY = []
currentDimX = -1
currentDimY = -1
stackParamsToBeSend = Stack()
stackParamsTypesToBeSend = Stack()
stackParamsDimsX = Stack()
stackParamsDimsY = Stack()
stackFunctionCalls = Stack()
stackDimSizes = Stack()
currentCtType = ""
isCurrentVarPrivate = True
isCurrentVarIndependent = False
isCurrentMethodPrivate = False
isCurrentMethodIndependent = False
refersToClass = False
decisionsPerLevel = [0]
decisionLevel = 0
ctDic = {}

#TODO: Modify this function to accept dimX and dimY as well.
# Helper methods for checking semantics during parsing process.
def getNextAddress(type, scope, dimX, dimY):
	global gInt, gDouble, gChar, gBool, lInt, lDouble, lChar, lBool, tInt, tDouble, tChar, tBool, ctInt, ctDouble, ctChar, ctBool
	typeAsStr = invKeywordMapper.get(type)

	# Set the shift constant based on dimX and dimY.
	# The shift constant is how addresses we are going to skip for the next time we want to get an address
	# (This is necessary for reserving addresses for vectors and matrices).
	if dimX != -1:
		if dimY != -1:
			shiftConstant = dimX * dimY
		else:
			shiftConstant = dimX
	else:
		shiftConstant = 1

	if scope == 'global':
		if typeAsStr == 'int':
			newAddress = gInt
			gInt = gInt + shiftConstant
			return newAddress
		if typeAsStr == 'double':
			newAddress = gDouble
			gDouble = gDouble + shiftConstant
			return newAddress
		if typeAsStr == 'char':
			newAddress = gChar
			gChar = gChar + shiftConstant
			return newAddress
		if typeAsStr == 'bool':
			newAddress = gBool
			gBool = gBool + shiftConstant
			return newAddress
	elif scope == 'local':
		if typeAsStr == 'int':
			newAddress = lInt
			lInt = lInt + shiftConstant
			return newAddress
		if typeAsStr == 'double':
			newAddress = lDouble
			lDouble = lDouble + shiftConstant
			return newAddress
		if typeAsStr == 'char':
			newAddress = lChar
			lChar = lChar + shiftConstant
			return newAddress
		if typeAsStr == 'bool':
			newAddress = lBool
			lBool = lBool + shiftConstant
			return newAddress
	elif scope == 'temp':
		if typeAsStr == 'int':
			newAddress = tInt
			tInt = tInt + shiftConstant
			return newAddress
		if typeAsStr == 'double':
			newAddress = tDouble
			tDouble = tDouble + shiftConstant
			return newAddress
		if typeAsStr == 'char':
			newAddress = tChar
			tChar = tChar + shiftConstant
			return newAddress
		if typeAsStr == 'bool':
			newAddress = tBool
			tBool = tBool + shiftConstant
			return newAddress
	elif scope == 'const':
		if typeAsStr == 'int':
			newAddress = ctInt
			ctInt = ctInt + shiftConstant
			return newAddress
		if typeAsStr == 'double':
			newAddress = ctDouble
			ctDouble = ctDouble + shiftConstant
			return newAddress
		if typeAsStr == 'char':
			newAddress = ctChar
			ctChar = ctChar + shiftConstant
			return newAddress
		if typeAsStr == 'bool':
			newAddress = ctBool
			ctBool = ctBool + shiftConstant
			return newAddress

def resetLocalAndTempMemoryAddresses():
	global lInt, lDouble, lChar, lBool, tInt, tDouble, tChar, tBool
	lInt = CONST_L_BEGIN_INT
	lDouble = CONST_L_BEGIN_DOUBLE
	lChar = CONST_L_BEGIN_CHAR
	lBool = CONST_L_BEGIN_BOOL
	tInt = CONST_T_BEGIN_INT
	tDouble = CONST_T_BEGIN_DOUBLE
	tChar = CONST_T_BEGIN_CHAR
	tBool = CONST_T_BEGIN_BOOL

def validateAndAddVarsToScope(dimX, dimY):
	for currentVarId in currentVarIds:
		if currentMethod == "":
			varTable = funcDirTable.getVarTable(currentClass, None, None, None) 
			if varTable.has(currentVarId):
				print("Error: Variable '%s' was already defined." % (currentVarId))
				sys.exit(0)
			else:
				address = getNextAddress(currentType, "global", dimX, dimY)
				newVarTableRow = VarTableRow(currentType, isCurrentVarIndependent, isCurrentVarPrivate, address, dimX, dimY)
				varTable.add(currentVarId, newVarTableRow)
		else:
			varTable = funcDirTable.getVarTable(currentMethod, tuple(currentParamTypes), tuple(currentParamDimsX), tuple(currentParamDimsY))
			if varTable.has(currentVarId):
				print("Error: Variable '%s' was already defined." % (currentVarId))
				sys.exit(0)
			else:
				address = getNextAddress(currentType, "local", dimX, dimY)
				newVarTableRow = VarTableRow(currentType, None, None, address, dimX, dimY)
				varTable.add(currentVarId, newVarTableRow)

def checkIfVariableWasDefined(id):
	if refersToClass == True or currentMethod == "":
		varTable = funcDirTable.getVarTable(currentClass, None, None, None)
		if varTable.has(id) == False:
			print("Error: Variable '%s' was not declared." % (id))
			sys.exit(0)
	else:
		varTable = funcDirTable.getVarTable(currentMethod, tuple(currentParamTypes), tuple(currentParamDimsX), tuple(currentParamDimsY))
		if varTable.has(id) == False:
			varTable = funcDirTable.getVarTable(currentClass, None, None, None)
			if varTable.has(id) == False:
				print("Error: Variable '%s' was not declared." % (id))
				sys.exit(0)

def getVarAddress(id):
	if refersToClass == True or currentMethod == '':
		varTable = funcDirTable.getVarTable(currentClass, None, None, None)
		return varTable.get(id).address
	else:
		varTable = funcDirTable.getVarTable(currentMethod, tuple(currentParamTypes), tuple(currentParamDimsX), tuple(currentParamDimsY))
		if varTable.has(id):
			return varTable.get(id).address
		else:
			varTable = funcDirTable.getVarTable(currentClass, None, None, None)
			return varTable.get(id).address

def getVarType(id):
	if refersToClass == True or currentMethod == '':
		varTable = funcDirTable.getVarTable(currentClass, None, None, None)
		return varTable.get(id).varType
	else:
		varTable = funcDirTable.getVarTable(currentMethod, tuple(currentParamTypes), tuple(currentParamDimsX), tuple(currentParamDimsY))
		if varTable.has(id):
			return varTable.get(id).varType
		else:
			varTable = funcDirTable.getVarTable(currentClass, None, None, None)
			return varTable.get(id).varType

def getVarDims(id):
	if refersToClass == True or currentMethod == '':
		varTable = funcDirTable.getVarTable(currentClass, None, None, None)
		return (varTable.get(id).dimX, varTable.get(id).dimY)
	else:
		varTable = funcDirTable.getVarTable(currentMethod, tuple(currentParamTypes), tuple(currentParamDimsX), tuple(currentParamDimsY))
		if varTable.has(id):
			return (varTable.get(id).dimX, varTable.get(id).dimY)
		else:
			varTable = funcDirTable.getVarTable(currentClass, None, None, None)
			return (varTable.get(id).dimX, varTable.get(id).dimY)

def generateQuadForBinaryOperator(operatorList):
	operatorMatch = False
	topOp = codeToOper.get(quadManager.topOp())
	for op in operatorList:
		if topOp == op:
			operatorMatch = True
			break
	if operatorMatch:
		operType2 = quadManager.popType()
		operType1 = quadManager.popType()
		oper2 = quadManager.popOper()
		oper1 = quadManager.popOper()
		stackDimSizes.pop()
		stackDimSizes.pop()
		operator = quadManager.popOp()
		resType = semanticCube.checkType(operator, operType1, operType2)
		if invKeywordMapper.get(resType) == "error":
			print("Error: Binary '%s' does not support operands of type '%s', '%s'." % (codeToOper.get(operator), invKeywordMapper.get(operType1), invKeywordMapper.get(operType2)))
			sys.exit(0)
		resAddress = getNextAddress(resType, "temp", 1, 1)
		quadManager.addQuad(operator, oper1, oper2, resAddress)
		quadManager.pushOper(resAddress)
		quadManager.pushType(resType)
		stackDimSizes.push((-1, -1))

def generateQuadForUnaryOperator(operatorList):
	operatorMatch = False
	topOp = codeToOper.get(quadManager.topOp())
	for op in operatorList:
		if topOp == op:
			operatorMatch = True
			break
	if operatorMatch:
		operType = quadManager.popType()
		oper = quadManager.popOper()
		stackDimSizes.pop()
		operator = quadManager.popOp()
		resType = semanticCube.checkType(operator, -1, operType)
		if invKeywordMapper.get(resType) == "error":
			print("Error: Unary '%s' does not support operand of type '%s'." % (codeToOper.get(operator), invKeywordMapper.get(operType)))
			sys.exit(0)
		resAddress = getNextAddress(resType, "temp", 1, 1)
		quadManager.addQuad(operator, -1, oper, resAddress)
		quadManager.pushOper(resAddress)
		quadManager.pushType(resType)
		stackDimSizes.push((-1, -1))

#PROGRAM
def p_program(p):
	'''program	: np_program_0 program_class MAIN np_program_1 class_block np_program_2'''

def p_program_class(p):
	'''program_class	:	CLASS ID np_program_1 prog_inh class_block program_class
										| empty'''

def p_prog_inh(p):
	'''prog_inh	: INHERITS ID
							| empty'''

#NEURAL POINTS FOR PROGRAM_CLASS
def p_np_program_0(p):
	'''np_program_0	:'''
	quadManager.addQuad(operToCode.get("GOTO"), -1, -1, -1)

def p_np_program_1(p):
	'''np_program_1	:'''
	global currentClass, funcDirTable
	currentClass = p[-1]
	if currentClass in classDirTable:
		print("Error: Class '%s' redefined in line %d" % (currentClass, p.lexer.lineno))
		sys.exit(0)
	classDirTable[currentClass] = FuncDirTable()
	funcDirRow = FuncDirRow("class", False, False, quadManager.quadCont)
	classDirTable[currentClass].add(currentClass, None, None, None, funcDirRow)
	# Assigns the function directory of the current class to the global variable funcDirTable.
	funcDirTable = classDirTable[currentClass]

def p_np_program_2(p):
	'''np_program_2	:'''
	if not classDirTable[currentClass].has("main", (), (), ()):
		print("Error: Main block must have a 'main' function with no parameters.")
		sys.exit(0)

#VAR_DECL
def p_var_decl(p):
	'''var_decl	: vars
							| vector
							| matrix'''

#CLASS_BLOCK
def p_class_block(p):
	'''class_block	: '{' class_blck_body '}' '''

def p_class_blck_body(p):
	'''class_blck_body	: class_vars class_asgs class_func
											| class_func'''

def p_class_vars(p):
	'''class_vars	: access var_decl more_class_vars'''

def p_more_class_vars(p):
	'''more_class_vars	: class_vars
											| empty'''

def p_class_asgs(p):
	'''class_asgs	: assignment class_asgs
								| empty'''

def p_class_func(p):
	'''class_func	: method class_func
								| empty'''

#ACCESS
def p_access(p):
	'''access	: acc_scope np_access_1 acc_dependent'''

def p_acc_scope(p):
	'''acc_scope	: PUBLIC
								| PRIVATE'''
	p[0] = p[1]

def p_dependent(p):
	'''acc_dependent	: INDEPENDENT np_access_2
								| np_access_3'''

#NEURAL POINTS FOR ACCESS
def p_np_access_1(p):
	'''np_access_1	:'''
	global isCurrentVarPrivate, isCurrentVarIndependent
	if (p[-1] == "public"):
		isCurrentVarPrivate = False
	else:
		isCurrentVarPrivate = True

def p_np_access_2(p):
	'''np_access_2	:'''
	global isCurrentVarIndependent
	isCurrentVarIndependent = True

def p_np_access_3(p):
	'''np_access_3	:'''
	global isCurrentVarIndependent
	isCurrentVarIndependent = False

#METHOD_ACCESS
def p_method_access(p):
	'''method_access	: met_acc_scope np_method_access_1 met_acc_dependent'''

def p_met_acc_scope(p):
	'''met_acc_scope	: PUBLIC_FUNC
										| PRIVATE_FUNC'''
	p[0] = p[1]

def p_met_acc_dependent(p):
	'''met_acc_dependent	: INDEPENDENT np_method_access_2
												|	np_method_access_3'''

#NEURAL POINTS FOR METHOD_ACCESS
def p_np_method_access_1(p):
	'''np_method_access_1	:'''
	global isCurrentMethodPrivate, isCurrentMethodIndependent
	if p[-1] == "public_func":
		isCurrentMethodPrivate = False
	else:
		isCurrentMethodPrivate = True

def p_np_method_access_2(p):
	'''np_method_access_2	:'''
	global isCurrentMethodIndependent
	isCurrentMethodIndependent = True

def p_np_method_access_3(p):
	'''np_method_access_3	:'''
	global isCurrentMethodIndependent
	isCurrentMethodIndependent = False

#IDS
def p_ids(p):
	'''ids : ID np_ids_1 m_ids'''

def p_m_ids(p):
	'''m_ids	: ',' ids
						| empty'''

#NEURAL POINTS FOR IDS
def p_np_ids_1(p):
	'''np_ids_1	:'''
	global currentVarIds
	currentVarIds.append(p[-1])

#VARS
def p_vars(p):
	'''vars	: VAR ids ':' vars_type ';' np_vars_3'''

def p_vars_type(p):
	'''vars_type	: type np_vars_1 vars_tp_a
	        			| ID np_vars_2 vars_tp_b'''

def p_vars_tp_a(p):
	'''vars_tp_a	: '=' np_vars_4 expression np_vars_5
	   				    | empty'''

def p_vars_tp_b(p):
	'''vars_tp_b	: '=' vars_assgn
	   					  | empty'''

def p_vars_assgn(p):
	'''vars_assgn	: create_obj
	  				    | expression'''

#NEURAL POINTS FOR VARS
def p_np_vars_1(p):
	'''np_vars_1	:'''
	dimX = -1
	dimY = -1
	validateAndAddVarsToScope(dimX, dimY)

def p_np_vars_2(p):
	'''np_vars_2	:'''
	global currentType
	dimX = -1
	dimY = -1
	currentType = keywordMapper.get("object")
	validateAndAddVarsToScope(dimX, dimY)

def p_np_vars_3(p):
	'''np_vars_3	:'''
	global currentVarIds
	currentVarIds[:] = []

def p_np_vars_4(p):
	'''np_vars_4	:'''
	quadManager.pushOp(p[-1])

def p_np_vars_5(p):
	'''np_vars_5	:'''
	global refersToClass
	# refersToClass is set to false since all the variables declared do not use 'this'.
	# It is necessary to do this so that getVarAddress(id) works properly in this method.
	refersToClass = False
	currentOp = quadManager.popOp()
	expressionValue = quadManager.popOper()
	expressionType = quadManager.popType()
	stackDimSizes.pop()
	answerType = semanticCube.checkType(currentOp, currentType, expressionType)
	if invKeywordMapper.get(answerType) == "error":
		print("Error: Type mismatch in line %d" % (p.lexer.lineno))
		sys.exit(0)
	for id in currentVarIds:
		address = getVarAddress(id)
		quadManager.addQuad(currentOp, -1, expressionValue, address)

#VEC_MAT_TYPE
def p_vec_mat_type(p):
	'''vec_mat_type	: type
									| ID np_vec_mat_type_1'''

#NEURAL POINTS FOR VEC_MAT_TYPE
def p_np_vec_mat_type_1(p):
	'''np_vec_mat_type_1	:'''
	global currentType
	currentType = keywordMapper.get("object")

#VECTOR
def p_vector(p):
	'''vector	: VEC ids ':' vec_mat_type '[' CONST_I ']' np_vector_1 vec_assgn ';' np_vector_2'''

def p_vec_assgn(p):
	'''vec_assgn	: '=' vector_exp
								| empty'''

#NEURAL POINTS FOR VECTOR
def p_np_vector_1(p):
	'''np_vector_1	:'''
	dimX = int(p[-2])
	dimY = -1
	if dimX == 0:
		print("Error: Vectors at line %d must have a positive integer size." % (p.lexer.lineno))
		sys.exit(0)
	validateAndAddVarsToScope(dimX, dimY)

def p_np_vector_2(p):
	'''np_vector_2	:'''
	global currentVarIds
	currentVarIds[:] = []

#MATRIX
def p_matrix(p):
	'''matrix	: MAT ids ':' vec_mat_type '[' CONST_I ',' CONST_I ']' np_matrix_1 mat_assgn ';' np_matrix_2'''

def p_mat_assgn(p):
	'''mat_assgn	: '=' matrix_exp
								| empty'''

#NEURAL POINTS FOR MATRIX
def p_np_matrix_1(p):
	'''np_matrix_1	:'''
	dimX = int(p[-4])
	dimY = int(p[-2])
	if dimX == 0 or dimY == 0:
		print("Error: Matrices at line %d must have a positive integer size in each dimension." % (p.lexer.lineno))
		sys.exit(0)
	validateAndAddVarsToScope(dimX, dimY)

def p_np_matrix_2(p):
	'''np_matrix_2	:'''
	global currentVarIds
	currentVarIds[:] = []

#ID_ACCESS
def p_id_access(p):
	'''id_access	: id_mat_acc id_var_acc'''

def p_id_mat_acc(p):
	'''id_mat_acc	: mat_vec_access
								| empty'''

def p_id_var_acc(p):
	'''id_var_acc	: '.' np_id_access_1 ID id_mat_acc
								| empty'''

#NEURAL POINTS FOR ID_ACCESS
# TODO: Possibly refactor this into a method (it is very similar to checkIfVariableWasDefined)
def p_np_id_access_1(p):
	'''np_id_access_1	:'''
	if refersToClass == True or currentMethod == "":
		varTable = funcDirTable.getVarTable(currentClass, None, None, None)
		primType = varTable.get(currentVarId).varType
		if primType != keywordMapper.get("object"):
			print("Error: Cannot use the '.' operator with '%s', because it is not of object type" % (currentVarId))
			sys.exit(0)
	else:
		varTable = funcDirTable.getVarTable(currentMethod, tuple(currentParamTypes), tuple(currentParamDimsX), tuple(currentParamDimsY))
		primType = varTable.get(currentVarId).varType
		if primType != keywordMapper.get("object"):
			varTable = funcDirTable.getVarTable(currentClass, None, None, None)
			primType = varTable.get(currentVarId).varType
			if primType != keywordMapper.get("object"):
				print("Error: Cannot use the '.' operator with '%s', because it is not of object type" % (currentVarId))
				sys.exit(0)

#ASSIGNMENT
def p_assignment(p):
	'''assignment	: this ID np_assignment_1 id_access '=' np_assignment_2 ass_value ';' '''

def p_ass_value(p):
	'''ass_value	: create_obj
								| expression np_assignment_3
								| matrix_exp
	        			| vector_exp'''

#NEURAL POINTS FOR ASSIGNMENT
def p_np_assignment_1(p):
	'''np_assignment_1	:'''
	global currentVarId
	currentVarId = p[-1]
	checkIfVariableWasDefined(currentVarId)
	quadManager.pushOper(getVarAddress(currentVarId))
	quadManager.pushType(getVarType(currentVarId))
	stackDimSizes.push(getVarDims(currentVarId))

def p_np_assignment_2(p):
	'''np_assignment_2	:'''
	quadManager.pushOp(p[-1])

def p_np_assignment_3(p):
	'''np_assignment_3	:'''
	currentOp = quadManager.popOp()
	expressionValue = quadManager.popOper()
	expressionType = quadManager.popType()
	stackDimSizes.pop()
	assignedVar = quadManager.popOper()
	assignedVarType = quadManager.popType()
	stackDimSizes.pop()
	answerType = semanticCube.checkType(currentOp, assignedVarType, expressionType)
	if invKeywordMapper.get(answerType) == "error":
		print("Error: Type mismatch in line %d." % (p.lexer.lineno))
		sys.exit(0)
	quadManager.addQuad(currentOp, -1, expressionValue, assignedVar)

#THIS
def p_this(p):
	'''this	: THIS np_this_1 '.'
					| np_this_2'''

#NEURAL POINTS FOR THIS
def p_np_this_1(p):
	'''np_this_1	:'''
	global refersToClass
	refersToClass = True

def p_np_this_2(p):
	'''np_this_2	:'''
	global refersToClass	
	refersToClass = False

#VECTOR_EXP
def p_vector_exp(p):
	'''vector_exp	: '[' vec_elem ']' '''

def p_vec_elem(p):
	'''vec_elem	: vec_object vec_more'''

def p_vec_object(p):
	'''vec_object	: create_obj
	    					| expression'''

def p_vec_more(p):
	'''vec_more	: ',' vec_elem
	        		| empty'''

#MATRIX_EXP
def p_matrix_exp(p):
	'''matrix_exp	: '{' mat_elem '}' '''

def p_mat_elem(p):
	'''mat_elem	: vector_exp mat_more'''

def p_mat_more(p):
	'''mat_more	: ',' mat_elem
							| empty'''

#MAT_VEC_ACCESS
def p_mat_vec_access(p):
	'''mat_vec_access	: '[' np_mat_vec_access_1 mat_vec_index mat_access np_mat_vec_access_4 ']' '''

def p_mat_vec_index(p):
	'''mat_vec_index	: '_'
										| expression np_mat_vec_access_2'''

def p_mat_access(p):
	'''mat_access	: ',' np_mat_vec_access_3 mat_vec_index
								| empty'''

#NEURAL POINTS FOR MAT_VEC_ACCESS
def p_np_mat_vec_access_1(p):
	'''np_mat_vec_access_1	:'''
	# At this point, the top of the stackDimSizes contains the dims of the current vector/matrix being accessed.
	id = quadManager.popOper()
	dimX, dimY = stackDimSizes.top()

	if dimX == -1:
		print("Error: '%s' at line %d is not a variable of the proper dimension." % (currentVarId, p.lexer.lineno))
		sys.exit(0)
	
	quadManager.pushDim(id, 1) # We are in the first dimension of the variable 'id'.
	quadManager.pushOp(operToCode.get("(")) # Push a false bottom operator.

def p_np_mat_vec_access_2(p):
	'''np_mat_vec_access_2	:'''
	id, dim = quadManager.topDim()
	stackDimSizes.pop() # Eliminate the top element in the stack, which is the dims of the last expression.
	dims = stackDimSizes.top()

	quadManager.addQuad(operToCode.get("VER"), quadManager.topOper(), -1, dims[dim - 1])
	# If the current dim is not the last one...
	if dim < len(dims) and dims[dim] != -1:
		aux = quadManager.popOper()
		dimX = dims[0]
		tempAddress = getNextAddress(keywordMapper.get("int"), "temp", 1, 1)
		
		# If dimX is not in the directory of constants...
		if dimX not in ctDic:
			# Assign dimX to an address in the scope of constants.
			constDimAddress = getNextAddress(keywordMapper.get("int"), "const", 1, 1)
			quadManager.addQuad(operToCode.get("="), -1, dimX, constDimAddress)
			ctDic[dimX] = constDimAddress
		else:
			constDimAddress = ctDic.get(dimX)
			quadManager.addQuad(operToCode.get("="), -1, dimX, constDimAddress)
		
		quadManager.addQuad(operToCode.get("*"), aux, constDimAddress, tempAddress)
		quadManager.pushOper(tempAddress)

	if dim > 1:
		aux2 = quadManager.popOper()
		aux = quadManager.popOper()
		tempAddress = getNextAddress(keywordMapper.get("int"), "temp", 1, 1)
		quadManager.addQuad(operToCode.get("+"), aux, aux2, tempAddress)
		quadManager.pushOper(tempAddress)

def p_np_mat_vec_access_3(p):
	'''np_mat_vec_access_3	:'''
	# At this point, the top of the stackDimSizes contains the dims of the current vector/matrix being accessed.
	id, dim = quadManager.popDim()
	dimX, dimY = stackDimSizes.top()
	if dimY == -1:
		# TODO: Update error message to use a variable id instead of address. Note that we cannot use currentVarId. 
		print("Error: '%s' at line %d is not a variable of the proper dimension." % (id, p.lexer.lineno))
		sys.exit(0)
	
	# Adds 1 to the dimension that was at the top of the stack of dimensions.
	quadManager.pushDim(id, dim + 1)

def p_np_mat_vec_access_4(p):
	'''np_mat_vec_access_4	:'''
	# At this point, the top of the stackDimSizes contains the dims of the current vector/matrix being accessed.
	aux = quadManager.popOper()
	idBase, dim = quadManager.topDim()
	dimX, dimY = stackDimSizes.top()
	if dim == 1 and dimY != -1:
		# TODO: Update error message to use a variable id instead of address. Note that we cannot use currentVarId. 
		print("Error: '%s' at line %d is not a variable of the proper dimension." % (idBase, p.lexer.lineno))
		sys.exit(0)

	# Stores the base id of the vector/matrix in a constant address, so that we can add it
	# to the shifting value accummulated so far. This is necessary since the "+" operation adds
	# the values stored in the addresses, not the addresses themselves.
	if idBase in ctDic:
		constantAddressForBase = ctDic[idBase]
	else:
		constantAddressForBase = getNextAddress(keywordMapper.get("int"), "const", 1, 1)
	
	quadManager.addQuad(operToCode.get("="), -1, idBase, constantAddressForBase)

	indexingAddress = getNextAddress(keywordMapper.get("int"), "temp", 1, 1)
	# Specifies that 'indexingAddress' in this moment is not a reference to another address. This had to be done
	# in order for the "REF" operator to work when accessing elements in a vector or matrix within a loop.
	quadManager.addQuad(operToCode.get("DEREF"), -1 , -1, indexingAddress)
	quadManager.addQuad(operToCode.get("+"), aux, constantAddressForBase, indexingAddress)
	# Specifies that 'indexingAddress' does not contain a value, but instead is a reference to another address.
	quadManager.addQuad(operToCode.get("REF"), -1, -1, indexingAddress)
	quadManager.pushOper(indexingAddress)
	quadManager.popOp() # Removes false bottom operator.
	quadManager.popDim()
	stackDimSizes.pop()
	stackDimSizes.push((-1, -1)) # Size dimensions of the new added operand (indexingAddress) to the stack of operands.

#METHOD
def p_method(p):
	'''method	: func_spec '(' np_method_5 opt_method_param ')' np_method_6 block np_method_7'''

def p_func_spec(p):
	'''func_spec	: method_access func_type ID np_method_4
								| CONSTRUCTOR np_method_1'''

def p_func_type(p):
	'''func_type	: VOID np_method_2
								| type
								| ID np_method_3'''

#NEURAL POINTS FOR METHOD
def p_np_method_1(p):
	'''np_method_1	:'''
	global isCurrentMethodPrivate, isCurrentMethodIndependent, currentMethod, currentType, currentMethodType
	isCurrentMethodPrivate = False
	isCurrentMethodIndependent = False
	currentMethod = "constructor"
	currentType = None
	currentMethodType = currentType

def p_np_method_2(p):
	'''np_method_2	:'''
	global currentType
	currentType = keywordMapper.get(p[-1])

def p_np_method_3(p):
	'''np_method_3	:'''
	global currentType
	currentType = keywordMapper.get("object")

def p_np_method_4(p):
	'''np_method_4	:'''
	global currentMethod, currentMethodType
	currentMethod = p[-1]
	if currentClass == "Main" and currentMethod == "main":
		quadManager.fill(0, quadManager.quadCont)
	currentMethodType = currentType

def p_np_method_5(p):
	'''np_method_5	:'''
	global currentParamIds, currentParamTypes, currentParamDimsX, currentParamDimsY
	currentParamIds[:] = []
	currentParamTypes[:] = []
	currentParamDimsX[:] = []
	currentParamDimsY[:] = []

def p_np_method_6(p):
	'''np_method_6	:'''
	global funcDirTable, varTable
	if funcDirTable.has(currentMethod, tuple(currentParamTypes), tuple(currentParamDimsX), tuple(currentParamDimsY)) == True:
		print("Error: Method '%s' at line %d was already defined with the same parameters." % (currentMethod, p.lexer.lineno))
		sys.exit(0)
	else:
		newFuncDirRow = FuncDirRow(currentMethodType, isCurrentMethodIndependent, isCurrentMethodPrivate, quadManager.quadCont)
		funcDirTable.add(currentMethod, tuple(currentParamTypes), tuple(currentParamDimsX), tuple(currentParamDimsY), newFuncDirRow)
		# Get the VarTable of the 'just created' function.
		varTable = funcDirTable.getVarTable(currentMethod, tuple(currentParamTypes), tuple(currentParamDimsX), tuple(currentParamDimsY))
		for index in range(len(currentParamIds)):
			if varTable.has(currentParamIds[index]):
				print("Error: Parameter '%s' was already defined for '%s' method" % (currentParamIds[index], currentMethod))
				sys.exit(0)
			else:
				address = getNextAddress(currentParamTypes[index], "local", currentParamDimsX[index], currentParamDimsY[index])
				newVarTableRow = VarTableRow(currentParamTypes[index], None, None, address, currentParamDimsX[index], currentParamDimsY[index])
				varTable.add(currentParamIds[index], newVarTableRow)
				# TODO: Check if operator has to be "LOAD_REF" or "LOAD_PARAM"
				quadManager.addQuad(operToCode.get("LOAD_PARAM"), -1, -1, address)

def p_np_method_7(p):
	'''np_method_7	:'''
	resetLocalAndTempMemoryAddresses()
	# TODO: Check if in Python is necessary to release current VarTable.
	quadManager.addQuad(operToCode.get("ENDPROC"), -1, -1, -1)

#METHOD_PARAM
def p_opt_method_param(p):
	'''opt_method_param : method_param
											| empty'''

def p_method_param(p):
	'''method_param	: ID np_method_param_1 ':' param_type param_mat_vec np_method_param_6 more_params'''

def p_more_params(p):
	'''more_params	: ',' method_param
									| empty'''

def p_param_type(p):
	'''param_type	: type
								| ID np_method_param_2'''

def p_param_mat_vec(p):
	'''param_mat_vec	: '[' param_mat ']'
										| np_method_param_3'''

def p_param_mat(p):
	'''param_mat	: CONST_I ',' CONST_I np_method_param_5
								| CONST_I np_method_param_4'''

#NEURAL POINTS FOR METHOD_PARAM
def p_np_method_param_1(p):
	'''np_method_param_1	:'''
	global currentParamId
	currentParamId = p[-1]

def p_np_method_param_2(p):
	'''np_method_param_2	:'''
	global currentType
	currentType = keywordMapper.get("object")

def p_np_method_param_3(p):
	'''np_method_param_3	:'''
	global currentDimX, currentDimY
	currentDimX = -1
	currentDimY = -1

def p_np_method_param_4(p):
	'''np_method_param_4	:'''
	global currentDimX, currentDimY
	currentDimX = int(p[-1])
	currentDimY = -1

def p_np_method_param_5(p):
	'''np_method_param_5	:'''
	global currentDimX, currentDimY
	currentDimX = int(p[-3])
	currentDimY = int(p[-1])

def p_np_method_param_6(p):
	'''np_method_param_6	:'''
	global currentParamIds, currentParamTypes, currentParamDimsX, currentParamDimsY
	currentParamIds.append(currentParamId)
	currentParamTypes.append(currentType)
	currentParamDimsX.append(currentDimX)
	currentParamDimsY.append(currentDimY)

#CREATE_OBJ
def p_create_obj(p):
	'''create_obj	: NEW func_call'''

#FUNC_CALL
def p_func_call(p):
	'''func_call	: np_func_call_1 '(' func_param np_func_call_3 ')' np_func_call_4'''

def p_func_param(p):
	'''func_param	: expression np_func_call_2 more_fpar
								| empty'''

def p_more_fpar(p):
	'''more_fpar	: ',' func_param
								| empty'''

#NEURAL POINTS FOR FUNC_CALL
def p_np_func_call_1(p):
	'''np_func_call_1	:'''
	global stackParamsToBeSend, stackParamsTypesToBeSend
	quadManager.addQuad(operToCode.get("ERA"), -1, -1, -1)
	stackParamsToBeSend.push([])
	stackParamsTypesToBeSend.push([])
	stackParamsDimsX.push([])
	stackParamsDimsY.push([])
	quadManager.pushOp(operToCode.get("("))

def p_np_func_call_2(p):
	'''np_func_call_2	:'''
	global stackParamsToBeSend, stackParamsTypesToBeSend
	param = quadManager.popOper()
	paramType = quadManager.popType()
	dimX, dimY = stackDimSizes.pop()
	currentParamsToBeSend = stackParamsToBeSend.top()
	currentParamsToBeSend.append(param)
	currentParamsTypesToBeSend = stackParamsTypesToBeSend.top()
	currentParamsTypesToBeSend.append(paramType)
	localParamDimsX = stackParamsDimsX.top()
	localParamDimsX.append(dimX)
	localParamDimsY = stackParamsDimsY.top()
	localParamDimsY.append(dimY)

def p_np_func_call_3(p):
	'''np_func_call_3	:'''
	funcName = stackFunctionCalls.pop()
	currentParamsToBeSend = stackParamsToBeSend.top()
	currentParamsTypesToBeSend = stackParamsTypesToBeSend.top()
	localParamDimsX = stackParamsDimsX.top()
	localParamDimsY = stackParamsDimsY.top()
	print(localParamDimsX, localParamDimsY)
	if funcDirTable.has(funcName, tuple(currentParamsTypesToBeSend), tuple(localParamDimsX), tuple(localParamDimsY)):
		funcDirRow = funcDirTable.getFuncDirRow(funcName, tuple(currentParamsTypesToBeSend), tuple(localParamDimsX), tuple(localParamDimsY))
		funcStartPos = funcDirRow.startPos
		funcType = funcDirRow.blockType
		for param in currentParamsToBeSend:
			# TODO: Validate whether param should be send by reference or by value.
			quadManager.addQuad(operToCode.get("PARAM"), -1, -1, param)
		quadManager.addQuad(operToCode.get("GOSUB"), -1, -1, funcStartPos)
		# TODO: Add error message for checking if you called a void function in an expression.
		if funcType != keywordMapper.get("void"):
			returnAddress = getNextAddress(funcType, "temp", 1, 1)
			quadManager.addQuad(operToCode.get("="), -1, CONST_RETURN, returnAddress)
			quadManager.pushOper(returnAddress)
			quadManager.pushType(funcType)
			stackDimSizes.push((-1, -1))
	else:
		print("Error: Function '%s' with the arguments used in line %d was not defined." % (funcName, p.lexer.lineno))
		sys.exit(0)

def p_np_func_call_4(p):
	'''np_func_call_4	:'''
	# Remove the "false bottom" in the stack of operators.
	quadManager.popOp()
	stackParamsToBeSend.pop()
	stackParamsTypesToBeSend.pop()
	stackParamsDimsX.pop()
	stackParamsDimsY.pop()

#BLOCK
def p_block(p):
	'''block	: '{' bstmt '}' '''

def p_bstmt(p):
	'''bstmt	: statement bstmt
						| empty'''

#STATEMENT
#TODO: Fix the part refererring to calling a function
def p_statement(p):
	'''statement	: assignment
								| condition
								| loop
								| in_out
								| return
								| this ID np_statement_1 func_call ';'
								| var_decl'''

#NEURAL POINTS FOR STATEMENT
def p_np_statement_1(p):
	'''np_statement_1	:'''
	global stackFunctionCalls
	stackFunctionCalls.push(p[-1])

#CONDITION
def p_condition(p):
	'''condition	: IF cond_body np_condition_4'''

def p_cond_body(p):
	'''cond_body	: '(' expression ')' np_condition_1 block cond_else'''

def p_cond_else(p):
	'''cond_else	: np_condition_2 ELSE block
								| np_condition_2 ELSEIF cond_body
								| np_condition_3'''

#NEURAL POINTS FOR CONDITION
def p_np_condition_1(p):
	'''np_condition_1	:'''
	global decisionLevel, decisionsPerLevel
	expressionType = quadManager.popType()
	expressionValue = quadManager.popOper()
	stackDimSizes.pop()
	if invKeywordMapper.get(expressionType) != "bool":
		print("Error: Expected boolean expression after 'if'/'elseif' in line %d" % (p.lexer.lineno))
		sys.exit(0)
	quadManager.addQuad(operToCode.get("GOTOF"), expressionValue, -1, -1)
	quadManager.pushJump(quadManager.quadCont - 1)
	decisionsPerLevel[decisionLevel] = decisionsPerLevel[decisionLevel] + 1
	decisionLevel = decisionLevel + 1
	if len(decisionsPerLevel) == decisionLevel:
		decisionsPerLevel.append(0)
	else:
		decisionsPerLevel[decisionLevel] = 0

def p_np_condition_2(p):
	'''np_condition_2	:'''
	global decisionLevel
	decisionLevel = decisionLevel - 1
	quadManager.addQuad(operToCode.get("GOTO"), -1, -1, -1)
	falseInCond = quadManager.popJump()
	quadManager.fill(falseInCond, quadManager.quadCont)
	quadManager.pushJump(quadManager.quadCont - 1)

def p_np_condition_3(p):
	'''np_condition_3	:'''
	global decisionLevel
	decisionLevel = decisionLevel - 1

def p_np_condition_4(p):
	'''np_condition_4	:'''
	global decisionLevel, decisionsPerLevel
	for _ in range(0, decisionsPerLevel[decisionLevel]):
		endOfDecision = quadManager.popJump()
		quadManager.fill(endOfDecision, quadManager.quadCont)

#LOOP
def p_loop(p):
	'''loop	: for_loop
					| while_loop'''

#FOR_LOOP
def p_for_loop(p):
	'''for_loop	: FOR '(' assignment np_for_loop_1 expression np_for_loop_2 ';' ID '=' expression np_for_loop_3 ')' block np_for_loop_4'''

#NEURAL POINTS FOR FOR_LOOP
def p_np_for_loop_1(p):
	'''np_for_loop_1	:'''
	quadManager.pushJump(quadManager.quadCont) # condition begin

def p_np_for_loop_2(p):
	'''np_for_loop_2	:'''
	expressionType = quadManager.popType()
	expressionValue = quadManager.popOper()
	stackDimSizes.pop()
	if invKeywordMapper.get(expressionType) != 'bool':
		print("Error: Expected boolean expression in second block of 'for' statement in line %d" % (p.lexer.lineno))
		sys.exit(0)
	quadManager.addQuad(operToCode.get("GOTOF"), expressionValue, -1, -1)
	quadManager.pushJump(quadManager.quadCont - 1) # quad that jumps to the end of the loop
	quadManager.addQuad(operToCode.get("GOTO"), -1, -1, -1) 
	quadManager.pushJump(quadManager.quadCont - 1) # quad that goes to the beginning of the block
	quadManager.pushJump(quadManager.quadCont) # quad that starts update of iteration var

def p_np_for_loop_3(p):
	'''np_for_loop_3	:'''
	modificationBegin = quadManager.popJump()
	conditionEnd = quadManager.popJump()
	falseCondition = quadManager.popJump()
	conditionBegin = quadManager.popJump()
	expressionAns = quadManager.popOper()
	expressionType = quadManager.popType()
	stackDimSizes.pop()
	forVarId = p[-3] # p[-3] is ID of variable to be assigned to.
	forVarIdAddress = getVarAddress(forVarId)
	forVarIdTypePrimType = getVarType(p[-3])
	if semanticCube.checkType(operToCode.get("="), expressionType, forVarIdTypePrimType) == keywordMapper.get("error"):
		print("Error: Type mismatch in line %d" % (p.lexer.lineno))
		sys.exit(0)
	quadManager.addQuad(operToCode.get("="), -1, expressionAns, forVarIdAddress) 
	quadManager.addQuad(operToCode.get("GOTO"), -1, -1, conditionBegin)
	quadManager.fill(conditionEnd, quadManager.quadCont)
	quadManager.pushJump(falseCondition)
	quadManager.pushJump(modificationBegin)

def p_np_for_loop_4(p):
	'''np_for_loop_4	:'''
	modificationBegin = quadManager.popJump()
	quadManager.addQuad(operToCode.get("GOTO"), -1, -1, modificationBegin)
	falseCondition = quadManager.popJump()
	quadManager.fill(falseCondition, quadManager.quadCont)

#WHILE_LOOP
def p_while_loop(p):
	'''while_loop	: WHILE np_while_loop_1 '(' expression ')' np_while_loop_2 block np_while_loop_3'''

#NEURAL POINTS FOR WHILE_LOOP
def p_np_while_loop_1(p):
	'''np_while_loop_1	:'''
	quadManager.pushJump(quadManager.quadCont)

def p_np_while_loop_2(p):
	'''np_while_loop_2	:'''
	expressionType = quadManager.popType()
	expressionValue = quadManager.popOper()
	stackDimSizes.pop()
	if invKeywordMapper.get(expressionType) != "bool":
		print("Error: Expected boolean expression after 'while' in line %d" % (p.lexer.lineno))
		sys.exit(0)
	quadManager.addQuad(operToCode.get("GOTOF"), expressionValue, -1, -1)
	quadManager.pushJump(quadManager.quadCont - 1)

def p_np_while_loop_3(p):
	'''np_while_loop_3	:'''
	endLoop = quadManager.popJump()
	returnToBeginLoop = quadManager.popJump()
	quadManager.addQuad(operToCode.get("GOTO"), -1, -1, returnToBeginLoop)
	quadManager.fill(endLoop, quadManager.quadCont)

#IN_OUT
def p_in_out(p):
	'''in_out	: PRINT '(' print_exp np_in_out_3 ')' ';'
						| SCAN '(' ID np_in_out_2 id_access ')' ';' '''

def p_print_exp(p):
	'''print_exp	: expression np_in_out_1 print_more'''

def p_print_more(p):
	'''print_more	: ',' print_exp
								| empty'''

#NEURAL POINTS FOR IN_OUT
def p_np_in_out_1(p):
	'''np_in_out_1	:'''
	expAddress = quadManager.popOper()
	expType = quadManager.popType()
	stackDimSizes.pop()
	operator = operToCode.get('print')
	quadManager.addQuad(operator, -1, -1, expAddress)

def p_np_in_out_2(p):
	'''np_in_out_2	:'''
	global currentVarId
	currentVarId = p[-1]
	idAddress = getVarAddress(currentVarId)
	operator = operToCode.get('scan')
	# TODO: Modify scan for vector/matrix expressions.
	quadManager.addQuad(operator, 0, -1, idAddress)

def p_np_in_out_3(p):
	'''np_in_out_3	:'''
	operator = operToCode.get('print')
	quadManager.addQuad(operator, -1, -1, -1)

#RETURN
def p_return(p):
	'''return	: RETURN ret_val ';' '''

def p_ret_val(p):
	'''ret_val	: expression np_return_1
							| np_return_2'''

#NEURAL POINTS FOR RETURN
def p_np_return_1(p):
	'''np_return_1	:'''
	returnValue = quadManager.popOper()
	returnType = quadManager.popType()
	stackDimSizes.pop()
	if returnType != currentMethodType:
		print("Error: Return value in line %d is not of type '%s'." % (p.lexer.lineno, invKeywordMapper.get(currentMethodType)))
		sys.exit(0)
	else:
		quadManager.addQuad(operToCode.get("RETURN"), returnValue, -1, CONST_RETURN)

def p_np_return_2(p):
	'''np_return_2	:'''
	if currentMethodType != keywordMapper.get("void"):
		print("Error: Must return a value of type '%s' in line %d." % (invKeywordMapper.get(currentMethodType), p.lexer.lineno))
		sys.exit(0)
	else:
		quadManager.addQuad(operToCode.get("RETURN"), -1, -1, -1)

#EXPRESSION
def p_expression(p):
	'''expression	: rel_expression np_expression_1 expression_op'''

def p_expression_op(p):
	'''expression_op	: AND np_expression_2 expression
										| OR np_expression_2 expression
										| XOR np_expression_2 expression
										| empty'''

#NEURAL POINTS FOR EXPRESSION
def p_np_expression_1(p):
	'''np_expression_1	:'''
	operatorList = ["and", "or", "xor"]
	generateQuadForBinaryOperator(operatorList)

def p_np_expression_2(p):
	'''np_expression_2	:'''
	quadManager.pushOp(p[-1])

#REL_EXPRESSION
def p_rel_expression(p):
	'''rel_expression	: rel_expression_1 np_rel_expression_1 rel_exp_op'''

def p_rel_exp_op(p):
	'''rel_exp_op	: EQUAL np_rel_expression_2 rel_expression
								| NOT_EQUAL np_rel_expression_2 rel_expression
								| empty'''

#NEURAL POINTS FOR REL_EXPRESSION
def p_np_rel_expression_1(p):
	'''np_rel_expression_1	:'''
	operatorList = ["==", "<>"]
	generateQuadForBinaryOperator(operatorList)

def p_np_rel_expression_2(p):
	'''np_rel_expression_2	:'''
	quadManager.pushOp(p[-1])

#REL_EXPRESSION_1
def p_rel_expression_1(p):
	'''rel_expression_1	: exp np_rel_expression_1_1 rel_exp_1_op'''

def p_rel_exp_1_op(p):
	'''rel_exp_1_op	: '<' np_rel_expression_1_2 rel_expression_1
									| LESS_EQUAL_THAN np_rel_expression_1_2 rel_expression_1
									| '>' np_rel_expression_1_2 rel_expression_1
									| GREATER_EQUAL_THAN np_rel_expression_1_2 rel_expression_1
									| empty'''

#NEURAL POINTS FOR REL_EXPRESSION_1
def p_np_rel_expression_1_1(p):
	'''np_rel_expression_1_1	:'''
	operatorList = ["<", "<=", ">", ">="]
	generateQuadForBinaryOperator(operatorList)

def p_np_rel_expression_1_2(p):
	'''np_rel_expression_1_2	:'''
	quadManager.pushOp(p[-1])

#EXP
def p_exp(p):
	'''exp	: term np_exp_1 exp_op'''

def p_exp_op(p):
	'''exp_op	: '+' np_exp_2 exp
						| '-' np_exp_2 exp
						| empty'''

#NEURAL POINTS FOR EXP
def p_np_exp_1(p):
	'''np_exp_1	:'''
	operatorList = ["+", "-"]
	generateQuadForBinaryOperator(operatorList)

def p_np_exp_2(p):
	'''np_exp_2	:'''
	quadManager.pushOp(p[-1])

#TERM
def p_term(p):
	'''term	: factor np_term_1 term_op'''

def p_term_op(p):
	'''term_op	: '*' np_term_2 term
							| '/' np_term_2 term
							| '%' np_term_2 term
							| empty'''

#NEURAL POINTS FOR TERM
def p_np_term_1(p):
	'''np_term_1	:'''
	operatorList = ["*", "/", "%"]
	generateQuadForBinaryOperator(operatorList)

def p_np_term_2(p):
	'''np_term_2	:'''
	quadManager.pushOp(p[-1])

#TYPE
def p_type(p):
	'''type	: INT np_type_1
					| DOUBLE np_type_1
					| CHAR np_type_1
					| BOOL np_type_1'''

#NEURAL POINTS FOR TYPE
def p_np_type_1(p):
	'''np_type_1	:'''
	global currentType
	currentType = keywordMapper.get(p[-1])

#VAR_CTE
def p_var_cte(p):
	'''var_cte	: CONST_I np_var_cte_1
							| CONST_F np_var_cte_2
							| CONST_CHAR np_var_cte_3
							| CONST_STRING np_var_cte_4
							| CONST_BOOL np_var_cte_5'''
	p[0] = p[1]

#NEURAL POINTS FOR VAR_CTE
def p_np_var_cte_1(p):
	'''np_var_cte_1	:'''
	global currentCtType
	currentCtType = 'int'

def p_np_var_cte_2(p):
	'''np_var_cte_2	:'''
	global currentCtType
	currentCtType = 'double'

def p_np_var_cte_3(p):
	'''np_var_cte_3	:'''
	global currentCtType
	currentCtType = 'char'

def p_np_var_cte_4(p):
	'''np_var_cte_4	:'''
	global currentCtType
	currentCtType = 'char'

def p_np_var_cte_5(p):
	'''np_var_cte_5	:'''
	global currentCtType
	currentCtType = 'bool'

#FACTOR
def p_factor(p):
	'''factor	: fact_neg fact_body np_factor_7'''

def p_fact_neg(p):
	'''fact_neg	: '-' np_factor_2
							| '~' np_factor_3
							| empty'''

def p_fact_body(p):
	'''fact_body	: '(' np_factor_4 expression ')' np_factor_5
								| var_cte np_factor_6
								| this ID np_factor_1 fact_id'''

def p_fact_id(p):
	'''fact_id	: np_factor_9 func_call
							| np_factor_8 id_access'''

#NEURAL POINTS FOR FACTOR
def p_np_factor_1(p):
	'''np_factor_1	:'''
	global currentVarId
	currentVarId = p[-1]

def p_np_factor_2(p):
	'''np_factor_2	:'''
	quadManager.pushOp('UMINUS')

def p_np_factor_3(p):
	'''np_factor_3	:'''
	quadManager.pushOp(p[-1])

def p_np_factor_4(p):
	'''np_factor_4	:'''
	quadManager.pushOp(p[-1])

def p_np_factor_5(p):
	'''np_factor_5	:'''
	quadManager.popOp()

def p_np_factor_6(p):
	'''np_factor_6	:'''
	ctValue = p[-1]
	ctTypeCode = keywordMapper.get(currentCtType)
	if ctValue in ctDic:
		ctAddress = ctDic[ctValue]
	else:
		ctAddress = getNextAddress(ctTypeCode, 'const', 1, 1)
		ctDic[ctValue] = ctAddress
	# When reading quads in VM, if the operator is '=' and oper3 has const scope, then
	# oper2 is a constant value (not an address) and must be treated as such.
	operator = operToCode.get('=')
	quadManager.addQuad(operator, -1, ctValue, ctAddress)
	quadManager.pushOper(ctAddress)
	quadManager.pushType(ctTypeCode)
	stackDimSizes.push((-1, -1))

def p_np_factor_7(p):
	'''np_factor_7	:'''
	operatorList = ["UMINUS", "~"]
	generateQuadForUnaryOperator(operatorList)

def p_np_factor_8(p):
	'''np_factor_8	:'''
	checkIfVariableWasDefined(currentVarId)
	quadManager.pushOper(getVarAddress(currentVarId))
	primType = getVarType(currentVarId)
	quadManager.pushType(primType)
	stackDimSizes.push(getVarDims(currentVarId))

def p_np_factor_9(p):
	'''np_factor_9	:'''
	global stackFunctionCalls
	stackFunctionCalls.push(p[-2])

#ERROR
def p_error(p):
	if p:
		print("Line #%d: Syntax error at token %s" % (p.lexer.lineno, p.type))
		sys.exit(0)
	else:
		print("Syntax error at EOF!")
		sys.exit(0)

#EMPTY
def p_empty(p):
	'''empty	: '''
	pass

# Creating and running the parser with a file provided by the user.
parser = yacc.yacc()
fileName = input("File to analyze: ")
try:
	file = open(fileName, 'r')
	parser.parse(file.read())
	quadManager.printToFile("quadruples.o")
	print("Syntax analysis finished.")
except OSError:
	print("The file '%s' does not exist or could not be opened." % (fileName))