'''
Created on Mar 1, 2015

@author: jsyadav
'''
from matplotlib.pyparsing import *
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
        return  "(" + sep.join(map(str,self.args)) + ")"        
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
    
class SchoolNode(object):
    def __init__(self,t):
        self.reach = 'Reach : ', [t[2],t[4]]
        self.target = 'Target : ',[t[8],t[10]]
        self.safety = 'Safety : ',[t[14],t[16]]
        
    def __str__(self):
        sep = " "
        return "(" + sep.join(map(str, [self.reach, self.target, self.safety])) + ")"          
    __repr__ = __str__
 
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
  
schoolList = Literal('[') + word + ZeroOrMore(','+word) + Literal(']')
RTS = Word('select Reach ')+ schoolList + Word('Target ')+schoolList+ Word('Safety ')+schoolList
RTS.setParseAction(SchoolNode)
select = rule + RTS

  
if __name__ == "__main__":
    
    gpa = input('Enter your wt. gpa > ')
    sat = input('Enter your sat score > ')
    #major = input('Enter your major choice > ')
    major = 'science'
    #gpa = 3.71
    #sat = 2251 
   
    tests = [ 
             'gpa >= 4.15 and sat > 1950 select Reach [Berkeley , LA ]  Target [SanDiego , Davis ] Safety [Irvine , Merced ]',
             'gpa >= 4.10 and sat > 2050 and major != \'math\' select Reach [LA , Berkeley ]  Target [SanDiego , Davis ] Safety [Irvine , Merced ]',
             'gpa > 4.05 and sat > 2150 and major == \'biotech\' select Reach [Berkeley , LA ]  Target [SanDiego , Davis ] Safety [Irvine , Merced ]',
             'gpa > 4.0 and sat > 2250 select Reach [Berkeley , LA ]  Target [SanDiego , Davis ] Safety [Irvine , Merced ]', 
             'gpa < 4.05 and gpa > 3.80 and sat > 2250 select Reach [SanDiego , Davis ]  Target [Irvine , Merced ] Safety [SanJose , Pamona ]',             
             'not  gpa < 3.85 and gpa > 3.70 and sat > 1950 select Reach [Irvine , Merced ]  Target [SanJose , Pamona ] Safety [Sacramento , Chico ]',
             'gpa < 3.85 and gpa > 3.70 and sat > 1950 select Reach [Irvine , Merced ]  Target [SanJose , Pamona ] Safety [Sacramento , Chico ]',          
              ]
    print("gpa =", gpa)
    print("sat =", sat)
    print("major =", major)

    print()
    for t in tests:
        res = select.parseString(t)
        result = res[0].solve()
        #print 'parsed list ',res, " result ",result
        if result:
            pass
            print 'Your RTS graph is ',res[1]
            break
            
       

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
    

