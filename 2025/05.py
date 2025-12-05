import sys
sys.path.append('../')
import utils.tools as tools
from typing import Any
import unittest

class TestSolution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=[
            tools.TestData(Solution(tools.mimicProcess('''3-5
10-14
16-20
12-18

1
5
8
11
17
32
'''
,mode='chunk'),True),3,14)
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
        self.setup()
        if not skip_part_a:
            if self.debug:print('Part A:')
            self.part_a_solution=self.part_a()
        if not skip_part_b:
            if self.debug:print('\nPart B:')
            self.part_b_solution=self.part_b()
        if self.debug:print('\033[0m')
        
    def setup(self):
        self.fresh=tools.RangeMap(False)
        
        self.ranges, self.ingredients=self.data
        self.ingredients=list(map(int,self.ingredients))
        
        for line in self.ranges:
            l,r=map(int,line.split('-'))
            self.fresh.set_range(l,r+1,True)
        
        
    def part_a(self):
        fresh_count=0
        for ingr in self.ingredients:
            fresh_count+=(1 if self.fresh[ingr] else 0)
        return fresh_count
            
    def part_b(self):
        total_fresh=0
        fresh_openers=sorted([k for k,v in self.fresh.map.items() if v==True])
        closers=[k for k,v in self.fresh.map.items() if v==False]
        while fresh_openers:
            op=fresh_openers.pop(0)
            closers=[v for v in closers if v>op]
            cl=min(closers)
            total_fresh+=(cl-op)
            fresh_openers=[v for v in fresh_openers if v>cl]
        
        
        return total_fresh
    
if __name__=='__main__':
    result=unittest.main(verbosity=1,exit=False).result
    if result.wasSuccessful():
        inp=tools.process('05',mode='chunk')
        print('\n\n')
        sol=Solution(inp)
        tools.output(sol.part_a_solution,sol.part_b_solution)

