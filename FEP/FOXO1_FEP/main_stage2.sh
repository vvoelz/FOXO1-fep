#!/bin/bash

cd L183R
./../job_mdp.sh
scp hybrid_FOXO1_mutant_K_solv_ions_sort.gro hybrid_X_solv_ions.gro
scp top_comb_K.top pmxtop_X.top
./../job_em.sh
cd ..

cd S152R
./../job_mdp.sh
scp hybrid_FOXO1_mutant_K_solv_ions_sort.gro hybrid_X_solv_ions.gro
scp top_comb_K.top pmxtop_X.top
./../job_em.sh
cd ..

cd S153R
./../job_mdp.sh
scp hybrid_FOXO1_mutant_K_solv_ions_sort.gro hybrid_X_solv_ions.gro
scp top_comb_K.top pmxtop_X.top
./../job_em.sh
cd ..

cd A166G
./../job_mdp.sh
scp hybrid_FOXO1_mutant_solv_ions.gro hybrid_X_solv_ions.gro
scp top_comb.top pmxtop_X.top
./../job_em.sh
cd ..

cd A166V
./../job_mdp.sh
scp hybrid_FOXO1_mutant_solv_ions.gro hybrid_X_solv_ions.gro
scp top_comb.top pmxtop_X.top
./../job_em.sh
cd ..

cd T182M
./../job_mdp.sh
scp hybrid_FOXO1_mutant_solv_ions.gro hybrid_X_solv_ions.gro
scp top_comb.top pmxtop_X.top
./../job_em.sh
cd ..

cd S205T
./../job_mdp.sh
scp hybrid_FOXO1_mutant_solv_ions.gro hybrid_X_solv_ions.gro
scp top_comb.top pmxtop_X.top
./../job_em.sh
cd ..

cd L183P
./../job_mdp.sh
scp hybrid_FOXO1_mutant_solv_ions.gro hybrid_X_solv_ions.gro
scp top_comb.top pmxtop_X.top
./../job_em.sh
cd ..

