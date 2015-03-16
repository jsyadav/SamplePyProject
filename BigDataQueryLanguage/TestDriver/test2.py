'''
Created on Mar 15, 2015

@author: jyadav
'''

if __name__ == '__main__':
    l1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    l2 = l1[1::2]
    print l2 
    print len(l2) 
    
    prev = 0
    for i in l2:
        print i
        l = list()
        l.append(prev)
        l.append(i+1)
        prev = {i:l}        
        print prev