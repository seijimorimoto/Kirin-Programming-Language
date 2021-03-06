# Kirin Programming Language
# QuadruplueManager class
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

from stack import Stack
from quadruple import Quadruple
from kirinMappers import operToCode
from kirinMappers import codeToOper

class QuadrupleManager(object):
  
  def __init__(self):
    self.stackOp = Stack()
    self.stackOper = Stack()
    self.stackTypes = Stack()
    self.stackJumps = Stack()
    self.stackDims = Stack()
    # Insert a false element in each stack, so that it always contains a top element.
    self.stackOp.push(999)
    self.stackOper.push(999)
    self.stackTypes.push(999)
    self.stackJumps.push(999)
    self.stackDims.push(999)
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
    self.stackOp.push(operToCode.get(op))
  
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
  
  def topType(self):
    return self.stackTypes.top()
  
  def pushJump(self, jump):
    self.stackJumps.push(jump)
  
  def popJump(self):
    return self.stackJumps.pop()
  
  def topJump(self):
    return self.stackJumps.top()
  
  def pushDim(self, id, dim):
    self.stackDims.push((id, dim))
  
  def popDim(self):
    return self.stackDims.pop()

  def topDim(self):
    return self.stackDims.top()
  
  def fill(self, quadPos, value):
    self.queueQuad[quadPos].oper3 = value
  
  def printToFile(self, fileName):
    file = open(fileName, "w")
    cont = 0 # for debugging purposes.
    for quad in self.queueQuad:
      file.write(str(quad))
      file.write("\n")
      # Print for debugging.
      print("%d) %s, %d, %s, %d" % (cont, codeToOper.get(quad.op), quad.oper1, quad.oper2, quad.oper3))
      cont = cont + 1
    file.close()