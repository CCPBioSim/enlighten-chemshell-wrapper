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
    # type of calculation (single point or optimization)

    # create Py-ChemShell input file (use pychemsh variable to hold the name)
    pychemsh = '/home/skfegan/chemsh-tutorial/single-point/sp_mndo'

    # run Py-ChemShell
    chemshell = wrappers.ChemShellWrapper(pychemsh)

if __name__ == '__main__':
    main()
