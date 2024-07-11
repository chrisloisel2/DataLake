#! /usr/bin/env bash

hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
  -input /liste.txt \
  -output /hadoop/mapred/output.ok \
  -mapper /hadoop/mapred/map.py \
  -reducer /hadoop/mapred/red.py \
  -file /hadoop/mapred/map.py\
  -file /hadoop/mapred/red.py
