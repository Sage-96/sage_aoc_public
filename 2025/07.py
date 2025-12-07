import sys
sys.path.append('../')
import utils.tools as tools
from typing import Any
import unittest
from collections import defaultdict
from PIL import Image
import numpy as np

class TestSolution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=[
            tools.TestData(Solution(tools.mimicProcess('''.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
'''
,mode='lines'),True,make_gif=True),21,40)
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
    def __init__(self, inp:Any,debug=False,skip_part_a=False,skip_part_b=False,make_gif=False):
        self.data=inp
        self.make_gif=make_gif
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
        if self.make_gif:
            sequence=[]
            
            palette=[240,240,240,   204,76,76,   153,153,153,    242,178,204,   127,204,25]+([0]*(768-15))
            self.gif_map=np.full((len(self.data),len(self.data[0])),0,dtype='uint8')
            self.gif_map[0,self.data[0].find('S')]=1
            for x,row in enumerate(self.data):
                for y,char in enumerate(row):
                    if char=='^':
                        self.gif_map[x,y]=2
                       
            t=Image.fromarray(self.gif_map)
            t.putpalette(palette)
            t=t.resize((t.width*8,t.height*8),Image.NEAREST)
            sequence.append(t.copy())
            sequence.append(t.copy())
            sequence.append(t.copy())
            sequence.append(t.copy())
            sequence.append(t.copy())
            
        
        
        self.splitters_hit=[]
        self.beams=[tuple([self.data[0].find('S')])]
        for row in range(1,len(self.data)):
            row_beams=[]
            prev=self.beams[row-1]
            curr=self.data[row]
            for spot in prev:
                if curr[spot]=='^':
                    self.splitters_hit.append((row,spot))
                    row_beams.append(spot-1)
                    row_beams.append(spot+1)
                                 
                    if self.make_gif:
                        self.gif_map[row,spot-1]=3
                        self.gif_map[row,spot+1]=3
                        self.gif_map[row,spot]=4
                        t=Image.fromarray(self.gif_map)
                        t.putpalette(palette)
                        t=t.resize((t.width*8,t.height*8),Image.NEAREST)
                        sequence.append(t.copy())
                    
                else:
                    row_beams.append(spot)
                    if self.make_gif:
                        self.gif_map[row,spot]=3
                        t=Image.fromarray(self.gif_map)
                        t.putpalette(palette)
                        t=t.resize((t.width*8,t.height*8),Image.NEAREST)
                        sequence.append(t.copy())
                        
                        
                        
            self.beams.append(tuple(set(row_beams)))
            
            if self.make_gif:
                sequence.append(t.copy())
                sequence.append(t.copy())
            
        self.splitters_hit=tuple(set(self.splitters_hit))
        
        if self.make_gif:
            sequence[0].save(f'day_7.gif',
               save_all = True, append_images = sequence[1:],
               optimize = False, duration = 16,loop=1)
            
        return len(self.splitters_hit)
                    
                
            
    def part_b(self):
        self.power_b=defaultdict(int)
        self.beams_b=[tuple([self.data[0].find('S')])]
        self.power_b[(0,self.data[0].find('S'))]=1
        
        for row in range(1,len(self.data)):
            row_beams=[]
            prev=self.beams_b[row-1]
            curr=self.data[row]
            
            for spot in prev:
                
                if curr[spot]=='^':
                    
                    self.power_b[(row,spot-1)]+=self.power_b[(row-1,spot)]
                    self.power_b[(row,spot+1)]+=self.power_b[(row-1,spot)]
                    
                    row_beams.append(spot-1)
                    row_beams.append(spot+1)
                else:
                    self.power_b[(row,spot)]+=self.power_b[(row-1,spot)]
                    row_beams.append(spot)
            
            self.beams_b.append(tuple(set(row_beams)))
        end_row_powers=[v for (k,v) in self.power_b.items() if k[0]==len(self.data)-1 ]
        return sum(end_row_powers)
    
if __name__=='__main__':
    result=unittest.main(verbosity=1,exit=False).result
    if result.wasSuccessful():
        inp=tools.process('07')
        print('\n\n')
        sol=Solution(inp,make_gif=False,skip_part_b=False)
        tools.output(sol.part_a_solution,sol.part_b_solution)

