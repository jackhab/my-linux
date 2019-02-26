#!/usr/bin/python3


# TODO:

# , char  switches separator on/off
# highligt on Windows platform
# highlight float numbers properly (int part is broken because of dot)
# use decimal instead of float (with Python float:  0.1+0.1+0.1=0.30000000000000004)
# accept 'h' suffix for hex numbers
#
# DONE:
# search the closest power for suffix attachment min(ppp, key=lambda x: abs(x-10))
# KMGmunpf suffixes
# allow binary number input 0b11010
# help for operators and math functions
# twos complement for negative binaries
# dec, hex and bin groups using colors or bold
# colored prompt and brown backgroud
# detect exponent before detecting hex numbers
# fix: negative 'e' in exponent converted to hex


import sys
import cmd
import re
from math import *

if sys.platform == 'win32':
    import ctypes
    ctypes.windll.kernel32.SetConsoleTitleW('jcalc')

    
def addMagSuf(x):
    if x == 0:
        return ''
        
    sufs={-15:'f',-12:'p',-9:'n',-6:'u',-3:'m',3:'K',6:'M',9:'G',12:'T',15:'P'}
    mag = int(log10(abs(x)))
    
    if mag > 15: mag = 15
    if mag < -15: mag = -15
    
    powerNear3 = int(mag/3)*3
    magNear3 = 10**powerNear3
    try:
        suffix = sufs[powerNear3]
    except KeyError:
        suffix=''
        
    final  = '{0:g}'.format(x / magNear3)
    #print(x, magNear3, final + suffix)
    return final + suffix

    
class MainCmd(cmd.Cmd):
    resVar = '@'
    resVals = {}

    
    def setResVar(self):
        '''generate one-letter variable name to hold the result history
            and update the prompt'''
        ascii = ord(self.resVar)
        if ascii == 91:
            ascii = 64
        self.resVar = chr(ascii + 1)
        self.prompt = Colors.GREEN + '\n' + self.resVar + ' = ' + Colors.NONE

        
    def preloop(self):
        '''cmd module init'''
        cmd.Cmd.preloop(self)
        self.setResVar()

    def do_EOF(self, Line):
        '''exit from shell on Ctrl-D'''
        return True


    def default(self, Line):
        '''command line callback: calculate both integer and floating results and
           print floating if it's more precise othewise integer in dec, hex and bin formats'''

        if Line == 'h' or Line == 'H':
            printHelp()
            return

        #remove digit groups separators and spaces
        Line = re.sub(r'[ ,]', '', Line)
        orgLine = Line
        
        #replace variable names with result history from resVals dictionary
        resVars = re.findall(r'''\b[A-Z]\b''', Line)
        if len(resVars) > 0:
            for v in resVars:
                try:
                    Line = re.sub(r'\b' + v + r'\b', self.resVals[v], Line)
                except KeyError:
                    print("Variable", v, 'is empty')
                    return

        
        #replace magnitude suffixes
        magFlag = False
        def suffixSub(match):
            sufs = {'f': 'e-15', 'p': 'e-12', 'n': 'e-9', 'u': 'e-6', 'm': 'e-3', 'K': 'e3', 'M': 'e6', 'G': 'e9', 'T': 'e12', 'P': 'e15'}
            m = match.group(0)
            nonlocal magFlag
            magFlag = True
            #return the found number with its suffix replaced to 'ePOWER'
            return m[:-1] + sufs[m[-1]]
        Line = re.sub(r'(\b\d+[fpnumKMGT]\b)', suffixSub, Line) 
        
        #now we can make everything lower case to make regex simpler
        Line = Line.lower()
        
        #convert e.g. log3(15) to log(15,3)
        Line = re.sub(r'log(\d+)\((\d+)\)', r'log(\2,\1)', Line) 
        
        #convert 0b-binary to decimal; must run before hex conversion
        #to avoid detecting e.g. 0b11 as 0xB11
        Line = re.sub(r'\b0b[01]+\b', lambda m: str(int(m.group(0), 2)), Line)

        #add '0x' prefix to hex number if not present
        def hexSub(match):
            m = match.group(0)
            if re.fullmatch(r'[\d.]+e-*[\d.]+', m): return m
            if re.fullmatch(r'[\d.]+e-[\d.]+', m): return m
            return r'0x' + m
        Line = re.sub(r'(\b\d*[a-f]+\d*[a-f]*\b)', hexSub, Line) 

        #convert hex to decimal
        def hexConv(match):
            return str(int(match.group(0), 16))
        Line = re.sub(r'(\b0x[a-f0-9]+\b)', hexConv, Line)
        
        #allow x! factorial format
        Line = re.sub(r'(\b[0-9]+)!', r'factorial(\1)', Line)

        #show parsed line to user to verify substitutions
        if Line != orgLine:
            print("   ", Line)

        result = None
        try:
            result = eval(Line)
            intResult = int(result)
        except:
            print("Can't calculate")
            return

        hexResult = ''
        binResult = ''
        finResult = ''
        sufResult = ''
        
        if intResult == result:
            finResult = intResult
        else:
            finResult = result
            
        decResult = fmt(finResult, 10)

        if (result <= 2**64):
            hexResult = fmt(finResult, 16)
            binResult = fmt(finResult, 2)
        
        if magFlag:
            sufResult = addMagSuf(finResult)
            if sufResult == decResult:
                sufResult = ''
            
        justLen = max(len(binResult), 45)
        decResult = decResult.rjust(justLen)
        sufResult = sufResult.rjust(justLen)
        hexResult = hexResult.rjust(justLen)
        binResult = binResult.rjust(justLen)


        print('%s\n%s\n%s\n%s' % (decResult, sufResult, hexResult, binResult))

            
        #advance history variable to the next letter after successful calculation
        self.resVals[self.resVar] = str(finResult)
        self.setResVar()


def printHelp():
    print('''
Note:
    * binary numbers must have '0b'
    * numbers with [a-f] forced to hex
        even when they don't have '0x'
    * hex, bin and dec can be mixed

Operators:
    + - * / % ** !
    & | ^ ~ << >>

Functions:
    pi
    degrees(x)
    radians(x)
    logN(x)

    sin(x) asin(x) sinh(x) asinh(x)
    cos(x) acos(x) cosh(x) acosh(x)
    tan(x) atan(x) tanh(x) atanh(x) 
''')

    

class Colors:
    if sys.platform == 'win32':
        BLUE = GREEN = BOLD = NONE = UNDERLINE = CYAN = WHITE = ''
    else:
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        BOLD = '\033[1m'
        NONE = '\033[0m'
        UNDERLINE = '\033[4m'
        CYAN = '\033[36m'
        WHITE = '\033[7m'
    
    def __init__(self):
        self.curCol = self.BOLD
        self.newCol = self.GREEN

    def switchCol(self):
        if self.curCol == self.NONE:
            self.curCol = self.newCol
        else:
            self.curCol = self.NONE
        return self.curCol



def chopStr(strIn, chopSize):
    '''split a string into list of strings; each one is the size of chopSize, e.g.:
        chopStr('example', 3) => ['e', 'xam', 'ple'] '''
    
    parts = []
    for t in range(len(strIn), 0, chopSize * -1):
        f = t - chopSize
        if f < 0:
            f=0        
        parts.insert(0, strIn[f:t])
    return parts
        
        
def highLight(numStr):
    '''highlight groups of digits in a string:
         every 3 digits for decimal, every 4 for bin and hex'''
    
    if sys.platform == 'win32':
        return numStr
        
    #split number into base prefix with rjust spaces and numerical value 
    splits = re.split('(^\s*(0x|0b)*)', numStr)
    prefix = splits[1]
    value = splits[3]
    
    #float highlighting is not implemented yet
    if '.' in value:
        return numStr
    
    #set string group size from base prefix
    if prefix.strip()[0:2] in ['0x', '0b']:
        groupSize = 4
    else:
        groupSize = 3

    #split strings into groups and highlight each one
    #groups are reversed to start highlighting from number's end 
    groupsIn = chopStr(value, groupSize)[::-1]
    
    c = Colors()
    groupsOut = [c.switchCol() + p for p in groupsIn][::-1]
    
    hiValue = ''.join(groupsOut)
    
    return prefix + hiValue + c.NONE
    
    
def fmt(num, base=10):
    '''return a formatted string from a number according to 2 or 16 or 10 base'''
    
    if num == None:
        return None
     
    if isinstance(num, float) and base != 10:
        return ''
        
    if base == 2:
        if num >= 0:        
            ret = bin(num)
        else:
            ret = bin(int(-1 * num - pow(2, 32))).replace('-', '')
    elif base == 16:
        if num >= 0:
            ret = hex(num)
        else:
            ret = hex(int(-1 * num - pow(2, 32))).replace('-', '')
    else:
        ret = str(num)
        
    #ret = ret.rjust(35)
    ret = highLight(ret)

    return ret

    
def test():
    sufs = {'f': 'e-15', 'p': 'e-12', 'n': 'e-9', 'u': 'e-6', 'm': 'e-3', 'K': 'e3', 'M': 'e6', 'G': 'e9', 'T': 'e12', 'P': 'e15'}
    print('test')

    [addMagSuf(x) for x in [0.001,1,200,999,1000,1001,9999,10000,100000,1000000]]
    
if __name__ == '__main__':
    if 'test' in sys.argv:
        test()
        sys.exit()
        
    MainCmd().cmdloop()















