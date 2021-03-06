# Kirin Programming Language
# Constants used throughout the compilation and execution process of Kirin
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

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

# Constants indicating the start of each type of memory addresses.
# These constants are exclusively used in the virtual machine.
CONST_GLOBAL_START = CONST_G_BEGIN_INT
CONST_LOCAL_START = CONST_L_BEGIN_INT
CONST_CONSTANT_START = CONST_CT_BEGIN_INT
