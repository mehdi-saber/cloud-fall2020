#!/usr/bin/env bash
./mvnw  clean package
scp ./target/Matrix-1.0-SNAPSHOT.jar hadoopuser@192.168.56.106:~/test-mat/Matrix.jar
#scp -r ./test/ hadoopuser@192.168.56.106:~/test-mat/input/
ssh hadoopuser@192.168.56.106  'hdfs dfs -rm -skipTrash -r /user/hadoop/matrix/output &> /dev/null'
#ssh hadoopuser@192.168.56.106  'hdfs dfs -rm -skipTrash -r /user/hadoop/mat-input/ &> /dev/null'
#ssh hadoopuser@192.168.56.106  'hdfs dfs -copyFromLocal ~/test-mat/input/ /user/hadoop/input/'
ssh hadoopuser@192.168.56.106  'hadoop jar ~/test-mat/Matrix.jar Matrix /user/hadoop/input/ /user/hadoop/matrix/output'
ssh hadoopuser@192.168.56.106  'hdfs dfs -cat /user/hadoop/matrix/output/part-r-00000'