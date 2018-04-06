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
from quadrupleManager import operatorMapper
from quadrupleManager import invOperatorMapper

# Constants for initializing memory addresses for local variables.
CONST_L_BEGIN_INT = 10000
CONST_L_BEGIN_DOUBLE = 11000
CONST_L_BEGIN_CHAR = 12000
CONST_L_BEGIN_BOOL = 13000

# Initialization of global counters
gInt = 0
gDouble = 1000
gChar = 2000
gBool = 3000
lInt = CONST_L_BEGIN_INT
lDouble = CONST_L_BEGIN_DOUBLE
lChar = CONST_L_BEGIN_CHAR
lBool = CONST_L_BEGIN_BOOL
tInt = 20000
tDouble = 21000
tChar = 22000
tBool = 23000
ctInt = 30000
ctDouble = 31000
ctChar = 32000
ctBool = 33000

# Initialize global variables with default values
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
currentCtType = ""
isCurrentVarPrivate = True
isCurrentVarIndependent = False
isCurrentMethodPrivate = False
isCurrentMethodIndependent = False
refersToClass = False
decisionsPerLevel = [0]
decisionLevel = 0

# Helper methods for checking semantics during parsing process.
def getNextAddress(type, scope):
	global gInt, gDouble, gChar, gBool, lInt, lDouble, lChar, lBool, tInt, tDouble, tChar, tBool
	typeAsStr = invKeywordMapper.get(type)
	if scope == 'global':
		if typeAsStr == 'int':
			newAddress = gInt
			gInt = gInt + 1
			return newAddress
		if typeAsStr == 'double':
			newAddress = gDouble
			gDouble = gDouble + 1
			return newAddress
		if typeAsStr == 'char':
			newAddress = gChar
			gChar = gChar + 1
			return newAddress
		if typeAsStr == 'bool':
			newAddress = gBool
			gBool = gBool + 1
			return newAddress
	elif scope == 'local':
		if typeAsStr == 'int':
			newAddress = lInt
			lInt = lInt + 1
			return newAddress
		if typeAsStr == 'double':
			newAddress = lDouble
			lDouble = lDouble + 1
			return newAddress
		if typeAsStr == 'char':
			newAddress = lChar
			lChar = lChar + 1
			return newAddress
		if typeAsStr == 'bool':
			newAddress = lBool
			lBool = lBool + 1
			return newAddress
	elif scope == 'temp':
		if typeAsStr == 'int':
			newAddress = tInt
			tInt = tInt + 1
			return newAddress
		if typeAsStr == 'double':
			newAddress = tDouble
			tDouble = tDouble + 1
			return newAddress
		if typeAsStr == 'char':
			newAddress = tChar
			tChar = tChar + 1
			return newAddress
		if typeAsStr == 'bool':
			newAddress = tBool
			tBool = tBool + 1
			return newAddress

def resetLocalMemoryAddresses():
	global lInt, lDouble, lChar, lBool
	lInt = CONST_L_BEGIN_INT
	lDouble = CONST_L_BEGIN_DOUBLE
	lChar = CONST_L_BEGIN_CHAR
	lBool = CONST_L_BEGIN_BOOL

def validateAndAddVarsToScope(dim):
	for currentVarId in currentVarIds:
		if currentMethod == "":
			varTable = funcDirTable.getVarTable(currentClass, None) 
			if varTable.has(currentVarId):
				print("Error: Variable '%s' was already defined." % (currentVarId))
				sys.exit(0)
			else:
				address = getNextAddress(currentType, "global")
				newVarTableRow = VarTableRow((dim, currentType), isCurrentVarIndependent, isCurrentVarPrivate, address)
				varTable.add(currentVarId, newVarTableRow)
		else:
			varTable = funcDirTable.getVarTable(currentMethod, tuple(currentParamTypes))
			if varTable.has(currentVarId):
				print("Error: Variable '%s' was already defined." % (currentVarId))
				sys.exit(0)
			else:
				address = getNextAddress(currentType, "local")
				newVarTableRow = VarTableRow((dim, currentType), None, None, address)
				varTable.add(currentVarId, newVarTableRow)

def checkIfVariableWasDefined(id):
	if refersToClass == True or currentMethod == "":
		varTable = funcDirTable.getVarTable(currentClass, None)
		if varTable.has(id) == False:
			print("Error: Variable '%s' was not declared." % (id))
			sys.exit(0)
	else:
		varTable = funcDirTable.getVarTable(currentMethod, tuple(currentParamTypes))
		if varTable.has(id) == False:
			varTable = funcDirTable.getVarTable(currentClass, None)
			if varTable.has(id) == False:
				print("Error: Variable '%s' was not declared." % (id))
				sys.exit(0)

def getVarAddress(id):
	if refersToClass == True or currentMethod == '':
		varTable = funcDirTable.getVarTable(currentClass, None)
		return varTable.get(id).address
	else:
		varTable = funcDirTable.getVarTable(currentMethod, tuple(currentParamTypes))
		if varTable.has(id):
			return varTable.get(id).address
		else:
			varTable = funcDirTable.getVarTable(currentClass, None)
			return varTable.get(id).address

def getVarType(id):
	if refersToClass == True or currentMethod == '':
		varTable = funcDirTable.getVarTable(currentClass, None)
		return varTable.get(id).varType
	else:
		varTable = funcDirTable.getVarTable(currentMethod, tuple(currentParamTypes))
		if varTable.has(id):
			return varTable.get(id).varType
		else:
			varTable = funcDirTable.getVarTable(currentClass, None)
			return varTable.get(id).varType

def generateQuadForBinaryOperator(operatorList):
	operatorMatch = False
	topOp = invOperatorMapper.get(quadManager.topOp())
	for op in operatorList:
		if topOp == op:
			operatorMatch = True
			break
	if operatorMatch:
		operType2 = quadManager.popType()
		operType1 = quadManager.popType()
		oper2 = quadManager.popOper()
		oper1 = quadManager.popOper()
		operator = quadManager.popOp()
		resType = semanticCube.checkType(operator, operType1, operType2)
		if invKeywordMapper.get(resType) == "error":
			print("Error: Binary '%s' does not support operands of type '%s', '%s'." % (invOperatorMapper.get(operator), invKeywordMapper.get(operType1), invKeywordMapper.get(operType2)))
			sys.exit(0)
		resAddress = getNextAddress(resType, "temp")
		quadManager.addQuad(operator, oper1, oper2, resAddress)
		quadManager.pushOper(resAddress)
		quadManager.pushType(resType)

def generateQuadForUnaryOperator(operatorList):
	operatorMatch = False
	topOp = invOperatorMapper.get(quadManager.topOp())
	for op in operatorList:
		if topOp == op:
			operatorMatch = True
			break
	if operatorMatch:
		operType = quadManager.popType()
		oper = quadManager.popOper()
		operator = quadManager.popOp()
		resType = semanticCube.checkType(operator, -1, operType)
		if invKeywordMapper.get(resType) == "error":
			print("Error: Unary '%s' does not support operand of type '%s'." % (invOperatorMapper.get(operator), invKeywordMapper.get(operType)))
			sys.exit(0)
		resAddress = getNextAddress(resType, "temp")
		quadManager.addQuad(operator, -1, oper, resAddress)
		quadManager.pushOper(resAddress)
		quadManager.pushType(resType)

#PROGRAM
def p_program(p):
	'''program	: imports CLASS ID np_program_1 prog_inh class_block'''

#NEURAL POINTS FOR PROGRAM
def p_np_program_1(p):
	'''np_program_1	:'''
	global currentClass, funcDirTable
	funcDirRow = FuncDirRow("class", False, False)
	currentClass = p[-1]
	funcDirTable.add(currentClass, None, funcDirRow)

def p_prog_inh(p):
	'''prog_inh	: INHERITS ID
							| empty'''

#IMPORTS
def p_imports(p):
	'''imports	: IMPORT CONST_STRING ';' imports
			   			| empty'''

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
	validateAndAddVarsToScope(0)

def p_np_vars_2(p):
	'''np_vars_2	:'''
	global currentType
	currentType = keywordMapper.get("object")
	validateAndAddVarsToScope(0)

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
	answerType = semanticCube.checkType(currentOp, currentType, expressionType)
	if invKeywordMapper.get(answerType) == "error":
		print("Error: Type mismatch in line %d" % (p.lineno))
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
	validateAndAddVarsToScope(1)

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
	validateAndAddVarsToScope(2)

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
		varTable = funcDirTable.getVarTable(currentClass, None)
		dim, primType = varTable.get(currentVarId).varType
		if primType != keywordMapper.get("object"):
			print("Error: Cannot use the '.' operator with '%s', because it is not of object type" % (currentVarId))
			sys.exit(0)
	else:
		varTable = funcDirTable.getVarTable(currentMethod, tuple(currentParamTypes))
		dim, primType = varTable.get(currentVarId).varType
		if primType != keywordMapper.get("object"):
			varTable = funcDirTable.getVarTable(currentClass, None)
			dim, primType = varTable.get(currentVarId).varType
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
	global currentVarId, currentVarIdToAssign
	currentVarId = p[-1]
	currentVarIdToAssign = p[-1]
	checkIfVariableWasDefined(currentVarId)

def p_np_assignment_2(p):
	'''np_assignment_2	:'''
	quadManager.pushOp(p[-1])

def p_np_assignment_3(p):
	'''np_assignment_3	:'''
	currentOp = quadManager.popOp()
	expressionValue = quadManager.popOper()
	expressionType = quadManager.popType()
	if invKeywordMapper.get(expressionType) == "error":
		print("Error: Type mismatch in line %d." % (p.lineno))
		sys.exit(0)
	address = getVarAddress(currentVarIdToAssign)
	quadManager.addQuad(currentOp, -1, expressionValue, address)

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
	'''mat_vec_access	: '[' mat_vec_index mat_access ']' '''

def p_mat_vec_index(p):
	'''mat_vec_index	: '_'
										| expression '''

def p_mat_access(p):
	'''mat_access	: ',' mat_vec_index
								| empty'''

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
	currentMethodType = currentType

def p_np_method_5(p):
	'''np_method_5	:'''
	global currentParamIds, currentParamTypes
	currentParamIds[:] = []
	currentParamTypes[:] = []

def p_np_method_6(p):
	'''np_method_6	:'''
	global funcDirTable, varTable
	if funcDirTable.has(currentMethod, tuple(currentParamTypes)) == True:
		print("Error: Method '%s' was already defined with the same parameters." % (currentMethod))
		sys.exit(0)
	else:
		newFuncDirRow = FuncDirRow(currentMethodType, isCurrentMethodIndependent, isCurrentMethodPrivate)
		funcDirTable.add(currentMethod, tuple(currentParamTypes), newFuncDirRow)
		# Get the VarTable of the 'just created' function.
		varTable = funcDirTable.getVarTable(currentMethod, tuple(currentParamTypes))
		for index in range(len(currentParamIds)):
			if varTable.has(currentParamIds[index]):
				print("Error: Parameter '%s' was already defined for '%s' method" % (currentParamIds[index], currentMethod))
				sys.exit(0)
			else:
				_, primType = currentParamTypes[index]
				address = getNextAddress(primType, "local")
				newVarTableRow = VarTableRow(currentParamTypes[index], None, None, address)
				varTable.add(currentParamIds[index], newVarTableRow)

def p_np_method_7(p):
	'''np_method_7	:'''
	resetLocalMemoryAddresses()

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
	'''param_mat	: ',' np_method_param_5
								| np_method_param_4'''

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
	global currentDim
	currentDim = 0

def p_np_method_param_4(p):
	'''np_method_param_4	:'''
	global currentDim
	currentDim = 1

def p_np_method_param_5(p):
	'''np_method_param_5	:'''
	global currentDim
	currentDim = 2

def p_np_method_param_6(p):
	'''np_method_param_6	:'''
	global currentParamIds, currentParamTypes
	currentParamIds.append(currentParamId)
	currentParamTypes.append((currentDim, currentType))

#CREATE_OBJ
def p_create_obj(p):
	'''create_obj	: NEW func_call'''

#FUNC_CALL
def p_func_call(p):
	'''func_call	: '(' func_param ')' '''

def p_func_param(p):
	'''func_param	: expression more_fpar'''

def p_more_fpar(p):
	'''more_fpar	: ',' func_param
								| empty'''

#BLOCK
def p_block(p):
	'''block	: '{' bstmt '}' '''

def p_bstmt(p):
	'''bstmt	: statement bstmt
						| empty'''

#STATEMENT
def p_statement(p):
	'''statement	: assignment
								| condition
								| loop
								| in_out
								| return
								| var_decl'''

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
	if invKeywordMapper.get(expressionType) != "bool":
		print("Error: Expected boolean expression after 'if'/'elseif' in line %d" % (p.lineno))
		sys.exit(0)
	quadManager.addQuad(operatorMapper.get("GOTOF"), expressionValue, -1, -1)
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
	quadManager.addQuad(operatorMapper.get("GOTO"), -1, -1, -1)
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
	if invKeywordMapper.get(expressionType) != 'bool':
		print("Error: Expected boolean expression in second block of 'for' statement in line %d" % (p.lineno))
		sys.exit(0)
	quadManager.addQuad(operatorMapper.get("GOTOF"), expressionValue, -1, -1)
	quadManager.pushJump(quadManager.quadCont - 1) # quad that jumps to the end of the loop
	quadManager.addQuad(operatorMapper.get("GOTO"), -1, -1, -1) 
	quadManager.pushJump(quadManager.quadCont - 1) # quad that goes to the beginning of the block
	quadManager.pushJump(quadManager.quadCont) # quad that starts update of iteration var

def p_np_for_loop_3(p):
	'''np_for_loop_3	:'''
	modificationBegin = quadManager.popJump()
	conditionEnd = quadManager.popJump()
	falseCondition = quadManager.popJump()
	conditionBegin = quadManager.popJump()
	quadManager.addQuad(operatorMapper.get("GOTO"), -1, -1, conditionBegin)
	quadManager.fill(conditionEnd, quadManager.quadCont)
	quadManager.pushJump(falseCondition)
	quadManager.pushJump(modificationBegin)

def p_np_for_loop_4(p):
	'''np_for_loop_4	:'''
	modificationBegin = quadManager.popJump()
	quadManager.addQuad(operatorMapper.get("GOTO"), -1, -1, modificationBegin)
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
	if invKeywordMapper.get(expressionType) != "bool":
		print("Error: Expected boolean expression after 'while' in line %d" % (p.lineno))
		sys.exit(0)
	quadManager.addQuad(operatorMapper.get("GOTOF"), expressionValue, -1, -1)
	quadManager.pushJump(quadManager.quadCont - 1)

def p_np_while_loop_3(p):
	'''np_while_loop_3	:'''
	endLoop = quadManager.popJump()
	returnToBeginLoop = quadManager.popJump()
	quadManager.addQuad(operatorMapper.get("GOTO"), -1, -1, returnToBeginLoop)
	quadManager.fill(endLoop, quadManager.quadCont)

#IN_OUT
def p_in_out(p):
	'''in_out	: PRINT '(' print_exp ')' ';'
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
	operator = operatorMapper.get('print')
	quadManager.addQuad(operator, -1, -1, expAddress)

def p_np_in_out_2(p):
	'''np_in_out_2	:'''
	global currentVarId
	currentVarId = p[-1]
	idAddress = getVarAddress(currentVarId)
	operator = operatorMapper.get('scan')
	quadManager.addQuad(operator, -1, -1, idAddress)

#RETURN
def p_return(p):
	'''return	: RETURN ret_val ';' '''

def p_ret_val(p):
	'''ret_val	: expression
							| empty'''

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
	'''fact_id	: func_call
							| id_access'''

#NEURAL POINTS FOR FACTOR
def p_np_factor_1(p):
	'''np_factor_1	:'''
	global currentVarId
	currentVarId = p[-1]
	checkIfVariableWasDefined(currentVarId)
	quadManager.pushOper(getVarAddress(currentVarId))
	_, primType = getVarType(currentVarId)
	quadManager.pushType(primType)

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
	ctTypeCode = keywordMapper.get(currentCtType)
	ctAddress = getNextAddress(ctTypeCode, 'temp')
	# When reading quads in VM, if the operator is '=' and oper3 has temp scope, then
	# oper2 is a constant value (not an address) and must be treated as such.
	operator = operatorMapper.get('=')
	quadManager.addQuad(operator, -1, p[-1], ctAddress)
	quadManager.pushOper(ctAddress)
	quadManager.pushType(ctTypeCode)

def p_np_factor_7(p):
	'''np_factor_7	:'''
	operatorList = ["UMINUS", "~"]
	generateQuadForUnaryOperator(operatorList)
	
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