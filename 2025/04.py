import sys
sys.path.append('../')
import utils.tools as tools
from typing import Any
import unittest
import numpy as np

class TestSolution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=[
            tools.TestData(Solution(tools.mimicProcess('''..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
'''
,mode='array'),True),13,43)
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
        if not skip_part_a:
            if self.debug:print('Part A:')
            self.part_a_solution=self.part_a()
        if not skip_part_b:
            if self.debug:print('\nPart B:')
            self.part_b_solution=self.part_b()
        if self.debug:print('\033[0m')
    
    def generate_neighbormap(self,arr,count='@'):
        rows,cols=arr.shape
        neighbormap=np.zeros((rows,cols))
        
        for (r,c),_ in np.ndenumerate(arr):
            rt=0
            if r>0:
                rt+=(1 if arr[r-1,c]==count else 0)
                if c>0:
                    rt+=(1 if arr[r-1,c-1]==count else 0)
                if c<cols-1:
                    rt+=(1 if arr[r-1,c+1]==count else 0)
            if r<rows-1:
                rt+=(1 if arr[r+1,c]==count else 0)
                if c>0:
                    rt+=(1 if arr[r+1,c-1]==count else 0)
                if c<cols-1:
                    rt+=(1 if arr[r+1,c+1]==count else 0)
            if c>0:
                rt+=(1 if arr[r,c-1]==count else 0)
            if c<cols-1:
                rt+=(1 if arr[r,c+1]==count else 0)
            neighbormap[r,c]=rt
        return neighbormap.copy()
    
    def part_a(self):
        self.to_remove=[]
        neighbors=self.generate_neighbormap(self.data)
        for (r,c),char in np.ndenumerate(self.data):
            if char=='@' and neighbors[r,c]<4:
                self.to_remove.append((r,c))
        return len(self.to_remove)
    def part_b(self):
        running_total=len(self.to_remove)
        while self.to_remove:
            for spot in self.to_remove:
                self.data[spot]='.'
            running_total+=self.part_a()
        
        return running_total
    
if __name__=='__main__':
    result=unittest.main(verbosity=1,exit=False).result
    if result.wasSuccessful():
        inp=tools.process('04',mode='array')
        print('\n\n')
        sol=Solution(inp)
        tools.output(sol.part_a_solution,sol.part_b_solution)

