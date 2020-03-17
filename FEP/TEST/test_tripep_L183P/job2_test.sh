#!/bin/bash

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

    mkdir Lambda_$LAMBDA
    cd Lambda_$LAMBDA

    ##############################
    # ENERGY MINIMIZATION STEEP  #
    ##############################
    echo "Starting minimization for lambda = $LAMBDA..." 

    mkdir EM
    cd EM

    # Iterative calls to grompp and mdrun to run the simulations

    gmx grompp -f $MDP/em_lam$LAMBDA.mdp -c $FREE_ENERGY/hybrid_tripep_solv_ions.gro -p $FREE_ENERGY/pmxtop.top -o em_lam$LAMBDA.tpr

    gmx mdrun -v -deffnm em_lam$LAMBDA

    sleep 10

    cd $FREE_ENERGY
done

exit;
