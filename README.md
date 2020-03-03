# FOXO1-fep
alchemical FEP studies of FOXO1 mutations

# Methods

On Feb 10, 2020, at 1:49 PM, Lei Qian <tuk04130@temple.edu> wrote:

```
For FEP, I used 
(1) the default Gromacs: gromacs/2016.3; 
(2) total 21 lambda: 0.00, 0.05, 0.10, 0.15, 0.20, 0.25, ... 0.90, 0.95, 1.00;
(3) force field: amber99sb-star-ildn
I combine two topologies: one is alchemical topology, the other one is protein-metal topology.
(4) alchemical topology built with pmx webserver (Gapsys)
(5) protein-metal topology built with MCPB.py (Li, Pengfei) from Ambertools17.6
(6) There are 3 thermodynamic equations: each production running 1ns. 
```

