#!/bin/bash


# this pipeline_v2.sh is for FOXO1 and Mg, and for 5 mutants: A166G, A166V, T182M, S205T, L183P

# add force field
scp -r /home/leiqian/.local/lib/python3.6/site-packages/pmx/data/mutff/amber14sbmut.ff .

# add H
gmx pdb2gmx -f ../3COA_FOXO1.pdb -o 3COA_FOXO1_H.pdb -ff amber14sbmut -water tip3p
# unused files: topol.top and posre.itp are also prepared

# mutate pdb
python3 ../job_mut_pdb.py $1 $2
# hybrid_FOXO1_mutant.pdb is prepared

# rename unused files from step: add H
mv topol.top num1_topol.top
mv posre.itp num1_posre.itp

# mutate top
gmx pdb2gmx -f hybrid_FOXO1_mutant.pdb -o hybrid_FOXO1_mutant.gro -ff amber14sbmut -water tip3p
# hybrid_FOXO1_mutant.gro, topol.top (w/o B state) and posre.itp are prepared

# change writing format of force field directory in topol.top (w/o B state)
scp topol.top topol_origin.top
sed -i "s|./amber14sbmut|amber14sbmut|g" topol.top

# hybrid top
python3 ../job_hyb_top.py
# pmxtop_FOXO1_mutant.top (w/ B state) is prepared from topol.top (w/o B state)

# combine mcpb top and hybrid top
python3 ../job_Topol_Combine.py $3 $4
# combine 3COA_dry_GMX.top and pmxtop_FOXO1_mutant.top to: top_comb.top

# rename unused files from step: mutate top
mv topol.top num2_topol.top
mv posre.itp num2_posre.itp

# MG.gro prep
scp /home/leiqian/Documents/GROMACS_FOXO1/MCPB/MCPB_Preps/MG.pdb .
gmx pdb2gmx -f MG.pdb -o MG.gro -ff amber14sbmut -water tip3p

# rename unused files from step: MG.gro prep
mv topol.top num3_mg_topol.top
mv posre.itp num3_mg_posre.itp

# hybrid_FOXO1_mutant_Mg.gro prep
python3 ../job_add_Mg.py "MG.gro" "hybrid_FOXO1_mutant.gro"

# gmx prep
gmx editconf -f hybrid_FOXO1_mutant_Mg.gro -o hybrid_FOXO1_mutant_newbox.gro -c -d 1.0 -bt cubic
gmx solvate -cp hybrid_FOXO1_mutant_newbox.gro -cs spc216.gro -o hybrid_FOXO1_mutant_solv.gro -p top_comb.top
gmx select -f hybrid_FOXO1_mutant_solv.gro -s hybrid_FOXO1_mutant_solv.gro -select "SOL" -on SOL.ndx
gmx grompp -f ../ions.mdp -c hybrid_FOXO1_mutant_solv.gro -p top_comb.top -o ions.tpr -maxwarn 31
gmx genion -s ions.tpr -o hybrid_FOXO1_mutant_solv_ions.gro -p top_comb.top -pname K -nname CL -neutral -conc 0.05 -n SOL.ndx

# # this step is for 3 mutants: L183R, S152R, S153R
# # change K ion in gro file and top file for neutral condition
# python3 ../job_changeK_newgro.py hybrid_FOXO1_mutant_solv_ions.gro
# gmx genconf -f hybrid_FOXO1_mutant_K_solv_ions.gro -o hybrid_FOXO1_mutant_K_solv_ions_sort.gro -renumber
# python3 ../job_changeK_newtop.py top_comb.top









