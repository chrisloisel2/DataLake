#!/bin/bash

# Démarrer les services HDFS
$HADOOP_HOME/sbin/start-dfs.sh

# Démarrer les services YARN
$HADOOP_HOME/sbin/start-yarn.sh

# Garder le conteneur en exécution si nécessaire
tail -f /dev/null
