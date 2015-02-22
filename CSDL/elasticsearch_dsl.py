'''
Created on Feb 08, 2015

@author: jyadav
'''
import matplotlib.pyparsing as pp
import re
from pyelasticsearch.client import ElasticSearch
from pyelasticsearch.exceptions import  ElasticHttpNotFoundError
from matplotlib.pyparsing import *
import unittest
import sys
 
 
ELASTICSEARCH_INDEX = 'myindex'
ELASTICSEARCH_URL = 'http://localhost:9200/'
 
es = ElasticSearch(ELASTICSEARCH_URL)
 
 
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
        else:
            raise NotImplementedError('Only ":" comparisons are implemented.')
  

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
        #literals = pp.Group(number | numberList | string | word).setName("literals").addParseAction(self.validateLiterals)("lit")
        literals = (number | numberList | string | word).setName("literals").addParseAction(self.validateLiterals)("lit")
    
        # symbols
        identifier = pp.Regex(r"[a-z][a-z_]+(?:\.[a-z][a-z_]+)+").setName("identifier").addParseAction(self.validateIdentifier)("id")
        #identifier = word.setName("identifier").addParseAction(self.validateIdentifier)("id")
    
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


parser = ElasticSearchDSLParser()

def myDump(p1):
    for i in p1:
        print i, "--", len(i)
        try:
            #len(i) == 2 :
            if hasattr(i,"st") & (i[0]=="stream"):
                print i[0]," ",i[1]              
            elif hasattr(i, "ex")& (i[1]=="exists"):
                print i[0], i[1]
            elif (i in ("OR", "AND", "NOT")):
                print "Logical Op = ",i
            # for ParseElement with comp or no comp but has id, op and lit
            # This happens with OR and AND logic is added in the expression
            elif len(i) == 3:
                print "id = ",i.id
                print "op = ",i.op
                print "lit = ",i.lit              
            else:
                # for ParseElement with only comp but len > 3
                if hasattr(i,"comp"):  
                    myDump(i)
        except (IndexError, AttributeError), e:
            print e
 
def getQuery(str):
    parsed = parser.parseString(str).asList()
    #ast = parsed[0].get_query();
    if isinstance(parsed[0], ComparisonNode):
        lst = parsed
    else:
        lst = parsed[0]
            
    return {
            'bool': {
            'must': [node.get_query() for node in lst]
            }
    }
    
def performSearch(str):
    full_query = {
        'query': getQuery(str),
    }
    results = es.search(full_query, index=ELASTICSEARCH_INDEX, doc_type='lead')
    return results['hits']['hits']
    

class SearchTestCase(unittest.TestCase):
    def setUp(self):
        try:
            es.delete_index(ELASTICSEARCH_INDEX)
        except ElasticHttpNotFoundError:
            pass
 
        self.leads = [{
            "id": 1,
            "fb.company": "Facebook Inc.",
            "fb.contact": "Mark Zuckerberg",
            "fb.city": "Menlo Park",
            "tw.description": "an online networking site"
        }, {
            "id": 2,
            "ms.company": "Microsoft",
            "ms.contact": "Steve Ballmer",
            "ms.city": "Redmond",
            "tw.description": "software and online services"
        }]
 
        for lead in self.leads:
            es.index(ELASTICSEARCH_INDEX, 'lead', lead, lead['id'])
 
        # Wait for the search index to be generated.
        while es.status(ELASTICSEARCH_INDEX)['indices'][ELASTICSEARCH_INDEX]['docs']['num_docs'] < len(self.leads):
            import time
            time.sleep(1)
 
    def assertSearchMatch(self, str, matches):
        results = performSearch(str)
        self.assertEqual(set([int(r['_id']) for r in results]), set(matches))
 
    def test_search(self):
        self.assertSearchMatch('ms.company contains microsoft',[2])
        self.assertSearchMatch('fb.company contains Facebook',[1])
        self.assertSearchMatch('tw.description contains online',[1,2])
        self.assertSearchMatch('ms.company contains microsoft ms.city contains redmond' ,[2])
        self.assertSearchMatch('fb.company contains facebook fb.city contains park' ,[1])
        #parsed = parser.parseString('NOT twi.uy exists OR twi.uh <= [67,78] AND twi.ui >= 90 AND stream "as8e9j98838"')
        parsed = parser.parseString('twi.uh <= 56  twi.ui >= 90  tw.uu != 67')
        myDump(parsed.expr)
        '''
        self.assertSearchMatch('onl', [1, 2])
        self.assertSearchMatch('online', [1, 2])
        self.assertSearchMatch('online networking', [1])
        self.assertSearchMatch('company : microsoft', [2])
        self.assertSearchMatch('contact : microsoft', [])
        self.assertSearchMatch('"menlo park"', [1])
        self.assertSearchMatch('"park menlo"', [])
         '''
 

#parsed = parser.parseString('twitter.text contains "Cincinnati Reds"')
#assert parsed.asList() == [['twitter.text', 'contains', '"Cincinnati Reds"']]
#parsed = parser.parseString('NOT twi.uh <= 56 AND twi.ui >= 90 OR stream "jkdjd" AND twi.uy exists')
#parsed = parser.parseString('NOT twi.uy exists OR twi.uh <= [67,78] AND twi.ui >= 90 AND stream "as8e9j98838"')
#parsed = parser.parseString('twi.ui contains "microsoft"')
#parsed = parser.parseString('stream "as8e9j98838"')

#print parsed.expr[0].op , "--", parsed.expr[0].lit, "--", parsed.expr[0].id
#print parsed.asXML("Top")
#c,v = parser.flatten(parsed.asList())
#print c, " -- ", v
#print parsed.dump()
print '""""""'
#print parsed.dump()
#ast = parsed.asList()
#assert ast == [ComparisonNode(['twi.ui', 'contains', ['"microsoft"']])]
#query = ast[0].get_query()
#print query
#results = perform_search(query)


#myDump(parsed.expr)
    
#print parsed.asList ,len( parsed)
if __name__ == '__main__':
    unittest.main()
'''
print parsed.items
print parsed.asList
print parsed.asDict
print parsed.asXML
'''
            

