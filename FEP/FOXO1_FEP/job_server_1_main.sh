#!/bin/bash

cd L183R
qsub ../job_server_1A.sh
sleep 5
qsub ../job_server_1B.sh
sleep 5
qsub ../job_server_1C.sh
sleep 5
cd ..

cd S152R
qsub ../job_server_1A.sh
sleep 5
qsub ../job_server_1B.sh
sleep 5
qsub ../job_server_1C.sh
sleep 5
cd ..

cd S153R
qsub ../job_server_1A.sh
sleep 5
qsub ../job_server_1B.sh
sleep 5
qsub ../job_server_1C.sh
sleep 5
cd ..

cd A166G
qsub ../job_server_1A.sh
sleep 5
qsub ../job_server_1B.sh
sleep 5
qsub ../job_server_1C.sh
sleep 5
cd ..

cd A166V
qsub ../job_server_1A.sh
sleep 5
qsub ../job_server_1B.sh
sleep 5
qsub ../job_server_1C.sh
sleep 5
cd ..

cd T182M
qsub ../job_server_1A.sh
sleep 5
qsub ../job_server_1B.sh
sleep 5
qsub ../job_server_1C.sh
sleep 5
cd ..

cd S205T
qsub ../job_server_1A.sh
sleep 5
qsub ../job_server_1B.sh
sleep 5
qsub ../job_server_1C.sh
sleep 5
cd ..

cd L183P
qsub ../job_server_1A.sh
sleep 5
qsub ../job_server_1B.sh
sleep 5
qsub ../job_server_1C.sh
sleep 5
cd ..

