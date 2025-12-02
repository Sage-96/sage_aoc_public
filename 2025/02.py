import sys
sys.path.append('../')
import utils.tools as tools
from typing import Any
import unittest
import re


class TestSolution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=[
            tools.TestData(Solution(tools.mimicProcess('''11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
'''
,mode='split',splitval=','),True),1227775554,4174379265)
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
        invalid_sum=0
        for chunk in self.data:
            l,r=chunk.split('-')
            l=int(l)
            r=int(r)
            for value in range(l,r+1):
                v=str(value)
                first,second=tools.split_on(v,len(v)//2)
                if first==second:
                    invalid_sum+=value
                
                
        return invalid_sum
    def part_b(self):
        rep_seq=re.compile(r'(\d+?)\1+')
        invalid_sum=0
        for chunk in self.data:
            l,r=chunk.split('-')
            l=int(l)
            r=int(r)
            for value in range(l,r+1):
                v=str(value)
                if rep_seq.fullmatch(v):
                    invalid_sum+=value
        return invalid_sum
    
if __name__=='__main__':
    result=unittest.main(verbosity=1,exit=False).result
    if result.wasSuccessful():
        inp=tools.process('02',mode='split',splitval=',')
        print('\n\n')
        sol=Solution(inp)
        tools.output(sol.part_a_solution,sol.part_b_solution)

