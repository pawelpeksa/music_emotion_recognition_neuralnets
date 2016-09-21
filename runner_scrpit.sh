#!/bin/bash

for i in `seq 1 2`;
do	
	for j in `seq 1 5`;
	do
		python ./src/main.py -t -e -n 40 &
		python ./src/main.py -t -e -n 40 &
		python ./src/main.py -t -e -n 40 &
		wait
	done
done 


