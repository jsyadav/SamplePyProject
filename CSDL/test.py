#from csdl import CSDLParser
from matplotlib.pyparsing import *


 
class AST(object):
    def __init__(self, t):
        print "__init__ AST ", t

               

class OST(object):
    def __init__(self,t):
        print "__init__ OST ", t
    
class EST(object):
    def __init__(self,t):
        print "__init__ EST ", t
    

operator = Regex(r"<=|>=|<>|\!=|==|<|>|not|in|regex_partial|regex_exact|geo_box|"+
                "geo_radius|geo_polygon|contains_any|substr|contains_near|any|contains_substr|near|"+
                "contains")


lpar, rpar = map(Suppress, "()")
subexpr = Forward()
 
unicode_printables = u''.join(unichr(c) for c in xrange(65536)
                                        if not unichr(c).isspace())
 
word = Word(unicode_printables)
expr = Group(word + operator + word)
expr.setParseAction(EST)



subexpr << nestedExpr(content=expr) 

#_and = CaselessLiteral("AND").setParseAction(ast.makeExpressionNode)

rule = operatorPrecedence(expr,[
            (CaselessLiteral("NOT"), 1, opAssoc.RIGHT, ), 
            (CaselessLiteral("AND"), 2, opAssoc.LEFT, AST),
            (CaselessLiteral("OR"), 2, opAssoc.LEFT,OST ),
            ])
    
#parsed = expr.parseString('tell < 56')
#parsed = expr.parseString('(tell < 56)')
parsed = rule.parseString('(tell < 56) AND (nell != 89) OR (tell < 65) AND (nell != 98)')
print "parsed ", parsed


#parsed = rule.parseString('tell < 5665 AND nell != 89 OR tell < 45')

#parsed = rule.parseString('tell AND (dell == null)')



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
    
#print flatten(parsed)
'''   
print flatten(parsed.asList())    
    
t = lambda x : x*x
print t(4)

f = lambda x,y: x*y
print f(4,5)

level=0
## [A op b]
def printTree(result):
    global level
    l = len(result)
    if isinstance(result, type([])):
        for i in range(0,l) :
            if isinstance(result[i], type([])) is False: # to the topple            
                lhs = result[i]
                op = result[i+1]
                rhs = result[i+2]
                print level , " ", op
                level +=1
                printTree(result[i])
                printTree(result[i+2])
            else:
               printTree(result[i])
        
#print printTree(parsed.asList())
def PrintStrings(L):
    if isinstance(L, basestring):
        print L
    else:
        for x in L:
            PrintStrings(x)


l = [[['a', 'b', 'c'], ['d']],[['e'], ['f'], ['g']]]
import compiler

for x in compiler.ast.flatten(l):
     print x
#PrintStrings(l)

#assert parsed.asList() == [['twitter.text', 'contains', '"Cincinnati Reds"']]
#parsed = parser.parseString('NOT twi.uh <= 56 AND twi.ui >= 90 OR stream "jkdjd" AND twi.uy exists')

parsed = parser.parseString('twi.uh <= 56 AND twi.ui >= 90 ')
print parsed.expr[0].op , "--", parsed.expr[0].lit, "--", parsed.expr[0].id
print parsed.asXML("Top")
print parsed.dump()
print parsed.asList ,len( parsed)
print parsed.items
print parsed.asList
print parsed.asDict
print parsed.asXML

parsed = parser.parseString('56 == twi.uh')
print parsed,len( parsed[0])
parsed = parser.parseString('twi.uh > 56 tag "jit" {twitter.txt < 89} return {twitter.txtu contains 90}')
print parsed
parsed = parser.parseString('stream "yuiu" exists "kio"')
print parsed
parsed = parser.parseString('tr.kiy exists ')
print parsed
parsed = parser.parseString('tag "jit" {twitter.txt < 89} return {twitter.txtu contains 90}')
print parsed
parsed = parser.parseString('twitter.txt contains "iphone", stream "http"')
print parsed

#p = pp.Regex(r"[a-z][a-z_]+(?:\.[a-z][a-z_]+)+").setName("identifier").addParseAction(self.validateIdentifier)
p = ppp.Regex(r"[a-z][a-z_]+(\.[a-z][a-z_]+)+").setName("identifier")
parsed = p.parseString ('ddgsggg.jkj.jk_jk.iuuu_')
print parsed.asList()

#parsed = parser.parseString('jitendra.text.hj > "hello" return {56}');
#parsed = parser.parseString('"identifier" < jitendra.text.hj  stream exists return {}');
#print parsed.asList

'''
