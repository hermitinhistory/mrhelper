#!/bin/sh
set -e
set -u


cd `dirname "$0"`


wordfile='word.txt'
cat $wordfile | name=yp ./mr_m_wc.py | sort | name=yp ./mr_r_wc.py


hadoop_home='/home/hadoop/hadoop/hadoop/'
streaming=$hadoop_home/contrib/streaming/hadoop-0.20.2-streaming.jar


inputdir=/tmp/
input=$inputdir/$wordfile
output='/tmp/test-mrhelper-output'

hadoop fs -rm $input || true
hadoop fs -put $wordfile $inputdir
hadoop fs -rmr $output || true

jobprefix=test-yp

mrhelperfile=./mrhelper.py
mapperfile=./mr_m_wc.py
reducerfile=./mr_r_wc.py

hadoop jar $streaming -D mapred.job.name=$jobprefix-wc \
-D mapred.reduce.tasks=3 \
-file $mrhelperfile \
-file $mapperfile -mapper $mapperfile \
-file $reducerfile -reducer $reducerfile \
-input $input \
-output $output \
-cmdenv name=yp


hadoop fs -ls $output
hadoop fs -get $output ./hohohohoho
cat ./hohohohoho/*
rm -rf ./hohohohoho
