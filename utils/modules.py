class Computer:  
    def __init__(self,code,name='Computer',debug=0,inputRequestMessages=0):
        from collections import defaultdict
        self.name=name
        
        self.orig=defaultdict(int)
        self.processCode(code)
        self.code=self.orig.copy()
        
        self.debug=debug
        if self.debug==True:self.debug=1
        if self.debug==False:self.debug=0
        self.pointer=0
        self.isStopped=False
        self.isFinished=False
        self.output=[]
        self.awaitingInput=False
        self.rb=0
        self.ioReq=inputRequestMessages
        
    def reset(self):
        self.code=self.orig.copy()
        self.pointer=0
        self.isStopped=False
        self.isFinished=False
        self.output=[]
        self.awaitingInput=False
        self.rb=0
    
    def processCode(self,code):
        for i,c in enumerate(code):
            self.orig[i]=c
        return    
    
    def difference(self):
        for i in range(len(self.code)):
            if self.code[i]!= self.orig[i]: print(f'''{self.name} - Difference at index {i}:\r
Original Value {self.orig[i]}    Current Value {self.code[i]}\n''')
        
    def toStop(self):
        if self.awaitingInput:
            print(f'{self.name} - Awaiting input: Not Continuing')
            return
        self.isStopped=False
        while not (self.isStopped or self.isFinished):
            self.runCommand()
            if self.debug>1:self.isStopped=True
    
    def setValue(self,index,value):
        self.code[index]=value

    def setPointer(self,value):
        self.pointer=value
        
    def nextValue(self):
        nxt = self.code[self.pointer]
        self.pointer+=1
        return nxt
    
    def decodeC(self,intcode):
        return intcode%100
    
    def decodeP(self,intcode):
        p1=(intcode//100)%10
        p2=(intcode//1000)%10
        p3=(intcode//10000)%10
        return[p1,p2,p3]
    
    def processParam(self,value,paramMode):
        if paramMode==0:
            return self.code[value]
        elif paramMode==1:
            return value
        elif paramMode==2:
            return self.code[value+self.rb]
        else: return None
        
        
    
    def runCommand(self):
        self.command=self.nextValue()
        if self.debug:
            print(f'{self.name} - Index {self.pointer-1}: Command {self.command}')
        if self.decodeC(self.command)==99:
            self.isFinished=True
            if self.debug:print(f'{self.name} - Exiting\n')
            return
        if self.decodeC(self.command)==1:
            self.add()
            return
        if self.decodeC(self.command)==2:
            self.multiply()
            return
        if self.decodeC(self.command)==3:
            self.io_in()
            return
        if self.decodeC(self.command)==4:
            self.io_out()
            return
        if self.decodeC(self.command)==5:
            self.jump()
            return
        if self.decodeC(self.command)==6:
            self.jump()
            return
        if self.decodeC(self.command)==7:
            self.less()
            return
        if self.decodeC(self.command)==8:
            self.equals()
            return
        if self.decodeC(self.command)==9:
            self.adjustBase()
            return
        else:
            raise ValueError(f"{self.name} - Unexpected opcode\n")
    
    
    
    def add(self):
        
        add1=self.nextValue()
        add2=self.nextValue()
        write=self.nextValue()
        
        p1,p2,p3=self.decodeP(self.command)
        add1=self.processParam(add1,p1)
        add2=self.processParam(add2,p2)
        
        if p3==2:write+=self.rb
        if self.debug:
            print(f'{self.name} - ADD:{add1}+{add2} to index {write}\n')
            
        value=add1+add2
        self.setValue(write,value)
    
    def multiply(self):
        
        mul1=self.nextValue()
        mul2=self.nextValue()
        write=self.nextValue()
        
        p1,p2,p3=self.decodeP(self.command)
        mul1=self.processParam(mul1,p1)
        mul2=self.processParam(mul2,p2)
        if p3==2:write+=self.rb
        
        if self.debug:
            print(f'{self.name} - MUL:{mul1}*{mul2} to index {write}\n')
            
        value=mul1*mul2
        self.setValue(write,value)
    
    def io_in(self):
        self.isStopped=True
        self.awaitingInput=True
        if self.debug or self.ioReq:
            print(f'{self.name} - Awaiting Input\n')
        
    def io_give(self,value,go=True):
        if not self.awaitingInput:
            print(f'{self.name} - Not Awaiting Input\n')
            return
        write=self.nextValue()
        p1,_,_=self.decodeP(self.command)
        if p1==2:write+=self.rb
        
        if self.debug:
            print(f'{self.name} - INP:{value} to index {write}\n')
        self.setValue(write,value)
        self.isStopped=False
        self.awaitingInput=False
        if go: self.toStop()
    
    def io_out(self):
        read=self.nextValue()
        i=read
        p1,_,_=self.decodeP(self.command)
        read=self.processParam(read,p1)
        
        
        if self.debug:
            print(f'{self.name} - OUT:{read} from index {i if p1==0 else self.pointer-1 if p1==1 else i+self.rb}\n')
        self.output.append(read)
        
    def jump(self):
        test=self.nextValue()
        to=self.nextValue()
        c=self.decodeC(self.command)
        p1,p2,_=self.decodeP(self.command)
        test=self.processParam(test,p1)
        to=self.processParam(to,p2)
            
        if c==5:
            tValue=True
        elif c==6:
            tValue=False
        else:
            raise ValueError(f"{self.name} - Unexpected JMP opcode\n")
        if bool(test)==tValue:
            self.pointer=to
            if self.debug:
                print(f'{self.name} - JMP:Pointer to {test}\n')
        else:
            if self.debug:
                print(f'{self.name} - JMP:No Change\n')
    
    def less(self):
        cmp1=self.nextValue()
        cmp2=self.nextValue()
        write=self.nextValue()
        p1,p2,p3=self.decodeP(self.command)
        
        cmp1=self.processParam(cmp1,p1)
        cmp2=self.processParam(cmp2,p2)
        if p3==2:write+=self.rb
        
        value=int(cmp1<cmp2)
        if self.debug:
            print(f'{self.name} - LST:{cmp1}<{cmp2} to index {write}\n')
        self.setValue(write,value)
    
    def equals(self):
        cmp1=self.nextValue()
        cmp2=self.nextValue()
        write=self.nextValue()
        p1,p2,p3=self.decodeP(self.command)
        
        cmp1=self.processParam(cmp1,p1)
        cmp2=self.processParam(cmp2,p2)
        if p3==2:write+=self.rb
        
        value=int(cmp1==cmp2)
        
        if self.debug:
            print(f'{self.name} - EQL:{cmp1}=={cmp2} to index {write}\n')
        self.setValue(write,value)
    
    def adjustBase(self):
        adj=self.nextValue()
        p1,_,_=self.decodeP(self.command)
        adj=self.processParam(adj,p1)
        self.rb+=adj
        if self.debug:
            print(f'{self.name} - ADJ:Adjust RB by {adj} to {self.rb}\n')