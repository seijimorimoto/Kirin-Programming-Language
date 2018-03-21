# Kirin Programming Language
# QuadruplueManager class
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

from stack import Stack
from quadruple import Quadruple

operatorMapper = {
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
  '(': 1001
}

invOperatorMapper = {
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
  1001: '('
}


class QuadrupleManager(object):
  
  def __init__(self):
    self.stackOp = Stack()
    self.stackOper = Stack()
    self.stackTypes = Stack()
    # Insert a false element in each stack, so that it always contains a top element.
    self.stackOp.push(999)
    self.stackOper.push(999)
    self.stackTypes.push(999)
    self.queueQuad = []
    self.quadCont = 0

  # op = Numeric code representation of an operator.
  # oper1 = Memory address of operand 1.
  # oper2 = Memory address of operand 2.
  # oper3 = Memory address of operand 3.
  def addQuad(self, op, oper1, oper2, oper3):
    newQuad = Quadruple(op, oper1, oper2, oper3)
    self.queueQuad.append(newQuad)
    self.quadCont = self.quadCont + 1
  
  def pushOp(self, op):
    self.stackOp.push(operatorMapper.get(op))
  
  def popOp(self):
    return self.stackOp.pop()
  
  def topOp(self):
    return self.stackOp.top()

  def pushOper(self, oper):
    self.stackOper.push(oper)
  
  def popOper(self):
    return self.stackOper.pop()
  
  def topOper(self):
    return self.stackOper.top()

  def pushType(self, type):
    self.stackTypes.push(type)
  
  def popType(self):
    return self.stackTypes.pop()
  
  def topTypes(self):
    return self.stackTypes.top()
  
  def printToFile(self, fileName):
    file = open(fileName, "w")
    for quad in self.queueQuad:
      file.write(str(quad))
      file.write("\n")
      # Print for debugging.
      print("%s, %d, %s, %d" % (invOperatorMapper.get(quad.op), quad.oper1, quad.oper2, quad.oper3))
    file.close()