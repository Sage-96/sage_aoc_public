import sys
sys.path.append('../')
import utils.tools as tools
from typing import Any
import unittest

class TestSolution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=[
            tools.TestData(Solution(tools.mimicProcess('''

'''
,mode='lines'),True),None)
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
        
    def part_a(self):
        return None
    def part_b(self):
        return None
    
if __name__=='__main__':
    result=unittest.main(verbosity=1,exit=False).result
    if result.wasSuccessful():
        inp=tools.process('00')
        print('\n\n')
        sol=Solution(inp)
        tools.output(sol.part_a_solution,sol.part_b_solution)
