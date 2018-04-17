#!/bin/bash
mysql -uroot -p'$3cureUS' -h db -e "drop database cs4501; create database cs4501 character set utf8;"
