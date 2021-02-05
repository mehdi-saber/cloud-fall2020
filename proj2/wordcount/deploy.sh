#!/usr/bin/env bash
./mvnw  clean package
scp ./target/WordCount-1.0-SNAPSHOT.jar hadoopuser@192.168.56.106:~/test/WordCount.jar
scp ./test.txt hadoopuser@192.168.56.106:~/test/test.txt
ssh hadoopuser@192.168.56.106  'hdfs dfs -rm -skipTrash -r /user/hadoop/wordcount/output2 &> /dev/null'
ssh hadoopuser@192.168.56.106  'hdfs dfs -rm -skipTrash -r /user/hadoop/test2.txt &> /dev/null'
ssh hadoopuser@192.168.56.106  'hdfs dfs -copyFromLocal ~/test/test.txt /user/hadoop/test2.txt'
ssh hadoopuser@192.168.56.106  'hadoop jar ~/test/WordCount.jar WordCount /user/hadoop/test2.txt /user/hadoop/wordcount/output2'
ssh hadoopuser@192.168.56.106  'hdfs dfs -cat /user/hadoop/wordcount/output2/part-r-00000'