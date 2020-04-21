#!/bin/bash

mcpb="../3COA_dry_GMX.top"
hybrid="pmxtop_FOXO1_mutant.top"

mkdir L183R
cd L183R
./../pipeline_v1.sh 34 "R" $mcpb $hybrid
cd ..

mkdir S152R
cd S152R
./../pipeline_v1.sh 3 "R" $mcpb $hybrid
cd ..

mkdir S153R
cd S153R
./../pipeline_v1.sh 4 "R" $mcpb $hybrid
cd ..

mkdir A166G
cd A166G
./../pipeline_v2.sh 17 "G" $mcpb $hybrid
cd ..

mkdir A166V
cd A166V
./../pipeline_v2.sh 17 "V" $mcpb $hybrid
cd ..

mkdir T182M
cd T182M
./../pipeline_v2.sh 33 "M" $mcpb $hybrid
cd ..

mkdir S205T
cd S205T
./../pipeline_v2.sh 56 "T" $mcpb $hybrid
cd ..

mkdir L183P
cd L183P
./../pipeline_v2.sh 34 "P" $mcpb $hybrid
cd ..




