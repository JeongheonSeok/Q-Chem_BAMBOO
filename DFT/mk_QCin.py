#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 13:46:40 2024

@author: JeongHeonSeok
"""

import os
import re

#%% #############################User Setting##################################
# There should be Q-Chem input files, PBS files, and xyz files in the working directory

directory = '.'                 # working directory
xyzdir = './xyz'
spdir = './SP'
qcformat = 'SPformat.in'
xyzindicator = 'xyzloc'         # input format exchange
chargeindicator = 'chargeloc'

# ION_LIST element: [ion name, charge]
ION_LIST = [['Li',1],['FSI',-1]]
#%% ###########################################################################
def charge_from_xyz(setname):
    """
    calculate charge from set name.\n
    ION_LIST need. default: Li, FSI

    Parameters
    ----------
    set_name : string
        may contain Li and FSI(default).\n
        If other ion needed, please modify ION_LIST \n
        ex) Frame10_0-7_sub6-0_TFDMP5FSI1 -> this function check TFDMP5FSI1 part

    Returns
    -------
    charge : int
        ex) = #Li - #FSI

    """
    setname = setname.split('_')[2]
    charge = 0
    for ion, ion_charge in ION_LIST:
        ion_match = re.search(rf'{ion}(\d+)', setname)
    
        if ion_match:
            ion_count = int(ion_match.group(1))
            charge += ion_count * ion_charge
    return int(charge+1)

#%% 
# load .xyz file name
xyz_files = []
for filename in os.listdir(xyzdir):
    if filename.endswith('.xyz'):
        xyz_files.append(filename)

# Read the contents of QC format and save them to qcf_txt.
with open(qcformat, 'r') as qcf:
    qcf_txt = qcf.read()

for xyz_file in xyz_files:
    # Read coordinate information from xyz file and save it in coord.
    with open(os.path.join(xyzdir, xyz_file), 'r') as xf:
        lines_xf = xf.readlines()
    coord = ''.join(lines_xf[2:])
        
    # Assign coord to format.
    qcin = qcf_txt
    qcin = qcin.replace(xyzindicator, coord)
    
    # charge, spin information
    chargespin = str(charge_from_xyz(xyz_file))+" 1"
    qcin = qcin.replace(chargeindicator, chargespin)
        
    # Create an input file with coordinates entered
    file_name = xyz_file[:-4] + '_SP.in'
    if not os.path.exists(spdir):
        os.makedirs(spdir)
    file_path = os.path.join(spdir, file_name)
    with open(file_path, 'w') as file:
        file.write(qcin)
