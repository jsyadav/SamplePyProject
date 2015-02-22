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
    
def getFullQuery(str):
    full_query = {
        'query': getBoolQuery(str),
    }
    return full_query

class Test(unittest.TestCase):

    def createQueries(self,str):
        print getFullQuery(str)
        

    def setUp(self):
        percolator.deleteIndex(ELASTICSEARCH_INDEX)
        percolator.createIndex(ELASTICSEARCH_INDEX)
        
        mapping =  {
                    'test-type' : {'properties' :
                                  {'tw.company' : {'type' : 'string'}}
                                  }
                    }
        
        percolator.putMapping(ELASTICSEARCH_INDEX, 'test-type' , mapping) #test-type as doc type
        
        
        self.leads = [{
            'id': 'stream8838',
            'query': {'query': {'match': {'tw.company':'facebook'}}}
        },{
            'id': 'stream1893',
            'query': {'query': {'match': {'tw.company':'microsoft'}}}
        },]
        
        
        for lead in self.leads:
            print 'put: ',percolator.indexPercolate(ELASTICSEARCH_INDEX, lead['query'], lead['id'])     
       

        # Wait for the search index to be generated.
        percolator.waitTillReady(ELASTICSEARCH_INDEX, len(self.leads));
        
    def tearDown(self):
        pass


    def testSerach(self):
        docs = [{
               'doc' : {
                'tw.company': 'facebook'
                }
               },{
               'doc' : {
                'tw.company': 'microsoft'
                }
               },{
               'doc' : {
                'tw.company': 'serendio'
                }}]
                  
        for doc in docs:
            print 'search : ',percolator.search(ELASTICSEARCH_INDEX, 'lead1', doc)     
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()