import os
from pmx.model import Model
from pmx.alchemy import mutate
import sys

FOXO1 = Model('3COA_FOXO1_H.pdb', rename_atoms=True, renumber_residues=True)
# Note that, by default, pmx.model.Model renumbers all residues from 1.
# Set renumber_residues=True
hybrid_FOXO1_mutant = mutate(m=FOXO1, mut_resid=int(sys.argv[1]), mut_chain='A', mut_resname=str(sys.argv[2]), ff='amber14sbmut', verbose=True)
hybrid_FOXO1_mutant.write('hybrid_FOXO1_mutant.pdb')

