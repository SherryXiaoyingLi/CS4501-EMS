#!/usr/bin/env bash

# install pymysql to spark-worker
docker exec -it spark-worker bash -c "chmod +x /tmp/data/install_pymysql.sh && /tmp/data/install_pymysql.sh" &&

# run automate-recommendation.sh to install mysql and run the spark job for spark-master
docker exec -it spark-master bash -c "chmod +x /tmp/data/automate-recommendation.sh && /tmp/data/automate-recommendation.sh"