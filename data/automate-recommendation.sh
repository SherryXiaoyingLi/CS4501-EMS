#!/usr/bin/env bash

# install mysql
chmod +x /tmp/data/install_pymysql.sh &&
/tmp/data/install_pymysql.sh &&

# run spark job
# have a while loop that runs every minute
bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/recommendation.py
