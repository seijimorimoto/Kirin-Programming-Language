# Kirin Programming Language
# Mappers used throughout the compilation and execution process of Kirin
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

operToCode = {
  '=': 101,
  '+': 102,
  '-': 103,
  '*': 104,
  '/': 105,
  '%': 106,
  'UMINUS': 107,
  '>': 201,
  '>=': 202,
  '<': 203,
  '<=': 204,
  '==': 205,
  '<>': 206,
  '~': 207,
  'print': 301,
  'scan': 302,
  'GOTO': 401,
  'GOTOF': 402,
  'GOTOT': 403,
  'GOSUB': 404,
  'ERA': 501,
  'PARAM': 502,
  'PARAM_REF': 503,
  'LOAD_PARAM': 504,
  'LOAD_REF': 505,
  'RETURN': 506,
  'ENDPROC': 507,
  'VER': 601,
  'REF': 602,
  'DEREF': 603,
  'MAP_ATTR': 701,
  'DEL_ATTR': 702,
  '(': 1001
}

codeToOper = {
  101: '=',
  102: '+',
  103: '-',
  104: '*',
  105: '/',
  106: '%',
  107: 'UMINUS',
  201: '>',
  202: '>=',
  203: '<',
  204: '<=',
  205: '==',
  206: '<>',
  207: '~',
  301: 'print',
  302: 'scan',
  401: 'GOTO',
  402: 'GOTOF',
  403: 'GOTOT',
  404: 'GOSUB',
  501: 'ERA',
  502: 'PARAM',
  503: 'PARAM_REF',
  504: 'LOAD_PARAM',
  505: 'LOAD_REF',
  506: 'RETURN',
  507: 'ENDPROC',
  601: 'VER',
  602: 'REF',
  603: 'DEREF',
  701: 'MAP_ATTR',
  702: 'DEL_ATTR',
  1001: '('
}

typeToCode = {
	'int': 1,
	'double': 2,
	'char': 3,
	'bool': 4,
	'object': 5,
	'class': 6,
	'void': 7,
  'error': 8
}

codeToType = {
  1: 'int',
	2: 'double',
	3: 'char',
	4: 'bool',
	5: 'object',
	6: 'class',
	7: 'void',
  8: 'error'
}