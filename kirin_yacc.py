# Kirin Programming Language
# Syntax File
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

import ply.yacc as yacc

from kirin_lex import tokens

#PROGRAM
def p_program(p):
	'''program	: imports CLASS ID prog_inh class_block'''

def p_prog_inh(p):
	'''prog_inh	: INHERITS ID
							| empty'''

#IMPORTS
#TODO: Adjust IMPORTS Syntax Diagram - Add posibility of empty production.
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
	'''access	: acc_scope dependent'''

def p_acc_scope(p):
	'''acc_scope	: PUBLIC
								| PRIVATE'''

def p_dependent(p):
	'''dependent	: INDEPENDENT
								| empty'''

#IDS
def p_ids(p):
	'''ids : ID m_ids'''

def p_m_ids(p):
	'''m_ids	: ',' ids
						| empty'''

#VARS
def p_vars(p):
	'''vars	: VAR ids ':' vars_type ';' '''

def p_vars_type(p):
	'''vars_type	: type vars_tp_a
	        			| ID vars_tp_b'''

def p_vars_tp_a(p):
	'''vars_tp_a	: '=' expression
	   				    | empty'''

def p_vars_tp_b(p):
	'''vars_tp_b	: '=' vars_assgn
	   					  | empty'''

def p_vars_assgn(p):
	'''vars_assgn	: create_obj
	  				    | expression'''

#VEC_MAT_TYPE
def p_ver_mat_type(p):
	'''vec_mat_type	: type
									| ID'''

#VECTOR
def p_vector(p):
	'''vector	: VEC ids ':' vec_mat_type '[' CONST_I ']' vec_assgn ';' '''

def p_vec_assgn(p):
	'''vec_assgn	: '=' vector_exp
								| empty'''

#MATRIX
def p_matrix(p):
	'''matrix	: MAT ids ':' vec_mat_type '[' CONST_I ',' CONST_I ']' mat_assgn ';' '''

def p_mat_assgn(p):
	'''mat_assgn	: '=' matrix_exp
								| empty'''

#ID_ACCESS
def p_id_access(p):
	'''id_access	: id_mat_acc id_var_acc'''

def p_id_mat_acc(p):
	'''id_mat_acc	: mat_vec_access
								| empty'''

def p_id_var_acc(p):
	'''id_var_acc	: '.' ID id_mat_acc
								| empty'''

#ASSIGNMENT
def p_assignment(p):
	'''assignment	: ID id_access '=' ass_value ';' '''

def p_ass_value(p):
	'''ass_value	: create_obj
								| expression
								| matrix_exp
	        			| vector_exp'''

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
	'''method	: func_spec '(' opt_method_param ')' block'''

def p_func_spec(p):
	'''func_spec	: access func_type kw_func ID
								| CONSTRUCTOR'''

def p_func_type(p):
	'''func_type	: VOID
								| type
								| ID'''

def p_kw_func(p):
	'''kw_func	: FUNC
							| empty'''

#METHOD_PARAM
#TODO: Adjust METHOD_PARAM Syntax Diagram - Add posibility of empty production since the beginning.
def p_opt_method_param(p):
	'''opt_method_param : method_param
											| empty'''

def p_method_param(p):
	'''method_param	: ID ':' param_type param_mat_vec more_params'''

def p_more_params(p):
	'''more_params	: ',' method_param
									| empty'''

def p_param_type(p):
	'''param_type	: type
								| ID'''

def p_param_mat_vec(p):
	'''param_mat_vec	: '[' param_mat ']'
										| empty'''

def p_param_mat(p):
	'''param_mat	: ','
								| empty'''

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
								| var_decl
								| CONSTANT var_decl '''

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
#TODO: Adjust IN_OUT Syntax Diagram - Remove CONST_STRING.
def p_in_out(p):
	'''in_out	: PRINT '(' print_exp ')' ';'
						| SCAN '(' ID id_access ')' ';' '''

def p_print_exp(p):
	'''print_exp	: print_val print_more'''

def p_print_val(p):
	'''print_val	: expression'''
#								| CONST_STRING CONFLICT: This production generated one shift/reduce conflict since it was possible to reach CONST_STRING via expression.

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
	'''type	: INT
					| DOUBLE
					| CHAR
					| BOOL'''

#VAR_CTE
def p_var_cte(p):
	'''var_cte	: CONST_I
							| CONST_F
							| CONST_CHAR
							| CONST_STRING
							| CONST_BOOL'''

#FACTOR
#TODO: Adjust FACTOR Syntax Diagram - Remove empty production after id.
def p_factor(p):
	'''factor	: fact_neg fact_body'''

def p_fact_neg(p):
	'''fact_neg	: '-'
							| '~'
							| empty'''

def p_fact_body(p):
	'''fact_body	: '(' expression ')'
								| var_cte
								| ID fact_id'''


def p_fact_id(p):
	'''fact_id	: func_call
							| id_access'''
#							| empty'''   CONFLICT: This production generarted 18 conf red/red, since rule id_access managed already an empty production.


#ERROR
def p_error(p):
	if p:
		print("Syntax error at token", p.type)
	else:
		print("Syntax error at EOF!")


#EMPTY
def p_empty(p):
	'''empty	: '''
	pass


parser = yacc.yacc()

fileName = input("File to analyze: ")
try:
	file = open(fileName, 'r')
	parser.parse(file.read())
	print("Syntax analysis finished.")
except OSError:
	print("The file '%s' does not exist or could not be opened." % (fileName))