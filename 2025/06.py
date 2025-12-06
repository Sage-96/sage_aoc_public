import sys
sys.path.append('../')
import utils.tools as tools
from typing import Any
import unittest
from math import prod
class TestSolution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=[
            tools.TestData(Solution(tools.mimicProcess('''123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
'''
,mode='lines'),True),4277556,3263827)
            ]
    def test_part_a(self):
        for case in self.cases:
            self.assertEqual(case.data.part_a_solution,case.part_a_expected)
            
    def test_part_b(self):
        if set(map(lambda case:case.part_b_expected,self.cases))=={None}: self.skipTest("No part B")
        for case in self.cases:
            if case.part_b_expected!=None:
                self.assertEqual(case.data.part_b_solution,case.part_b_expected)
    
class Solution:
    def __init__(self, inp:Any,debug=False,skip_part_a=False,skip_part_b=False):
        self.data=inp
        
        if debug: self.debug=True
        else:self.debug=False
        self.part_a_solution=self.part_b_solution=None
        if self.debug:print('\033[96mDebugger On')
        self.process_data()
        if not skip_part_a:
            if self.debug:print('Part A:')
            self.part_a_solution=self.part_a()
        if not skip_part_b:
            if self.debug:print('\nPart B:')
            self.part_b_solution=self.part_b()
        if self.debug:print('\033[0m')
    
    def process_data(self):
        self.columns=[]
        width=max(map(len,self.data))
        empty=set(' ')
        last_empty=-1
        for c in range(width):
            if set([row[c] for row in self.data])==empty:
                self.columns.append([row[last_empty+1:c] for row in self.data])
                last_empty=c
        self.columns.append([row[last_empty+1:] for row in self.data])
        
    def part_a(self):
        self.processed_columns=[]
        for column in self.columns:
            column=list(map(lambda x:x.strip(),column))
            fxn=column[-1]
            data=map(int,column[:-1])
            self.processed_columns.append((data,fxn))
        
        grand_total=0
        for problem in self.processed_columns:
            if problem[1]=='+':
                grand_total+=sum(problem[0])
            else:
                grand_total+=prod(problem[0])
        return grand_total
    
        
        
    def part_b(self):
        self.processed_verticals=[]
        for column in self.columns:
            fxn=column[-1].strip()
            data=map(int,[''.join([cell[v] for cell in column[:-1]]).strip() for v in range(len(column[0]))])
            self.processed_verticals.append((data,fxn))
        grand_total=0
        for problem in self.processed_verticals:
            if problem[1]=='+':
                grand_total+=sum(problem[0])
            else:
                grand_total+=prod(problem[0])
        return grand_total
    
            
            
    
if __name__=='__main__':
    result=unittest.main(verbosity=1,exit=False).result
    if result.wasSuccessful():
        inp=tools.process('06')
        print('\n\n')
        sol=Solution(inp)
        tools.output(sol.part_a_solution,sol.part_b_solution)

