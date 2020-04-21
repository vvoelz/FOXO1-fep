#!/bin/bash

cd L183R
alchemical_analysis -d XVG/ -p md_lam -q xvg -u kJ -w
sleep 5
cd ..

cd S152R
alchemical_analysis -d XVG/ -p md_lam -q xvg -u kJ -w
sleep 5
cd ..

cd S153R
alchemical_analysis -d XVG/ -p md_lam -q xvg -u kJ -w
sleep 5
cd ..

cd A166G
alchemical_analysis -d XVG/ -p md_lam -q xvg -u kJ -w
sleep 5
cd ..

cd A166V
alchemical_analysis -d XVG/ -p md_lam -q xvg -u kJ -w
sleep 5
cd ..

cd T182M
alchemical_analysis -d XVG/ -p md_lam -q xvg -u kJ -w
sleep 5
cd ..

cd S205T
alchemical_analysis -d XVG/ -p md_lam -q xvg -u kJ -w
sleep 5
cd ..

cd L183P
alchemical_analysis -d XVG/ -p md_lam -q xvg -u kJ -w
sleep 5
cd ..

