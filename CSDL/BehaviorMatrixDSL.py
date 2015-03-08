#from csdl import CSDLParser
from pyparsing import *
from string import find

class ExpNode(object):
    def __init__(self, t):
        self.lhs = t[0][0]
        self.op = t[0][1]
        self.rhs = t[0][2]
        
    def __str__(self):
        sep = " %s " % self.op
        return "(" + sep.join(map(str, [self.lhs, self.rhs])) + ")"          
    __repr__ = __str__
    
    def solve(self):
        if self.op == 'contains':          
            return bool(find(self.lhs, self.rhs) + 1)# add 1, as bools(-1) is true
        else: 
            return eval(repr(self))
        
        
class BinaryNode(object):
    def __init__(self, t):
        self.args = t[0][0::2]
        
    def __str__(self):
        sep = " %s " % self.reprsymbol
        return "(" + sep.join(map(str, self.args)) + ")"   
        
    __repr__ = __str__
    
    

class BoolAnd(BinaryNode):
    reprsymbol = '&'
    evalop = all
    def solve(self):
        for a in self.args:
            if not isinstance(a, ExpNode):
                if not bool(a):
                    return False    
            else:
                if not a.solve():
                    return False
        return True


class BoolOr(BinaryNode):
    reprsymbol = '|'
    evalop = any
    def solve(self):
        for a in self.args:
            if not isinstance(a, ExpNode):
                if bool(a):
                    return True    
            else:
                if a.solve():
                    return True
        return False

        
class UnaryNode(object):
    def __init__(self, t):
        self.op = t[0][0]
        self.rhs = t[0][1]
        
    def __str__(self):
        sep = " "
        return "(" + sep.join(map(str, [self.op, self.rhs])) + ")"          
    __repr__ = __str__
    
    def solve(self):  
        return eval(repr(self))
 
operator = Regex(r"<=|>=|<>|\!=|==|<|>|not|in|regex_partial|regex_exact|geo_box|"+
                "geo_radius|geo_polygon|contains_any|substr|contains_near|any|contains_substr|near|"+
                "contains")

unicode_printables = u''.join(unichr(c) for c in xrange(65536)
                                        if not unichr(c).isspace()) 
word = Word(unicode_printables)
expr = Group(word + operator + word)
expr.setParseAction(ExpNode)

rule = operatorPrecedence(expr,[
            (CaselessLiteral("not"), 1, opAssoc.RIGHT,UnaryNode), 
            (CaselessLiteral("and"), 2, opAssoc.LEFT,BoolAnd),
            (CaselessLiteral("or"), 2, opAssoc.LEFT,BoolOr),
            ])
  
if __name__ == "__main__":
    tell = 58
    nell = 75
    kell = 30
   
    tests = ['tell < 56',
              'tell < 56 and nell != 78',
              'tell < 56 or nell != 78',
              'NOT tell < 56',
              'tell < 56 and nell != 78 and kell < 34',
              'tell < 56 or nell != 78 or kell < 34',
              'tell < 56 and nell != 78 or kell < 34',
              'tell < 56 or nell != 78 and kell < 34',        
              'not tell < 56 or nell != 78 or kell < 34',
              'tell < 56 and not nell != 78 or kell < 34',
              'tell < 56 or not nell != 78 and kell < 34',
              'not tell < 56 and nell != 78 and kell < 34',
              'tell contains ell',
              'tell contains eyll',
              ]
    print("tell =", tell)
    print("nell =", nell)
    print("kell =", kell)
    print()
    for t in tests:
        res = rule.parseString(t)
        print 'parsed list ',res, " eval ",res[0].solve()

def flatten(expr):
        print 'flatten-- ', expr
        a = []
        contains_sub_expr = False
        if isinstance(expr, list):
            for ex in expr:
                cv, v = flatten(ex)
                contains_sub_expr = contains_sub_expr or cv 
                if cv:
                    a.append("(")
                    a.append(v)
                    a.append(")")
                else:
                    a.append(v)
        else:
            return False, expr
        return contains_sub_expr, " ".join(a)
    

