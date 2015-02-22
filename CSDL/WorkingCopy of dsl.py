import matplotlib.pyparsing as pp
import re


class DSLParser(object):

    """Expose the PyParsing exception as to avoid creating import dependencies downstream.""" 
    ParseException = pp.ParseBaseException
    
    def __init__(self):
        #print "CTOR"
        # supported operators
        operator = pp.Regex(r"<=|>=|<>|\!=|==|<|>|not|in|regex_partial|regex_exact|geo_box|geo_radius|geo_polygon|contains_any|substr|contains_near|any|contains_substr|near|contains").setName("operator").addParseAction(self.validateOperator)("op")
        
        # literals
        number = pp.Regex(r"[+-]?\d+(:?\.\d*)?(:?[eE][+-]?\d+)?").setName("number")
        numberList = pp.Group(pp.Literal('[') + number + pp.ZeroOrMore("," + number) + pp.Literal(']')).setName("numberList")
        string = pp.dblQuotedString
        #literals = (number | string)("lit")
        literals = (number | numberList | string)("lit")
        #literals = pp.Group(number | numberList | string).setName("literals").addParseAction(self.validateLiterals)
    
        # symbols
        #identifier = pp.Regex(r"[a-z][a-z_]+(?:\.[a-z][a-z_]+)+").addParseAction(self.validateIdentifier).setName("identifier")
        identifier = pp.Regex(r"[a-z][a-z_]+(?:\.[a-z][a-z_]+)+").setName("identifier").addParseAction(self.validateIdentifier)("id")
    
        # we'll get there...
        subExpr = pp.Forward()
    
        # predicates
        stream = pp.Group(pp.Literal("stream") + string).setName("stream")
        exists = pp.Group(identifier + pp.Literal("exists")).setName("exists")
    
        # boolean predicates
        
        comparison = pp.Group(
            identifier + operator + literals
            | literals + operator + identifier
        ).setName("comparison")("comp")
        
        #comparison = (identifier + operator + literals).setName("comparison")("comp")
        #comparison = identifier + operator + literals | literals + operator + identifier
        
        condition = comparison | stream | exists | subExpr
        subExpr << pp.nestedExpr(content=condition)
    
        # standard boolean operator precedence
        expr = pp.operatorPrecedence(condition,[
            (pp.CaselessLiteral("not"), 1, pp.opAssoc.RIGHT, ), 
            (pp.CaselessLiteral("AND"), 2, pp.opAssoc.LEFT, ),
            (pp.CaselessLiteral("OR"), 2, pp.opAssoc.LEFT, ),
            ])("expr")
    
        # tag "thing" { expr }
        tag = pp.Group(pp.Literal("tag") + pp.quotedString + pp.nestedExpr("{", "}", expr)).setName("tag")
    
        # return { expr }
        a_return = pp.Group(pp.Literal("return") + pp.nestedExpr("{", "}", expr)).setName("return")
    
        # a single expression or tag [, tag, ...] return { expression }
        parser = expr | (pp.OneOrMore(tag) + a_return)
    
        # handle multilines
        parser.setDefaultWhitespaceChars(" \t\n\r")
    
        # handle // comments
        parser.ignore("//" + pp.restOfLine)
        
        self.parser = parser
    
    def parseString(self, s):
        """Parses a given string into an AST."""
        print 'String => ', s
        return self.parser.parseString(s)

    def validateIdentifier(self, tokens):
        """Called for every operator parsed."""
        return tokens
        
    def validateOperator(self, tokens):
        """Called for every operator parsed.""" 
        return tokens
    
    def validateLiterals (self, tokens):
        """Called for every literal parsed.""" 
        return tokens
    
    def flatten(self, expr):
        print 'flatten-- ', expr
        a = []
        contains_sub_expr = False
        if isinstance(expr, list):
            for ex in expr:
                cv, v = self.flatten(ex)
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


parser = DSLParser()


#parsed = parser.parseString('twitter.text contains "Cincinnati Reds"')
#assert parsed.asList() == [['twitter.text', 'contains', '"Cincinnati Reds"']]
#parsed = parser.parseString('NOT twi.uh <= 56 AND twi.ui >= 90 OR stream "jkdjd" AND twi.uy exists')
parsed = parser.parseString('twi.uy exists AND twi.uh <= 56 AND twi.ui >= 90 AND stream "as8e9j98838"')
#parsed = parser.parseString('twi.uh <= 56 OR twi.ui >= 90 OR tw.uu != 67')
#print parsed.expr[0].op , "--", parsed.expr[0].lit, "--", parsed.expr[0].id
#print parsed.asXML("Top")
#c,v = parser.flatten(parsed.asList())
#print c, " -- ", v
#print parsed.dump()
print '""""""'
print parsed.dump()
def myDump(p1):
    for i in p1.expr:
        print i, "--", len(i)
        try:
            if len(i) == 2 :
                if i[0] == "stream":
                    print "stream ",i[1]
                elif i[1] == "exists":
                    print i[0], "exists"
            elif hasattr(i, "comp"):
                print "id = ",i.id
                print "op = ",i.op
                print "lit = ",i.lit              
                myDump(i)
            
            else:
                print "Logical Op = ",i
        except (IndexError, AttributeError), e:
            print e
        
            

myDump(parsed)
    
#print parsed.asList ,len( parsed)
'''
print parsed.items
print parsed.asList
print parsed.asDict
print parsed.asXML
'''

