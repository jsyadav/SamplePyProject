'''
Created on Feb 21, 2015

@author: jyadav
'''
import unittest

from pyelasticsearch.client import ElasticSearch
from pyelasticsearch.exceptions import ElasticHttpNotFoundError
from BigDataQueryLanguage.Parser.QueryParser import *
from BigDataQueryLanguage.ESPercolator.Percolator import *

ELASTICSEARCH_INDEX = 'myindex'
ELASTICSEARCH_URL = 'http://localhost:9200/'
 

parser = ElasticSearchDSLParser()
percolator = PercolatorQuery()


def getBoolQuery(str):
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
    
# Get the AST for this expression
def getFullQuery(str):
    full_query = {
        'query': getBoolQuery(str),
    }
    return full_query

class ParserTestCase(unittest.TestCase):

    def createQueries(self,str):
        print getFullQuery(str)
        
    def testSearch(self):
        #self.createQueries('twi.uh <= 56  twi.ui >= 90  tw.uu != 67')
        self.createQueries('tw.company contains facebook tw.city contains park')
    
class SimpleTestCase(unittest.TestCase):
        
    def setUp(self):
        percolator.deleteIndex(ELASTICSEARCH_INDEX)
        percolator.createIndex(ELASTICSEARCH_INDEX)
        
        # Define all the field types
        # this is where the data dictionary goes
        mapping =  {
                    'test-type' : {'properties' :
                                  {'tw.company' : {'type' : 'string'},
                                   'tw.city' : {'type' : 'string'},
                                   'tw.contact' : {'type' : 'string'},
                                   'tw.description' : {'type' : 'string'}
                                  }
                                  }
                    }
        
        percolator.putMapping(ELASTICSEARCH_INDEX, 'test-type' , mapping) #test-type as doc type
        
        
        self.leads = [{
            'id': 'stream8838',
            'query': {'query': {'match': {'tw.company':'facebook'}}}
        },{
            'id': 'stream1893',
            'query': {'query': {'match': {'tw.company':'microsoft'}}}
        },{
            'id': 'stream6893',
            'query': {'query': {'match': {'tw.city':'Menlo Park'}}}
        },{
            'id' : 'stream5676',
            'query': getFullQuery('tw.company contains facebook tw.city contains park')
        },{
            'id': 'stream3453',
            'query': {'query': {'bool': {'must' : [{'match_phrase':{'tw.company':'facebook'}},{'match_phrase':{'tw.city':'Menlo Park'}}]}}}
        },{
            'id': 'stream4453',
            'query': getFullQuery('tw.contact contains "Mark Zuckerberg" tw.description contains "an online networking site"')
        },{
            'id': 'stream2353',
            'query': getFullQuery('tw.contact contains "Mark Zuckerberg"')
        },]
        
        
        for lead in self.leads:
            print 'put: ',percolator.indexPercolate(ELASTICSEARCH_INDEX, lead['query'], lead['id'])     
       

        # Wait for the search index to be generated.
        percolator.waitTillReady(ELASTICSEARCH_INDEX, len(self.leads));
        
    def tearDown(self):
        percolator.deleteIndex(ELASTICSEARCH_INDEX)

    def assertSearchMatch(self, results, streams):
        self.assertEqual(set([(r['_id']) for r in results]), set(streams))

    def testSerach(self):
        docs = [{
               'doc' : {
                'tw.company': 'facebook',
                'streams' : ['stream8838']
                }
               },{
               'doc' : {
                'tw.company': 'microsoft',
                'streams' : ['stream1893']
                }
               },{
               'doc' : {
                'tw.company': 'serendio',
                'streams' : []
                }
               },{
               'doc' : {
                'tw.company': 'facebook','tw.city':"Menlo Park",
                'streams' : ['stream8838','stream6893','stream3453','stream5676']
                }
               },{
               'doc' : {
                'tw.contact': "Mark Zuckerberg",'tw.description':"an online networking site",
                'streams' : ['stream4453','stream2353']
                }
               },{
               'doc' : {
                'tw.city': 'park','tw.company': 'microsoft',
                'streams' : ['stream6893','stream1893']
                }}]
                  
        for doc in docs:
            results = percolator.search(ELASTICSEARCH_INDEX, 'lead1', doc)
            self.debug(results, doc)
            self.assertSearchMatch(results['matches'], doc['doc']['streams'])
            
    def debug(self,results,doc):   
        print results 
        
        if len(results['matches']):
            for match in results['matches']:
                print "found stream id ", match['_id'], " for doc ",doc
        else:
            print 'No match found for doc ', doc
                


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()