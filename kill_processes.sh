#!/bin/bash

sudo systemctl stop mongod

file='pids.txt'
while read line; do

	kill $line

done < pids.txt

rm pids.txt
