# FOXO1-fep
alchemical FEP studies of FOXO1 mutations

# Methods

```
For FEP, I used 
(1) the default Gromacs: gromacs/2016.3; 
(2) I have 30 lambdas (there are 4 different intervals in these 30 lambdas)
0.000 0.002 0.004 0.006 0.008 0.01  0.02  0.03  0.04  0.05  0.10   0.15   0.20   0.25   0.30   0.35   0.40   0.45 0.50   0.55   0.60   0.65   0.70   0.75   0.80   0.85   0.90   0.95   0.975  1.00
(3) force field: Amber14sbmut
I combine two topologies: one is alchemical topology, the other one is protein-metal topology.
(4) alchemical topology built with pmx Github (Gapsys)
(5) protein-metal topology built with MCPB.py (Li, Pengfei) from Ambertools17.6
(6) There are 3 thermodynamic equations: each production running 1ns. 
```

