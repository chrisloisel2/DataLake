#!/bin/bash

# Démarrer le ResourceManager
$HADOOP_HOME/sbin/start-yarn.sh

# Démarrer le NodeManager
$HADOOP_HOME/sbin/yarn-daemon.sh start nodemanager

# Pause infinie pour maintenir le conteneur en vie
while true; do sleep 1000; done
