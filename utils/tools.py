import numpy as np
import warnings
from typing import Any,List,Tuple
from dataclasses import dataclass
from numbers import Number
from math import inf

"""
import sys
sys.path.append('../')
import utils.tools as tools
"""

@dataclass
class TestData:
    data:Any
    part_a_expected:Any
    part_b_expected:Any=None

    
def process(day,mode='lines',splitval='',ints=False):
    with open(str(day)+'.txt') as inputVals:
        if mode=='lines':
            inp=inputVals.read().splitlines()
            if ints: inp=list(map(int,inp))
            
        elif mode=='split':
            inp=inputVals.read().split(splitval)
            if ints: inp=list(map(int,inp))
            if not ints and inp[-1][-1:]=='\n':
                inp[-1]=inp[-1][:-1]
        elif mode=='linesplit':
            inp=inputVals.read().splitlines()
            inp=list(map(lambda line:line.split(splitval),inp))
            if ints:
                inp=list(map(lambda sublist: list(map(int,sublist)),inp))

        elif mode=='chars':
            inp=inputVals.read()
            return [v for v in inp]
        
        elif mode=='chunk':
            inp=list(map(str.splitlines,inputVals.read().split('\n\n')))
            if ints:
                for i,line in enumerate(inp):
                    inp[i]=list(map(int,line))
            
        elif mode=='array':
            lines=inputVals.read().splitlines()
            width=max(list(map(len,lines)))
            height=len(lines)
            inp=np.full((height,width),None)
            for row in range(height):
                line=lines[row]
                for col in range(len(line)):
                    inp[row,col]=line[col]
            if ints: inp=inp.astype(int)
            
        elif mode=='raw':
            inp=inputVals.read().strip()
            
        
    return inp
def mimicProcess(data,mode='lines',splitval='',ints=False):
    if mode=='lines':
        inp=data.splitlines()
        if ints: inp=list(map(int,inp))
            
    elif mode=='split':
        inp=data.split(splitval)
        if ints: inp=list(map(int,inp))
        if not ints and inp[-1][-1:]=='\n':
                inp[-1]=inp[-1][:-1]
    elif mode=='linesplit':
        inp=data.splitlines()
        inp=list(map(lambda line:line.split(splitval),inp))
        if ints:
            inp=list(map(lambda sublist: list(map(int,sublist)),inp))
            

    elif mode=='chars':
        inp=data
        return [v for v in inp]
    
    elif mode=='chunk':
        inp=list(map(str.splitlines,data.split('\n\n')))
        if ints:
            for i,line in enumerate(inp):
                inp[i]=list(map(int,line))
        
                
    elif mode=='array':
        
        lines=data.splitlines()
        width=max(list(map(len,lines)))
        height=len(lines)
        inp=np.full((height,width),None)
        for row in range(height):
            line=lines[row]
            for col in range(len(line)):
                inp[row,col]=line[col]
        if ints: inp=inp.astype(int)
    else:inp=None
    return inp

def output(partA,partB=None):
    print(f'Part 1: {partA}')
    if partB:
        print(f'Part 2: {partB}')


def columnExtract(lst:list,pos:int) -> list:
    return [x[pos] for x in lst]

def columnReplace(lst:list,col:list|str,pos:int) -> None:
    ##RUNS ON EXISTING LIST
    for r,v in enumerate(col):
        lst[r][pos]=v
        
def columnInject(lst:list,col:list|str,pos:int) -> None:
    ##RUNS ON EXISTING LIST
    if type(col)==str:col=list(col)
    for r,v in enumerate(col):
        row=lst[r][:pos]
        row.append(v)
        row+=lst[r][pos:]
        lst[r]=row

def columnRemove(lst:list,pos:int) -> None:
    ##RUNS ON EXISTING LIST
    for r in range(len(lst)):
        row=lst[r][:pos]+lst[r][pos+1:]
        lst[r]=row

def cycleBack(lst:list) -> None:
    ##RUNS ON EXISTING LIST
    t=lst[0]
    lst[:-1]=lst[1:]
    lst[-1]=t

def cycleForward(lst:list) -> None:
    ##RUNS ON EXISTING LIST
    t=lst[-1]
    lst[1:]=lst[:-1]
    lst[0]=t

def transpose(lst,string=False):
    transposed=[]
    for c in range(len(lst[0])):
        transposed.append(columnExtract(lst,c))
    if string:
        transposed=list(map(lambda x:''.join(x),transposed))
    return transposed

def wildcardSub(pattern,wildcardChar,substitutes)->list:
    patterns=[]
    
    if wildcardChar in pattern:
        subs=[]
        for sub in substitutes:
            if wildcardChar in sub:
                warnings.warn(f"Wildcard character in substitute {sub}. Ignoring value.")
                substitutes.remove(sub)
                continue
            subs.append(pattern.replace(wildcardChar,sub,1))
        for p in subs:
            patterns+=wildcardSub(p,wildcardChar,substitutes)
    else:
        patterns.append(pattern)
    return patterns if type(patterns)==list else [patterns]

def othersDict(lst:list)->dict:
    dct={}
    for element in lst:
        l=list(lst).copy()
        l.remove(element)
        dct[element]=l
    return dct
    
def show(array:np.ndarray|list,file=False,filename:str ='show_array.txt') -> None:
    if not file:
        for line in array:
            print(''.join(list(map(str,line))))
        print('\n')
    else:
        out=''
        for line in array:
            out+=(''.join(list(map(str,line))))+'\n'
        with open(filename,'w',encoding='locale') as openFile:
            openFile.write(out)
    
def subdivide(size:int) -> list[int]:
    groups=[]
    for i in range(1,size//2+1):#Number of dividing lines
        if (size-i) % (i+1)==0:
            groups.append((size-i)//(i+1))#Size of groups
    return groups
    
def str_to_bool(value:str) -> bool:
    value=value.lower().capitalize()
    if value=='True':return True
    else:return False

def split_on(value:str,split:int) ->tuple[str,str]:
    if not isinstance(value,str):raise TypeError("can only be used on 'str' objects")
    if not isinstance(split,int):raise TypeError("can only split on an integer")
    return (value[:split],value[split:])

def sign(value:int) -> int:
    if value==0:return 0
    else: return value//abs(value)
    
def neighbors(cell:tuple[int,int],shape:tuple[int,int],corners=False)-> list[tuple[int,int]]:
    
    x,y=cell
    rows,cols=shape
    
    neighbors=[]
    if x>0:neighbors.append((x-1,y))
    if x<rows-1:neighbors.append((x+1,y))
    if y>0:neighbors.append((x,y-1))
    if y<cols-1:neighbors.append((x,y+1))
    if corners:
        if x>0 and y>0:neighbors.append((x-1,y-1))
        if x>0 and y<cols-1:neighbors.append((x-1,y+1))
        if x<rows-1 and y>0:neighbors.append((x+1,y-1))
        if x<rows-1 and y<cols-1:neighbors.append((x+1,y+1))
    
    return neighbors

class RangeMap:
    def __init__(self,default:Any=None,presets:List[Tuple[Number,Number,Any]]=None):
        self.map={-inf:default}
        if presets:
            for start,end,value in presets:
                self.set_range(start,end,value)
            
    def __getitem__(self,arg:Number):
        if not isinstance(arg,Number):
            raise TypeError("RangeMap indices must be numbers.")
        key=max([k for k in self.map.keys() if k<=arg])
        return self.map[key]
    
    def set_range(self,start:Number,end:Number,value:Any,mode='override'):
        prev_upper_key=k=max([k for k in self.map.keys() if k<=end])
        prev_upper_val=self.map[prev_upper_key]
        self.map[end]=prev_upper_val
        self.map[start]=value
        for key in [k for k in self.map.keys() if k>start and k<end]:
            del self.map[key]
    
        
    

directions={0:(-1,0),1:(0,1),2:(1,0),3:(0,-1)}##U,R,D,L




if __name__=='__main__':
    print(subdivide(38))
    
