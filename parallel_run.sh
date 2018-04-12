#!/usr/bin/env bash

total_run=$1
test=$2

DATE=`date '+%Y-%m-%d_%H-%M-%S'`
mkdir -p logs

for i in `seq 1 $total_run`;
do
    python main.py $2  2>&1 > logs/${DATE}_run_${i}.log &
done

echo Launched ${total_run} jobs.