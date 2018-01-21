'''
Created on Mar 16, 2015

@author: irma
'''

import unittest

class levelPatterns(object):
    level_patterns=[]
    cutoff=None
    cutoff_counter=0


    def __init__(self,cutoff,level_patterns):
       self.level_patterns=level_patterns
       self.cutoff=cutoff
    
    def get_cutoff(self):
        self.cutoff_counter+=1
        return self.level_patterns[self.cutoff_counter*self.cutoff:(self.cutoff_counter*self.cutoff)+self.cutoff]
    
    
    
class Test_levelPatterns(unittest.TestCase): 
    example=[]
    for i in range(0,1600):
        example.append(i)
        
    obj=levelPatterns(400,example)
        
    def test_1(self):
        self.assertEqual(len(self.obj.get_cutoff()),400)
        self.assertEqual(self.obj.cutoff_counter, 1)
        self.assertEqual(len(self.obj.get_cutoff()),400)
        self.assertEqual(self.obj.cutoff_counter, 2)
        self.assertEqual(len(self.obj.get_cutoff()),400)
        self.assertEqual(self.obj.cutoff_counter, 3)
        self.assertEqual(len(self.obj.get_cutoff()),0)
            
    
    
    
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(Test_levelPatterns('test_1'))
    unittest.TextTestRunner().run(suite)
        