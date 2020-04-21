import os
from pmx.forcefield import Topology
from pmx.alchemy import gen_hybrid_top

top_FOXO1_mutant = Topology('topol.top')
pmxtop_FOXO1_mutant, _ = gen_hybrid_top(topol=top_FOXO1_mutant)
pmxtop_FOXO1_mutant.write('pmxtop_FOXO1_mutant.top')

