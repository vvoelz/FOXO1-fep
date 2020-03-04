#!/bin/bash

FREE_ENERGY=`pwd`
mkdir XVG
XVG=$FREE_ENERGY/XVG

for (( i=0; i<21; i++ ))
do
    LAMBDA=$i
    cd Lambda_$LAMBDA
    cd Production_MD
    scp md_lam$LAMBDA.xvg $XVG/
    cd $FREE_ENERGY
done

exit;
