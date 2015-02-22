'''
Created on Feb 21, 2015

@author: jyadav
'''

from pyelasticsearch.client import ElasticSearch
from pyelasticsearch.exceptions import ElasticHttpNotFoundError

PERCOLATOR = ".percolator" #must don't change

class PercolatorQuery(object):
    def __init__(self):
        self.es = ElasticSearch()     
        
    def createIndex(self, _idx):
        return self.es.create_index(_idx)
        
    def putMapping(self,_idx, _type, _mapping):
        self.es.put_mapping(_idx, _type, _mapping)
    
    def deleteIndex(self,_idx):
        try:
            self.es.delete_index(_idx)
        except ElasticHttpNotFoundError:
            pass
        
    def indexPercolate(self,_idx, _doc, _id):
        return self.es.index(index=_idx, doc_type=PERCOLATOR, doc=_doc, id=_id)
        
    
    def waitTillReady(self,_idx,_count):
        while self.es.status(_idx)['indices'][_idx]['docs']['num_docs'] < _count:
            import time
            time.sleep(1)
            
    def search(self, _idx, _doc_type, _doc):
        return self.es.percolate(index=_idx, doc_type=_doc_type, doc=_doc)