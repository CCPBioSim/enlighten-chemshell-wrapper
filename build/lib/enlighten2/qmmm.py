#!/usr/bin/env python3
import argparse
import json
from enlighten2 import utils, wrappers

## To run Py-ChemShell using the structure and topology from dynam.py ##

def main():

    # get input coordinates and topology
    parser = argparse.ArgumentParser(description="Runs a QM/MM calculation\n", formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("type", help="type of calculation: sp, opt, neb")
    parser.add_argument("params", help="JSON file with parameters", type=argparse.FileType())
    parser.add_argument("parmtop", help="topology information", type=argparse.FileType())
    parser.add_argument("reactants", help="file for the initial coordinates of the system", type=argparse.FileType())
    parser.add_argument("-p","-products", help="file for the final coordinates of the system for neb only", type=argparse.FileType())

    args = parser.parse_args()

    # set options for running Py-ChemShell from user input or defaults
    # define qm region - must be specified by user
    # get charges
    # qm code (MNDO or DFTB+)
    # method (AM1, ...)
    # max scf cycles
    # multiplicity
    # nimages is for NEB calculations
    # type of calculation (single point or optimization)
    params = {'qm_engine' : 'DFTBplus', 
            'qm_path' : '~/dftb/bin/dftb+', 
            'skf_path' : '~/dftb/slakos/mio-1-1/',
            'qm_method' : 'am1', 
            'multiplicity' : 1, 
            'scftype' : 'rhf', 
            'maxcycles' : 100, 
            'nimages' : 8, 
            'climbing_image' : 'yes', 
            'qm_region' : [], 
            'qm_charge' : []}

    if args.params is not None:
        params.update(json.load(args.params))

    qm_region = params['qm_region']
    qm_charge = params['qm_charge']
    qm_engine = params['qm_engine']
    qm_method = params['qm_method']
    multiplicity = params['multiplicity']
    skf_path = params['skf_path']
    qm_path = params['qm_path']

    # read charges from topology file (amber charges must be divided by 18.2223 to get the units right)
    charges = utils.get_amber_charges(args.parmtop.name)

    # create Py-ChemShell input file
    with open('pychemsh.py', 'w') as f:
        f.write("from chemsh import * \n")
        f.write("my_enzyme = Fragment(coords='../{}', charges={})\n".format(args.reactants.name,charges))
        f.write("my_enzyme.save('new.pdb')\n")
        f.write("indicies_qm_region = {}\n".format(qm_region))
        f.write("frag_qm_region = my_enzyme.getSelected(indicies_qm_region)\n")
        f.write("frag_qm_region.save('qm_region.pdb')\n")
        f.write("qm_charge = {}\n".format(qm_charge))
        if qm_engine == 'DFTBplus':
            f.write("my_qm = {}(charge = {}, mult = {}, skf_path='{}', path = '{}',)\n".format(qm_engine,qm_charge,multiplicity,skf_path,qm_path))
        else:
            f.write("my_qm = {}(method = '{}', charge = {}, mult = {}, path = '{}',)\n".format(qm_engine,qm_method,qm_charge,multiplicity,qm_path))
        f.write("my_mm = DL_POLY(ff='../{}', rcut=999.99)\n".format(args.parmtop.name))
        f.write("my_qmmm = QMMM(frag = my_enzyme, qm = my_qm, mm = my_mm, qm_region = indicies_qm_region,)\n")
        if args.type == 'opt':
            f.write("my_opt = Opt(theory=my_qmmm)\n")
            f.write("my_opt.run(dryrun=False)\n")


    # run Py-ChemShell
    chemshell = wrappers.ChemShellWrapper('pychemsh')

if __name__ == '__main__':
    main()
