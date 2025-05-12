# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 15:51:48 2025

@author: qidaw
"""

"""
This script processes LOBSTER results and splits them into separate files based on interaction type.

Liu Guoliang conceived of this script. He explained the COHPCAR.lobster format to me and tested it.
"""
import re
import os

titles = [] #Stores sections containing interaction label information.
values = [] #Stores sections containing numerical calculation results.

#Path to the COHPCAR file to be processed.        
file_path = r"D:COHPCAR.lobster"
#Result files are stored in the script's directory.

with open(file_path, 'r') as file:
    lines = file.readlines()
    
#Spin polarisation is the second value on the second line.
if lines[1].split()[1] == '1':
    ISPIN = 1 #spin polarisation off
elif lines[1].split()[1] == '2':
    ISPIN = 2 #spin polarisation on
else:
    raise ValueError
    
for i in range(len(lines)):
    if not re.match(r'No\.', lines[i]):
        continue
    else:
        break

#Reads interaction labels.            
for j in range(i, len(lines)):
    if re.match(r'No\.', lines[j]):
        titles.append(lines[j])
    else:
        break

#Reads calculation resulgs.
for k in range(j, len(lines)):
    values.append(lines[k])
    if ISPIN == 1:
        #energy axis (1) + average (2) + specific interactions * 2 
        assert len(lines[k].split()) == len(titles)*2 + 3
    elif ISPIN == 2:
        #energy axis (1) + average (2) + specific interactions * 4 
        assert len(lines[k].split()) == len(titles)*4 + 5
    else:
        raise ValueError
 
#Extracts information containing only atom labels    
for i in range(len(titles)):
    m = re.search(r'([a-zA-Z]+\d+)->([a-zA-Z]+\d+)', titles[i])
    titles[i] = m.group(1) + '_' + m.group(2)
    
filename = os.path.basename(file_path)
filename, _ = os.path.splitext(filename)
        
if ISPIN == 1:
    with open(filename + "_average" + '.txt', 'w') as file:
        for line in values:
            splitted_lines = line.split()
            file.write(splitted_lines[0] + '    ' + splitted_lines[1] + '    ' + splitted_lines[2] + '\n')    
    for i in range(len(titles)):
        with open(filename + "_" + titles[i] + '_' + str(i+1) + '.txt', 'w') as file:
            for line in values:
                splitted_lines = line.split()
                file.write(splitted_lines[0] + '    ' + splitted_lines[3 + i * 2] + '    ' + splitted_lines[4 + i * 2] + '\n')
                #Specific interactions start from column 4 (index 3)
                #Interaction index i is zero-based(starts at 0)
                
elif ISPIN == 2:
    with open(filename + "_average" + '_up' + '.txt', 'w') as file:
        for line in values:
            splitted_lines = line.split()
            file.write(splitted_lines[0] + '    ' + splitted_lines[1] + '    ' + splitted_lines[2] + '\n')    
    with open(filename + "_average" + '_down' + '.txt', 'w') as file:
        for line in values:
            splitted_lines = line.split()
            file.write(splitted_lines[0] + '    ' + splitted_lines[3 + len(titles) * 2] 
                           + '    ' + splitted_lines[4 + len(titles) * 2] + '\n')
            #LOBSTER manual states down spin starts at column 2N+4
            #Python uses 0-based indexing.
    for i in range(len(titles)):
        with open(filename + "_" + titles[i] + '_' + str(i+1) + '_up' + '.txt', 'w') as file:
            for line in values:
                splitted_lines = line.split()
                file.write(splitted_lines[0] + '    ' + splitted_lines[3 + i * 2] 
                           + '    ' + splitted_lines[4 + i * 2] + '\n')
        
        with open(filename + "_" + titles[i] + '_' + str(i+1) + '_down' + '.txt', 'w') as file:
            for line in values:
                splitted_lines = line.split()
                file.write(splitted_lines[0] + '    ' + splitted_lines[5 + len(titles) * 2 + i * 2] 
                           + '    ' + splitted_lines[6 + len(titles) * 2 + i * 2] + '\n')
                #Skip 2 average columns
                #2N+6 and 2N+7 -> 0-indexed columns 2i+5 and 2i+6
    
   
    