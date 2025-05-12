# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 16:37:09 2025

@author: qidaw
"""
import os
import re

file_path = "Gaussian.gjf"

lat = []
atoms = set()
with open(file_path, 'r') as file:
    lines = file.readlines()
    
for line in lines:
    m = re.search('\s+Tv\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)$', line)
    if m:
        lat.extend([m.group(1), m.group(2), m.group(3)])
assert len(lat) == 9

for line in lines:
    m = re.search('\s+([A-Za-z]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)$', line)
    if m and m.group(1) != 'Tv':
        atoms.add(m.group(1))
        
filename = os.path.basename(file_path)
filename, _ = os.path.splitext(filename)
filename = filename + '_POSCAR'
atoms = list(atoms)

with open(filename, 'w') as file:   
    file.write('\n')
    file.write('1.0\n')
    file.write("       " + lat[0] + '         ' + lat[1] + '         ' + lat[2] + '\n')
    file.write("       " + lat[3] + '         ' + lat[4] + '         ' + lat[5] + '\n')
    file.write("       " + lat[6] + '         ' + lat[7] + '         ' + lat[8] + '\n')
    for atom in atoms:
        file.write(" " * (5 - len(atom)))
        file.write(atom)
    file.write('\n')
    for atom in atoms:
        i = 0
        for line in lines:
            m = re.search('\s+' + re.escape(atom) + '\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)$', line)
            if m:
                i += 1
        file.write(" " * (5 - len(str(i))))
        file.write(str(i))
    file.write('\n')
    file.write('Cartesian\n')
    for atom in atoms:
        for line in lines:
            m = re.search('\s+' + re.escape(atom) + '\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)$', line)
            if m:
                file.write(" " * (16 - len(m.group(1))))
                file.write(m.group(1))
                file.write(' ' * (20 - len(m.group(2))))
                file.write(m.group(2))
                file.write(" " * (20 - len(m.group(3))))
                file.write(m.group(3))
                file.write('\n')
                
            
            
    
        
    
    
    