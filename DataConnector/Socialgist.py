'''
Created on Feb 15, 2015

@author: jyadav
'''
import sys

import requests
import json

print sys.path
s = requests.Session()
js_list = []
tweets = []

def streaming():    
    req = requests.Request("GET",'https://emotodata.socialgist.com/stream/sinaweibo_main/subscription/main/part/1/data.json').prepare()
    resp = s.send(req, stream=True)

    for line in resp.iter_lines():
        if line:
            yield line
        
def readStream():
    for i,line in enumerate(streaming()):
        js_list.append(line)
        if i == 5:
            return js_list

print readStream()[0]

'''   
 def writeJson(js):
    
    with open("sample_stream.txt",'w') as f:
        for j in js:
            f.write(j)        
def parseJson(single_json):
    #TODO
    pass
'''

