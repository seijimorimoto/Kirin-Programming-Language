# Kirin Programming Language
# Lexic File
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380


import ply.lex as lex

tokens = (
	'CLASS',
	'INHERITS',
	'CONSTANT',
	'PUBLIC',
	'PRIVATE',
	'INDEPENDENT',
	'CONSTRUCTOR',
	'VAR',
	'FUNC',
	'MAT',
	'VEC',
	'NEW',
	'IF',
	'ELSE',
	'FOR',
	'WHILE',
	'PRINT',
	'SCAN',
	'RETURN',
	'AND',
	'OR',
	'XOR',
	'LESS_EQUAL_THAN',
	'GREATER_EQUAL_THAN',
	'EQUAL',
	'NOT_EQUAL',
	'IMPORT',
	'INT'
	'DOUBLE',
	'CHAR',
	'BOOL',
	'ID',
	'CONST_I',
	'CONST_F',
	'CONST_STRING',
	'CONST_CHAR',
	'CONST_BOOL'
	)

literals = ['=', '+', '-', '*', '/', '>', '<', '~', '_', ',']
ignore = ' \t\n'

# Reserved Keywords

def t_CLASS(t):
	r'class'
	return t

def t_INHERITS(t):
	r'inherits'
	return t

def t_CONSTANT(t):
	r'constant'
	return t

def t_PUBLIC(t):
	r'public'
	return t

def t_PRIVATE(t):
	r'private'
	return t

def t_INDEPENDENT(t):
	r'independent'
	return t

def t_CONSTRUCTOR(t):
	r'constructor'
	return t

def t_VAR(t):
	r'var'
	return t

def t_FUNC(t):
	r'func'
	return t

def t_MAT(t):
	r'mat'
	return t

def t_VEC(t):
	r'vec'
	return t

def t_NEW(t):
	r'new'
	return t

def t_IF(t):
	r'if'
	return t

def t_ELSE(t):
	r'else'
	return t

def t_FOR(t):
	r'for'
	return t

def t_WHILE(t):
	r'while'
	return t

def t_PRINT(t):
	r'print'
	return t

def t_SCAN(t):
	r'scan'
	return t

def t_RETURN(t):
	r'return'
	return t

def t_AND(t):
	r'and|AND'
	return t

def t_OR(t):
	r'or|OR'
	return t

def t_XOR(t):
	r'xor|XOR'
	return t

def t_LESS_EQUAL_THAN(t):
	r'<='
	return t

def t_GREATER_EQUAL_THAN(t):
	r'>='
	return t

def t_EQUAL(t):
	r'=='
	return t

def t_NOT_EQUAL(t):
	r'<>'
	return t

def t_IMPORT(t):
	r'import'
	return t

def t_INT(t):
	r'int'
	return t

def t_DOUBLE(t):
	r'double'
	return t

def t_CHAR(t):
	r'char'
	return t

def t_BOOL(t):
	r'bool'
	return t

def t_ID(t):
	r'[a-zA-Z][0-9a-zA-Z_]*'
	return t

def t_CTE_I(t):
	r'[0-9]+'
	return t

def t_CTE_F(t):
	r'[0-9]+\.[0-9]+'
	return t

def t_CTE_STRING(t):
	r'\"[^\"]*\"'
	return t

def t_CONST_CHAR(t):
	r'\’[^\’]\’'
	return t

def t_CONST_BOOL(t):
	r'true|false'
	return t

def t_error(t):
	print("%d: Illegal character '%s'" % (t.lexer.lineno, t.value[0]))
	print(t.value)
	t.lexer.skip(1)

lex.lex()
