'''
Created on Feb 21, 2015

@author: jyadav
'''

import matplotlib.pyparsing as pp
from matplotlib.pyparsing import *
import re

class Node(list):
    def __eq__(self, other):
        return list.__eq__(self, other) and self.__class__ == other.__class__
        
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, list.__repr__(self))
 
    @classmethod
    def group(cls, expr):
        def group_action(s, l, t):
            try:
                lst = t[0].asList()
            except (IndexError, AttributeError), e:
                lst = t
            return [cls(lst)]
 
        return Group(expr).setParseAction(group_action)
 
    def get_query(self):
        raise NotImplementedError()

## For Comparison String 
class ComparisonNode(Node):
    def get_query(self):
        field = self[0]
        op = self[1]
        node = self[2]
 
        if op == 'contains':
            return {
            'match_phrase': {
                 field: node
             }
        }
        elif op == '==':
            return {
                'match_phrase': {
                 field: node
                 }
            }
        else:
            raise NotImplementedError('Only "contains" comparisons are implemented.')
  

# Actual Parser
class ElasticSearchDSLParser(object):

    """Expose the PyParsing exception as to avoid creating import dependencies downstream.""" 
    ParseException = pp.ParseBaseException
    
    def __init__(self):
        # supported operators
        operator = pp.Regex(r"<=|>=|<>|\!=|==|<|>|not|in|regex_partial|regex_exact|geo_box|"+
                "geo_radius|geo_polygon|contains_any|substr|contains_near|any|contains_substr|near|"+
                "contains").setName("operator").addParseAction(self.validateOperator)("op")
        
        # literals
        number = pp.Regex(r"[+-]?\d+(:?\.\d*)?(:?[eE][+-]?\d+)?").setName("number")
        numberList = pp.Group(pp.Literal('[') + number + pp.ZeroOrMore("," + number) + pp.Literal(']')).setName("numberList")
        string = pp.dblQuotedString
        unicode_printables = u''.join(unichr(c) for c in xrange(65536)
                                        if not unichr(c).isspace())
 
        word = Word(unicode_printables)
        literals = (number | numberList | string | word).setName("literals").addParseAction(self.validateLiterals)("lit")
    
        # symbols
        identifier = word
        
    
        # we'll get there...
        subExpr = pp.Forward()
    
        # predicates
        stream = pp.Group(pp.Literal("stream") + string).setName("stream")("st")
        exists = pp.Group(identifier + pp.Literal("exists")).setName("exists")("ex")
    
        # boolean predicates        
        comparison = ComparisonNode.group(
            identifier + operator + literals
            | literals + operator + identifier
        ).setName("comparison")("comp")
        
        condition = comparison | stream | exists | subExpr
        subExpr << pp.nestedExpr(content=condition)
    
        # standard boolean operator precedence    
        ''' 
        expr = pp.operatorPrecedence(condition,[
            (pp.CaselessLiteral("NOT"), 1, pp.opAssoc.RIGHT, ), 
            (pp.CaselessLiteral("AND"), 2, pp.opAssoc.LEFT, ),
            (pp.CaselessLiteral("OR"), 2, pp.opAssoc.LEFT, ),
            ])("expr")
        '''
        expr = pp.OneOrMore(condition)("expr")

        # a single expression 
        parser = expr 
    
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


if __name__ == '__main__':
    pass