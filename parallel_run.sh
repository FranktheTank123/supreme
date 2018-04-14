#!/usr/bin/env bash

total_run=$1
if [ -z "$2" ] || [ $2 != "test" ]; then
    TEST=""
else
    TEST="--test"
fi

python main.py $TEST -m monitor&
for i in `seq 1 $total_run`;
do
    python main.py $TEST -m shop&
done
