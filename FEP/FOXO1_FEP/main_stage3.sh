#!/bin/bash

cd L183R
for x in {0..29}; do sed -i "s/gen_seed                 = 173529   ; change -1 to 173529/gen_seed                 = -1/" MDP/nvt_lam$x.mdp; done
cd ..
tar -cvzf L183R.tar.gz L183R/

cd S152R
for x in {0..29}; do sed -i "s/gen_seed                 = 173529   ; change -1 to 173529/gen_seed                 = -1/" MDP/nvt_lam$x.mdp; done
cd ..
tar -cvzf S152R.tar.gz S152R/

cd S153R
for x in {0..29}; do sed -i "s/gen_seed                 = 173529   ; change -1 to 173529/gen_seed                 = -1/" MDP/nvt_lam$x.mdp; done
cd ..
tar -cvzf S153R.tar.gz S153R/

cd A166G
for x in {0..29}; do sed -i "s/gen_seed                 = 173529   ; change -1 to 173529/gen_seed                 = -1/" MDP/nvt_lam$x.mdp; done
cd ..
tar -cvzf A166G.tar.gz A166G/

cd A166V
for x in {0..29}; do sed -i "s/gen_seed                 = 173529   ; change -1 to 173529/gen_seed                 = -1/" MDP/nvt_lam$x.mdp; done
cd ..
tar -cvzf A166V.tar.gz A166V/

cd T182M
for x in {0..29}; do sed -i "s/gen_seed                 = 173529   ; change -1 to 173529/gen_seed                 = -1/" MDP/nvt_lam$x.mdp; done
cd ..
tar -cvzf T182M.tar.gz T182M/

cd S205T
for x in {0..29}; do sed -i "s/gen_seed                 = 173529   ; change -1 to 173529/gen_seed                 = -1/" MDP/nvt_lam$x.mdp; done
cd ..
tar -cvzf S205T.tar.gz S205T/

cd L183P
for x in {0..29}; do sed -i "s/gen_seed                 = 173529   ; change -1 to 173529/gen_seed                 = -1/" MDP/nvt_lam$x.mdp; done
cd ..
tar -cvzf L183P.tar.gz L183P/

