import sys
sys.path.append('../')
import utils.tools as tools
from typing import Any
import unittest

class TestSolution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=[
            tools.TestData(Solution(tools.mimicProcess('''987654321111111
811111111111119
234234234234278
818181911112111
'''
,mode='lines'),True),357,3121910778619)
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
        total_output=0
        
        for line in self.data:
            bank=list(map(int,list(line)))
            nonfinal=bank[:-1]
            first_digit=max(nonfinal)
            first_index=nonfinal.index(first_digit)
            second_digit=max(bank[first_index+1:])
            total_output+=first_digit*10 + second_digit
            
        return total_output
    def part_b(self):
        total_output=0
        for line in self.data:
            local_output=0
            bank=list(map(int,list(line)))
            rt=0
            last_index=-1
            for i in range(12):
                start=last_index+1
                end=len(bank)-11+i
                look=bank[start:end]
                
                next_digit=max(look)
                last_index=look.index(next_digit)+start
                local_output=local_output*10+next_digit
            total_output+=local_output
        return total_output
    
if __name__=='__main__':
    result=unittest.main(verbosity=1,exit=False).result
    if result.wasSuccessful():
        inp=tools.process('03')
        print('\n\n')
        sol=Solution(inp)
        tools.output(sol.part_a_solution,sol.part_b_solution)

