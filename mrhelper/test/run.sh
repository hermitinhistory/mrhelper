#!/bin/sh
set -e
set -u


cd `dirname "$0"`


wordfile='word.txt'
cat $wordfile | name=yp ./mr_m_wc.py | sort | name=yp ./mr_r_wc.py


streaming=/data/clusterserver/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.4.jar

root_dir=/tmp/
input=$root_dir/$wordfile
output=$root_dir/test_mrhelper_output

hadoop fs -rm -r $input $output || true
hadoop fs -put $wordfile $root_dir

jobprefix=test_yp

mrhelperfile=./mrhelper.py
mapperfile=./mr_m_wc.py
reducerfile=./mr_r_wc.py

hadoop jar $streaming -D mapred.job.name=${jobprefix}_wc \
-D mapred.reduce.tasks=3 \
-file $mrhelperfile \
-file $mapperfile -mapper $mapperfile \
-file $reducerfile -reducer $reducerfile \
-input $input \
-output $output \
-cmdenv name=yp


hadoop fs -ls $output
hadoop fs -cat $output/* | sort
