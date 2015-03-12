'''
Created on Feb 21, 2015

@author: jyadav
'''
import unittest

from pyelasticsearch.client import ElasticSearch
from pyelasticsearch.exceptions import ElasticHttpNotFoundError
from BigDataQueryLanguage.Parser.QueryParser import *
from BigDataQueryLanguage.ESPercolator.Percolator import *
from BigDataQueryLanguage.Domain.ConsolidatedObject import *

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

def getAllQueries():
    queries = [{
            'id': 'stream8838',
            'query': {'query': {'match': {'source':'sinawebo'}}}
        },{
            'id': 'stream1893',
            'query': {'query': {'match': {'keyword':'microsoft'}}}
        },{
            'id': 'stream6893',
            'query': {'query': {'match': {'source_language':'Menlo Park'}}}
        },{
            'id' : 'stream5676',
            'query': getFullQuery('source contains sinawebo source_language contains park')
        },{
            'id': 'stream3453',
            'query': {'query': {'bool': {'must' : [{'match_phrase':{'source':'sinawebo'}},{'match_phrase':{'source_language':'Menlo Park'}}]}}}
        },
        ]
    return queries;


def getAllJSONTestDocs():
    testDocs = [{
               'doc' : {'source': 'sinawebo', 'not_available': 'junk'},
               'streams' : ['stream8838']               
               },{
               'doc' : {'keyword': 'microsoft'},
               'streams' : ['stream1893']
               },{
               'doc' : {'source': 'serendio'},
               'streams' : []
               },{
               'doc' : {'source': 'sinawebo','source_language':"Menlo Park"},
               'streams' : ['stream8838','stream6893','stream3453','stream5676']
               },{
               'doc' : {'keyword': 'microsoft','source': 'sinawebo'},
                'streams' : ['stream8838','stream1893']
                }]
    return testDocs

def getConsoldiateObjectDoc():
    co = ConsolidatedDocument()
    co.source = 'sinawebo'
    co.keyword = 'microsoft'
    co.source_language = 'park'
    
    doc = {'doc':co,
           'streams':['stream8838','stream1893','stream6893','stream5676']}
    
    return doc

# Define all the field types
def getMapping():
    # this is where the data dictionary goes
    mapping =  {
                'co-type' : {'properties' :
                              {'source' : {'type' : 'string'},
                               'keyword' : {'type' : 'string'},
                               'source_language' : {'type' : 'string'},                                }
                               }
                }
    return mapping
                
class KafkaConsolidateObjectTestCase(unittest.TestCase):
        
    def setUp(self):
        percolator.deleteIndex(ELASTICSEARCH_INDEX)
        percolator.createIndex(ELASTICSEARCH_INDEX)
        
        #test-type as doc type
        percolator.putMapping(ELASTICSEARCH_INDEX, 'co-type' , getMapping()) 

        #Get All the queries to be indexed
        allQueries = getAllQueries()
        
        # index all the queries
        for q in allQueries:
            print 'put: ',percolator.indexPercolate(ELASTICSEARCH_INDEX, q['query'], q['id'])            

        # Wait for the search index to be generated.
        percolator.waitTillReady(ELASTICSEARCH_INDEX, len(allQueries));
        
    def tearDown(self):
        percolator.deleteIndex(ELASTICSEARCH_INDEX)

    def assertSearchMatch(self, results, streams):
        self.assertEqual(set([(r['_id']) for r in results]), set(streams))

    def testSerach(self):
        doc = getConsoldiateObjectDoc()
        results = percolator.search(ELASTICSEARCH_INDEX, 'lead1', doc)
        self.debug(results, doc)
        self.assertSearchMatch(results['matches'], doc['streams'])
                      
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