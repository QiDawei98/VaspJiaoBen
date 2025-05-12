# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 22:34:34 2024

@author: qidaw
"""

"""
Extracts information about:
    free energy TOTEN
    E-fermi
    final convergence information
    Maximum number of electronic SC (self-consistency) steps
    ISYM
The script should be run from the directory where the OUTCAR, OSZICAR, and INCAR files are located.
"""

import re

with open(r'OUTCAR', 'r') as OUTCAR:
    line = OUTCAR.readline()
    while line != '': #The EOF char is an empty string
        if re.search('free  energy   TOTEN', line):
            print(line.lstrip().rstrip('\r\n') + '    #from OUTCAR')
        if re.search('E-fermi', line):
            print(line.lstrip().rstrip('\r\n') + '    #from OUTCAR')
        line = OUTCAR.readline()
print('')
        
with open(r'OSZICAR', 'r') as OSZICAR:
    line = OSZICAR.readline()
    while line != '': #find first DAV
        if re.search('DAV:', line):
            previous_line = line 
            while line != '':
                if not re.search('DAV:', line): #find first line without DAV
                    print(previous_line.rstrip('\r\n') + '    #from OSZICAR')
                    break
                else: #if not, store it as previous_line
                    previous_line = line
                line = OSZICAR.readline()  #read next line for the last DAV search cycle
        line = OSZICAR.readline() #read next line for the first DAV search cycle
        
print('')

ISYM_exist = False
with open(r'INCAR', 'r') as INCAR:
    line = INCAR.readline()
    while line != '':
        line = re.sub(r'[#!].*', '', line) #remove INCAR comments
        if re.search(r'NELM\b', line):
            print(line.rstrip('\r\n') + '    #from INCAR')
        elif re.search(r'ISYM\b', line):
            print(line.rstrip('\r\n') + '    #from INCAR')
            ISYM_exist = True
        line = INCAR.readline()
if not ISYM_exist:
    print('ISYM as Default')
