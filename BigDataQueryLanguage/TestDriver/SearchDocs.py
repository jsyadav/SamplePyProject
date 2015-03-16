'''
Created on Mar 1, 2015

@author: jyadav
'''

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
 
 
class TextNode(Node):
    def get_query(self, field='_all'):
        return {
            'term': {
                 field: self[0]
                 }
             }
 
class ExactNode(Node):
    def get_query(self, field='_all'):

        return {
            'term': {
                 field: self[0]
             }
        }
 
class ComparisonNode(Node):
    def get_query(self):
        field = self[0]
        op = self[1]
        node = self[2]
 
        if op == ':' or op =='==':
            return node.get_query(field)
        else:
            raise NotImplementedError('Only ":" comparisons are implemented.')

class UnaryNode(Node):
    def get_query(self):
        return   {
            self[0] : self[1].get_query()
                }

class BinaryNode(Node):
    def get_query(self):        
        l2 = self[1::2]
        prev = self[0].get_query()
        j = 0
        for i in range(0,len(l2)):
            l = list()
            l.append(prev)
            l.append(self[j+2].get_query())
            prev = {self[j+1]:l}   
            j += 2     
        return prev
 
 
unicode_printables = u''.join(unichr(c) for c in xrange(65536)
                                        if not unichr(c).isspace())
 
word = TextNode.group(Word(unicode_printables))
exact = ExactNode.group(QuotedString('"', unquoteResults=True, escChar='\\'))
number = Regex(r"[+-]?\d+(:?\.\d*)?(:?[eE][+-]?\d+)?").setName("number")
numberList = Group(Literal('[') + number + ZeroOrMore("," + number) + Literal(']')).setName("numberList")
term = exact | word | number | numberList

comparison_name = Word(unicode_printables)
operator = Regex(r":|<=|>=|<>|\!=|==|<|>|not|in|regex_partial|regex_exact|geo_box|"+
                "geo_radius|geo_polygon|contains_any|substr|contains_near|any|contains_substr|near|"+
                "contains")

comparison = ComparisonNode.group(comparison_name + operator + term)
unary = UnaryNode.group('not' + comparison)
andOr = CaselessLiteral('and') | CaselessLiteral('or')

andOrN = BinaryNode.group(comparison+ OneOrMore(andOr + comparison ))    
content = OneOrMore(unary | andOrN | comparison | term )

    
def get_query(search_query):
    nodes = content.parseString(search_query, parseAll=True).asList()
    print nodes
    return {
        'bool': {
            'must': [node.get_query() for node in nodes]
        }
    }
    
def getQuery(str):
    print "Expr => ",str
    nodes = content.parseString(str, parseAll=True).asList()
    print "Parsed => ", nodes

    return {
        'filtered': {
            'filter': [node.get_query() for node in nodes]
        }
    }
def getQueryString(str):
    queries = [ {
        "match" : {
            "description" : {
                "query" : "an online test",
                "operator" : "or"
            }
               }
                 },{
        'bool' : {
            'must'  :[{'match_phrase' : {'description' : 'an online '}},{'match_phrase' : {'city' : "Menlo Park"}}]
            }
                },{               
        'filtered' :{"query" : {
            "match_all" : { }
                },
                    'filter': {'not': {'term': {'company': 'Microsoft'}}}}

                        },{               
        'filtered' :{
                    'filter': {'term': {'company' : 'Microsoft'}}}

                        },{               
        'filtered' :{"query" : {
            "match_all" : { }
                },
                    'filter': {'term' : {'id' : 2}}}

                        },{
        "filtered" : {
            "filter" : {
                "exists" : { "field" : "contact" }
                }
                            }
                           },{
        "filtered" : {
            "filter" :  {'not' : {"filter":{
                "exists" : { "field" : "contact" }
                }
                                  }
                            }}
                           }, 
               
                   ]
    return queries

def perform_search(search_query):
    #full_query = {'query': get_query(search_query),}
    #full_query = {'query': getQueryString(search_query)[2],}
    full_query = {'query': getQuery(search_query)}
    
    print "Query => ", full_query
    results = es.search(full_query, index=ELASTICSEARCH_INDEX, doc_type='lead')
    return results['hits']['hits']

class QueryGenerationTestCase():
    def test_parse(self):
        search_query = 'not contact : microsoft'
        nodes = content.parseString(search_query, parseAll=True).asList()
        for node in nodes:
            print node.get_query()
    

    

 
class SearchTestCase(unittest.TestCase):
    def setUp(self):
        try:
            es.delete_index(ELASTICSEARCH_INDEX)
        except ElasticHttpNotFoundError:
            pass
 
        self.leads = [{
            "id": 1,
            "company": "Facebook Inc. ",
            "contact": "Mark Zuckerberg",
            "city": "Menlo Park",
            "description": "an online networking site"
        }, {
            "id": 2,
            "company": "Microsoft",
            "contact": "Steve Ballmer",
            "city": "Redmond",
            "description": "software and online services"
        }]
      
        es.create_index('myindex')
        mapping =  {
                'lead' : {'properties' :
                              {'company' : {'type' : 'string',"index":"not_analyzed"},
                               'city' : {'type' : 'string',"index":"not_analyzed"},
                               'contact' : {'type' : 'string',"index":"not_analyzed"},
                               'id' : {'type' : 'float',"index":"not_analyzed"},
                               }
                }}
                    
        es.put_mapping('myindex', 'lead', mapping)
        for lead in self.leads:
            es.index('myindex', 'lead', lead, lead['id'])
            
 
        # Wait for the search index to be generated.
        while es.status(ELASTICSEARCH_INDEX)['indices'][ELASTICSEARCH_INDEX]['docs']['num_docs'] < len(self.leads):
            import time
            time.sleep(1)
 
    def assertSearchMatch(self, query, matches):
        results = perform_search(query)
        self.assertEqual(set([int(r['_id']) for r in results]), set(matches))
 
    def test_search(self):
        '''
        self.assertSearchMatch('onl', [1, 2])
        self.assertSearchMatch('online', [1, 2])
        self.assertSearchMatch('online networking', [1])
        self.assertSearchMatch('company : microsoft', [2])
        self.assertSearchMatch('contact : microsoft ', [])
        self.assertSearchMatch('"menlo park"', [1])
        self.assertSearchMatch('"park menlo"', [])
        '''
        exprQueries = ['company == Microsoft',
                      'city : Redmond and company : Microsoft',
                      'contact : \"Mark Zuckerberg\" and company : \"Facebook Inc. \"',
                      'contact == \"Mark Zuckerberg\" and company == \"Facebook Inc. \" and city == \"Menlo Park\"',
                      'contact == \"Mark Zuckerberg\" and company == \"Facebook Inc. \" and city == \"Menlo Park\" and id == 2',
                      'city : Redmond or company : Facebook',    
                      'contact : \"Mark Zuckerberg\" or company : \"Facebook Inc. \"',
                      'contact == \"Mark Zuckerberg\" or company == \"Facebook Inc. \" or city == \"Menlo Park\"',
                      'contact == \"Mark Zuckerberg\" or company == \"Facebook Inc. \" or city == \"Menlo Park\" and id == 2',  
                      'not company == Microsoft',                   
                      ]
        for s in exprQueries:
            res = perform_search(s)
            print "Result => ",res, "\n"
        
if __name__ == '__main__':
    #print sys.path
    unittest.main()