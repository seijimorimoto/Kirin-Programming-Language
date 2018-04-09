# Kirin Programming Language
# Lexic File
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

import sys
import ply.lex as lex

reservedWords = { 
  'class': 'CLASS',
  'Main': 'MAIN',
  'inherits': 'INHERITS',
  'public': 'PUBLIC',
  'private': 'PRIVATE',
  'public_func': 'PUBLIC_FUNC',
  'private_func': 'PRIVATE_FUNC',
  'independent': 'INDEPENDENT',
  'var': 'VAR',
  'vec': 'VEC',
  'mat': 'MAT',
  'void': 'VOID',
  'constructor': 'CONSTRUCTOR',
  'new': 'NEW',
  'this': 'THIS',
  'if': 'IF',
  'else': 'ELSE',
  'elseif': 'ELSEIF',
  'for': 'FOR',
  'while': 'WHILE',
  'print': 'PRINT',
  'scan': 'SCAN',
  'return': 'RETURN',
  'int': 'INT',
  'double': 'DOUBLE',
  'char': 'CHAR',
  'bool': 'BOOL'
}

tokens = ['ID', 
'CONST_I',
'CONST_F',
'CONST_CHAR',
'CONST_STRING',
'CONST_BOOL',
'LESS_EQUAL_THAN',
'GREATER_EQUAL_THAN',
'EQUAL',
'NOT_EQUAL',
'AND',
'OR',
'XOR']

tokens = tokens + list(reservedWords.values())

literals = ['=', '+', '-', '*', '%', '/', '>', '<', '~', '_', ',', ';', ':', '.', '{', '}', '[', ']', '(', ')']
t_ignore = ' \t'

def t_COMMENT(t):
  r'\/\/.*'
  pass

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

def t_AND(t):
  r'and|AND'
  return t

def t_OR(t):
  r'or|OR'
  return t

def t_XOR(t):
  r'xor|XOR'
  return t

def t_CONST_F(t):
	r'[0-9]+\.[0-9]+'
	return t

def t_CONST_I(t):
	r'[0-9]+'
	return t

def t_CONST_STRING(t):
	r'\"[^\"]*\"'
	return t

def t_CONST_CHAR(t):
	r'\’[^\’]\’'
	return t

def t_CONST_BOOL(t):
	r'true|false'
	return t

def t_ID(t):
	r'[a-zA-Z][0-9a-zA-Z_]*'
	t.type = reservedWords.get(t.value, 'ID')
	return t

def t_error(t):
	print("Line # %d: Illegal character '%s'" % (t.lexer.lineno, t.value[0]))
	t.lexer.skip(1)
	sys.exit(0)

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

lex.lex()