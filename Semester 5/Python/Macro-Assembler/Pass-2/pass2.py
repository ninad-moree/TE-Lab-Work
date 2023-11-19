import re as regex
import json
import os

os.system('cls' if os.name == 'nt' else 'clear')

with open("D:\Coding\PICT College\TE Lab Work\Semester 5\Python\Macro-Assembler\Pass-2\output\expcode.asm",'w') as file:
    pass
file.close()

def get_key(val: str, dict: dict) -> any:
    for key, value in dict.items():
        if val == value:
            return key
    return None

def process_params(param: str):
    pattern = r'\(([^,]+),(\d+)\)'
    match = regex.match(pattern, param)
    if match:
        component1 = match.group(1)
        component2 = int(match.group(2))
        return component1, component2
    else:
        return None
    
def convert(lst):
    return ' '.join(lst)

kpdtabFile = open('D:\Coding\PICT College\TE Lab Work\Semester 5\Python\Macro-Assembler\Pass-2\input\kpdtab.json', 'r')
mdtFile = open('D:\Coding\PICT College\TE Lab Work\Semester 5\Python\Macro-Assembler\Pass-1\output\mdt.asm', 'r')
mntFile = open('D:\Coding\PICT College\TE Lab Work\Semester 5\Python\Macro-Assembler\Pass-1\output\mnt.json', 'r')
pntabFile = open('D:\Coding\PICT College\TE Lab Work\Semester 5\Python\Macro-Assembler\Pass-1\output\pntab.json', 'r')
callsFile = open('D:\Coding\PICT College\TE Lab Work\Semester 5\Python\Macro-Assembler\Pass-2\input\calls.asm', 'r')

expcodeFile = open('D:\Coding\PICT College\TE Lab Work\Semester 5\Python\Macro-Assembler\Pass-2\output\expcode.asm', 'a')

kpdtab = json.load(kpdtabFile)
mnt = json.load(mntFile)
pntab = json.load(pntabFile)

spacePattern = r'\s+'

for line in callsFile:
    if line == '\n': continue
    line = line.strip()

    cmd = regex.split(spacePattern, line.rstrip())

    macroName = cmd[0] 
    MPList = cmd[1::] 
      
    mdtPointer, kpdtPointer, npp, nkp = "","","",""

    for key,value in mnt.items():
        if value['name'] == macroName:
            mdtPointer = value['mdtp']
            kpdtPointer = value['kpdtp']
            npp = value['pp']
            nkp = value['kp']
            break

    tot = npp + nkp

    APTAB = pntab[macroName].copy()
    aptPointer = 1

    if mdtPointer == "":
        print("No such macro exists")
        continue

    for parameter in MPList:
        if parameter[-1] == ',':
            parameter = parameter.replace(',','',1)

        if '=' in parameter:
            eqIndex = parameter.index('=')
            paramName = parameter[0:eqIndex:]
            paramValue = parameter[eqIndex + 1::]

            APTAB[get_key(paramName, APTAB)] = paramValue

        else:
            APTAB[str(aptPointer)] = parameter
            aptPointer += 1

    if nkp:
        for key, value in kpdtab.items():
            if (value["macro"] == macroName) and (value["value"] != "---"):
                if APTAB.get(get_key(value["name"], APTAB)):
                    APTAB[get_key(value["name"], APTAB)] = value["value"]

    macroStmts = []

    current_line_number = 0
    for mdtLine in mdtFile:
        current_line_number += 1
        if current_line_number == mdtPointer:
            macroStmts.append(mdtLine)  
            break

    for mdtLine in mdtFile:
        if 'MEND' in mdtLine:
            break
        macroStmts.append(mdtLine) 

    for macroStatementIndex in range(len(macroStmts)):
        macroStatement = macroStmts[macroStatementIndex]
        macroCmd = regex.split(spacePattern, macroStatement.rstrip())

        for itemIndex in range(len(macroCmd)):
            item = macroCmd[itemIndex]
            
            if '(' in item:
                tab_pos = process_params(item)
                if tab_pos is not None:
                    tab, pos = tab_pos
                else:
                    print("Invalid format for item:", item)

        macroCmd[0] = "+" + macroCmd[0]     # Add a '+' at the beginning to denote expanded code
        macroStmts[macroStatementIndex] = convert(macroCmd)
        expcodeFile.write(macroStmts[macroStatementIndex] + '\n')

    mdtFile.seek(0)
    expcodeFile.write('\n')
    APTAB = ""
    mdtLine=""