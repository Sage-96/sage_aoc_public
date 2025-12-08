import sys
sys.path.append('../')
import utils.tools as tools
from typing import Any
import unittest
from itertools import combinations
from math import sqrt,prod
import datetime
class TestSolution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=[
            tools.TestData(Solution(tools.mimicProcess('''162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
'''
,mode='linesplit',splitval=',',ints=True),True),40,25272)
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
        self.data=list(map(tuple,self.data))
        
        self.distances={}
        self.networks={k:set([k]) for k in self.data}
        
        def distance(a,b):
            return sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2 + (b[2]-a[2])**2)
        
        for (a,b) in combinations(self.data,2):
            self.distances[(a,b)]=distance(a,b)
        
        
        
        
    def part_a(self):
        self.dist=self.distances.copy()
        i=1000
        if self.debug:i=10
        
        for _ in range(i):
            if not _%500:print(_)
            (a,b) = min(self.dist,key=self.dist.get)
            if self.debug:print(f'{a} <-> {b}')
            if a not in self.networks[b]:
                comb=self.networks[a]|self.networks[b]
                for spot in comb:
                    self.networks[spot]=comb
            del(self.dist[(a,b)])
        self.nw=[]
        for v in self.networks.values():
            if v not in self.nw:self.nw.append(v)
        return prod(sorted(list(map(len,self.nw)),reverse=True)[:3])
        
                
            
        
    def part_b(self):
        i=1000
        if self.debug:i=10
        
        while len(self.networks[self.data[0]])<len(self.data):
            if not i%500:print(i)
            (a,b) = min(self.dist,key=self.dist.get)
            if a not in self.networks[b]:
                comb=self.networks[a]|self.networks[b]
                for spot in comb:
                    self.networks[spot]=comb
            del(self.dist[(a,b)])
            i+=1
        return a[0]*b[0]
            
    
if __name__=='__main__':
    #Timing this one just because
    start=datetime.datetime.now().timestamp()
    
    result=unittest.main(verbosity=1,exit=False).result
    if result.wasSuccessful():
        inp=tools.process('08',mode='linesplit',splitval=',',ints=True)
        print('\n\n')
        sol=Solution(inp)
        tools.output(sol.part_a_solution,sol.part_b_solution)

    end=datetime.datetime.now().timestamp()
    delta=int(end-start)
    print(f'{delta} seconds')
    #161 seconds
    