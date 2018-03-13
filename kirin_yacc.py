# Kirin Programming Language
# Syntax File
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

# TODO: Whenever an error occurs and the message is displayed, break the execution of the parser.
import ply.yacc as yacc

from kirin_lex import tokens
from funcDirTable import FuncDirTable
from funcDirRow import FuncDirRow
from varTableRow import VarTableRow
from type import Type

keywordMapper = {
	'int': 1,
	'double': 2,
	'char': 3,
	'bool': 4,
	'object': 5,
	'class': 6,
	'void': 7
}

# Initialize global variables with default values
funcDirTable = FuncDirTable()
currentClass = ""
currentMethod = ""
currentMethodType = 0
currentType = 0
currentDim = 0
currentVarId = ""
currentVarIds = []
currentParamId = ""
currentParamIds = []
currentParamTypes = []
isCurrentVarPrivate = True
isCurrentVarIndependent = False
isCurrentMethodPrivate = False
isCurrentMethodIndependent = False
refersToClass = False

# Helper methods for checking semantics during parsing process.
def validateAndAddVarsToScope(dim):
	for currentVarId in currentVarIds:
		if currentMethod == "":
			varTable = funcDirTable.getVarTable(currentClass, None) 
			if varTable.has(currentVarId):
				print("Error: Variable '%s' was already defined." % (currentVarId))
			else:
				newVarTableRow = VarTableRow(Type(dim, currentType), isCurrentVarIndependent, isCurrentVarPrivate)
				varTable.add(currentVarId, newVarTableRow)
		else:
			varTable = funcDirTable.getVarTable(currentMethod, tuple(currentParamTypes))
			if varTable.has(currentVarId):
				print("Error: Variable '%s' was already defined." % (currentVarId))
			else:
				newVarTableRow = VarTableRow(Type(dim, currentType), None, None)
				varTable.add(currentVarId, newVarTableRow)

def checkIfVariableWasDefined(id):
	if refersToClass == True or currentMethod == "":
		varTable = funcDirTable.getVarTable(currentClass, None)
		if varTable.has(id) == False:
			print("Error: Variable '%s' was not declared." % (id))
	else:
		varTable = funcDirTable.getVarTable(currentMethod, tuple(currentParamTypes))
		if varTable.has(id) == False:
			varTable = funcDirTable.getVarTable(currentClass, None)
			if varTable.has(id) == False:
				print("Error: Variable '%s' was not declared." % (id))

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
	'''vars_tp_a	: '=' expression
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
		if varTable.get(currentVarId).varType.primType != keywordMapper.get("object"):
			print("Error: Cannot use the '.' operator with '%s', because it is not of object type" % (currentVarId))
	else:
		varTable = funcDirTable.getVarTable(currentMethod, tuple(currentParamTypes))
		if varTable.get(currentVarId).varType.primType != keywordMapper.get("object"):
			varTable = funcDirTable.getVarTable(currentClass, None)
			if varTable.get(currentVarId).varType.primType != keywordMapper.get("object"):
				print("Error: Cannot use the '.' operator with '%s', because it is not of object type" % (currentVarId))

#ASSIGNMENT
def p_assignment(p):
	'''assignment	: this ID np_assignment_1 id_access '=' ass_value ';' '''

def p_ass_value(p):
	'''ass_value	: create_obj
								| expression
								| matrix_exp
	        			| vector_exp'''

#NEURAL POINTS FOR ASSIGNMENT
def p_np_assignment_1(p):
	'''np_assignment_1	:'''
	global currentVarId
	currentVarId = p[-1]
	checkIfVariableWasDefined(currentVarId)

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
	'''method	: func_spec '(' np_method_5 opt_method_param ')' np_method_6 block'''

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
	global isCurrentMethodPrivate, isCurrentMethodIndependent, currentMethod, currentType
	isCurrentMethodPrivate = False
	isCurrentMethodIndependent = False
	currentMethod = "constructor"
	currentType = None

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
	else:
		newFuncDirRow = FuncDirRow(currentMethodType, isCurrentMethodIndependent, isCurrentMethodPrivate)
		funcDirTable.add(currentMethod, tuple(currentParamTypes), newFuncDirRow)
		# Get the VarTable of the 'just created' function.
		varTable = funcDirTable.getVarTable(currentMethod, tuple(currentParamTypes))
		for index in range(len(currentParamIds)):
			if varTable.has(currentParamIds[index]):
				print("Error: Parameter '%s' was already defined for '%s' method" % (currentParamIds[index], currentMethod))
			else:
				dim, primType = currentParamTypes[index]
				newVarTableRow = VarTableRow(Type(dim, primType), None, None)
				varTable.add(currentParamIds[index], newVarTableRow)

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
	currentParamTypes.append(Type(currentDim, currentType).toTuple())

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
	'''condition	: IF cond_body'''

def p_cond_body(p):
	'''cond_body	: '(' expression ')' block cond_else'''

def p_cond_else(p):
	'''cond_else	: ELSE block
								| ELSEIF cond_body
								| empty'''

#LOOP
def p_loop(p):
	'''loop	: for_loop
					| while_loop'''

#FOR_LOOP
def p_for_loop(p):
	'''for_loop	: FOR '(' assignment expression ';' ID '=' expression ')' block'''

#WHILE_LOOP
def p_while_loop(p):
	'''while_loop	: WHILE '(' expression ')' block'''

#IN_OUT
def p_in_out(p):
	'''in_out	: PRINT '(' print_exp ')' ';'
						| SCAN '(' ID id_access ')' ';' '''

def p_print_exp(p):
	'''print_exp	: print_val print_more'''

def p_print_val(p):
	'''print_val	: expression'''

def p_print_more(p):
	'''print_more	: ',' print_exp
								| empty'''

#RETURN
def p_return(p):
	'''return	: RETURN ret_val ';' '''

def p_ret_val(p):
	'''ret_val	: expression
							| empty'''

#EXPRESSION
def p_expression(p):
	'''expression	: rel_expression expression_op'''

def p_expression_op(p):
	'''expression_op	: AND expression
										| OR expression
										| XOR expression
										| empty'''

#REL_EXPRESSION_1
def p_rel_expression(p):
	'''rel_expression	: rel_expression_1 rel_exp_op'''

def p_rel_exp_op(p):
	'''rel_exp_op	: EQUAL rel_expression
								| NOT_EQUAL rel_expression
								| empty'''

#REL_EXPRESSION_1
def p_rel_expression_1(p):
	'''rel_expression_1	: exp rel_exp_1_op'''

def p_rel_exp_1_op(p):
	'''rel_exp_1_op	: '<' rel_expression_1
									| LESS_EQUAL_THAN rel_expression_1
									| '>' rel_expression_1
									| GREATER_EQUAL_THAN rel_expression_1
									| empty'''

#EXP
def p_exp(p):
	'''exp	: term exp_op'''

def p_exp_op(p):
	'''exp_op	: '+' exp
						| '-' exp
						| empty'''

#TERM
def p_term(p):
	'''term	: factor term_op'''

def p_term_op(p):
	'''term_op	: '*' term
							| '/' term
							| '%' term
							| empty'''

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
	'''var_cte	: CONST_I
							| CONST_F
							| CONST_CHAR
							| CONST_STRING
							| CONST_BOOL'''

#FACTOR
def p_factor(p):
	'''factor	: fact_neg fact_body'''

def p_fact_neg(p):
	'''fact_neg	: '-'
							| '~'
							| empty'''

def p_fact_body(p):
	'''fact_body	: '(' expression ')'
								| var_cte
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

#ERROR
def p_error(p):
	if p:
		print("Line #%d: Syntax error at token %s" % (p.lexer.lineno, p.type))
	else:
		print("Syntax error at EOF!")

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
	print("Syntax analysis finished.")
except OSError:
	print("The file '%s' does not exist or could not be opened." % (fileName))