
#!/bin/bash

mkdir MDP/

for f in em_lam{0..5}.mdp; do scp em_correct.mdp MDP/$f; done
for x in {0..5}; do sed -i "s/init_lambda_state        = 10/init_lambda_state        = $x/" MDP/em_lam$x.mdp; done
for x in {0..5}; do sed -i "s/; init_lambda_state        0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15   16   17   18   19   20/; init_lambda_state        0    1    2    3    4    5/" MDP/em_lam$x.mdp; done
for x in {0..5}; do sed -i "s/fep_lambdas              = 0.00 0.05 0.10 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50 0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95 1.00/fep_lambdas              = 0.00 0.01 0.02 0.03 0.04 0.05/" MDP/em_lam$x.mdp; done

for f in nvt_lam{0..5}.mdp; do scp nvt_correct.mdp MDP/$f; done
for x in {0..5}; do sed -i "s/init_lambda_state        = 10/init_lambda_state        = $x/" MDP/nvt_lam$x.mdp; done
for x in {0..5}; do sed -i "s/; init_lambda_state        0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15   16   17   18   19   20/; init_lambda_state        0    1    2    3    4    5/" MDP/nvt_lam$x.mdp; done
for x in {0..5}; do sed -i "s/fep_lambdas              = 0.00 0.05 0.10 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50 0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95 1.00/fep_lambdas              = 0.00 0.01 0.02 0.03 0.04 0.05/" MDP/nvt_lam$x.mdp; done

for f in npt_lam{0..5}.mdp; do scp npt_correct.mdp MDP/$f; done
for x in {0..5}; do sed -i "s/init_lambda_state        = 10/init_lambda_state        = $x/" MDP/npt_lam$x.mdp; done
for x in {0..5}; do sed -i "s/; init_lambda_state        0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15   16   17   18   19   20/; init_lambda_state        0    1    2    3    4    5/" MDP/npt_lam$x.mdp; done
for x in {0..5}; do sed -i "s/fep_lambdas              = 0.00 0.05 0.10 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50 0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95 1.00/fep_lambdas              = 0.00 0.01 0.02 0.03 0.04 0.05/" MDP/npt_lam$x.mdp; done

for f in md_lam{0..5}.mdp; do scp md_correct.mdp MDP/$f; done
for x in {0..5}; do sed -i "s/init_lambda_state        = 10/init_lambda_state        = $x/" MDP/md_lam$x.mdp; done
for x in {0..5}; do sed -i "s/; init_lambda_state        0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15   16   17   18   19   20/; init_lambda_state        0    1    2    3    4    5/" MDP/md_lam$x.mdp; done
for x in {0..5}; do sed -i "s/fep_lambdas              = 0.00 0.05 0.10 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50 0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95 1.00/fep_lambdas              = 0.00 0.01 0.02 0.03 0.04 0.05/" MDP/md_lam$x.mdp; done
