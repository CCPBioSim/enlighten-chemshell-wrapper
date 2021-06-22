#!/usr/bin/env python3
from enlighten2 import utils, wrappers

## To run Py-ChemShell using the structure and topology from dynam.py ##

def main():

    # get input coordinates and topology

    # set options for running Py-ChemShell from user input or defaults
    # define qm region - must be specified by user
    # get charges
    # qm code (MNDO or DFTB+)
    # method (AM1, ...)
    # max scf cycles
    # multiplicity
    # nimages is for NEB calculations
    # type of calculation (single point or optimization)
    params = {
        'qm_engine' : 'dftb'
        'qm_method' : ''
        'multiplicity' : 1
        'scftype' : 'rhf'
        'maxcycles' : 100
        'nimages' : 8
        'climbing_image' : 'yes'
        'qm_region' : ''
        'qm_charge' : ''
    }        

    # create Py-ChemShell input file (use pychemsh variable to hold the name)
    with open('pychemsh.py', 'w') as f:
        f.write("from chemsh import *")
        f.write("my_enzyme = Fragment(coords='{}', charges={})".format(inputcrd,charges))


    # run Py-ChemShell
    chemshell = wrappers.ChemShellWrapper(pychemsh)

if __name__ == '__main__':
    main()
