#!/usr/bin/env bash

# install mysql
chmod +x /tmp/data/install_pymysql.sh &&
/tmp/data/install_pymysql.sh &&

# run spark job
# have a while loop that runs every two minutes
# code based on https://stackoverflow.com/questions/25157642/how-to-repeatedly-run-bash-script-every-n-seconds
while bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/recommendation.py; do sleep 120; done
