#!/bin/sh
#PBS -l walltime=48:00:00
#PBS -N fep_tripeptide_test
#PBS -q normal
#PBS -l nodes=1:ppn=28

cd $PBS_O_WORKDIR

module load gromacs/2016.3

# Set some environment variables 
FREE_ENERGY=`pwd`
echo "Free energy home directory set to $FREE_ENERGY"
MDP=$FREE_ENERGY/MDP
echo ".mdp files are stored in $MDP"

for (( i=0; i<6; i++ ))
do
    LAMBDA=$i

    # A new directory will be created for each value of lambda and
    # at each step in the workflow for maximum organization.
 
    cd Lambda_$LAMBDA

    #####################
    # NVT EQUILIBRATION #
    #####################
    echo "Starting constant volume equilibration..."

    mkdir NVT
    cd NVT

    gmx grompp -f $MDP/nvt_lam$LAMBDA.mdp -c ../EM/em_lam$LAMBDA.gro -p $FREE_ENERGY/pmxtop.top -o nvt_lam$LAMBDA.tpr

    gmx mdrun -nt 22 -ntmpi 22 -npme 4 -deffnm nvt_lam$LAMBDA

    echo "Constant volume equilibration complete."

    sleep 10

    #####################
    # NPT EQUILIBRATION #
    #####################
    echo "Starting constant pressure equilibration..."

    cd ../
    mkdir NPT
    cd NPT

    gmx grompp -f $MDP/npt_lam$LAMBDA.mdp -c ../NVT/nvt_lam$LAMBDA.gro -p $FREE_ENERGY/pmxtop.top -t ../NVT/nvt_lam$LAMBDA.cpt -o npt_lam$LAMBDA.tpr

    gmx mdrun -nt 22 -ntmpi 22 -npme 4 -deffnm npt_lam$LAMBDA

    echo "Constant pressure equilibration complete."

    sleep 10

    #################
    # PRODUCTION MD #
    #################
    echo "Starting production MD simulation..."

    cd ../
    mkdir Production_MD
    cd Production_MD

    gmx grompp -f $MDP/md_lam$LAMBDA.mdp -c ../NPT/npt_lam$LAMBDA.gro -p $FREE_ENERGY/pmxtop.top -t ../NPT/npt_lam$LAMBDA.cpt -o md_lam$LAMBDA.tpr

    gmx mdrun -nt 22 -ntmpi 22 -npme 4 -deffnm md_lam$LAMBDA

    echo "Production MD complete."

    # End
    echo "Ending. Job completed for lambda = $LAMBDA"

    cd $FREE_ENERGY
done

exit;
