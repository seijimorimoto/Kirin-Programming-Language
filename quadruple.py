# Kirin Programming Language
# Quadruple class
# Jose Juan Zavala Iglesias		| A01281362
# Angel Seiji Morimoto Burgos	| A01281380

class Quadruple(object):
  
  def __init__(self, op, oper1, oper2, oper3):
    self.op = op
    self.oper1 = oper1
    self.oper2 = oper2
    self.oper3 = oper3
  
  def __str__(self):
    return "%d %d %s %d" % (self.op, self.oper1, self.oper2, self.oper3)