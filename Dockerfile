# Définir l'image de base
FROM ubuntu:20.04

ENV HADOOP_VERSION=3.4.0

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y openjdk-11-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which javac)))) && \
    echo "JAVA_HOME=$JAVA_HOME" >> /etc/environment


# Installer les dépendances nécessaires
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y openjdk-11-jdk curl ssh pdsh net-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV HADOOP_VERSION=3.4.0 \
    HADOOP_HOME=/usr/local/hadoop \
    PATH=$PATH:/usr/local/hadoop/bin:/usr/local/hadoop/sbin \
    JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64

ENV HDFS_NAMENODE_USER=hadoop \
    HDFS_DATANODE_USER=hadoop \
    HDFS_SECONDARYNAMENODE_USER=hadoop \
    YARN_RESOURCEMANAGER_USER=hadoop \
    YARN_NODEMANAGER_USER=hadoop


RUN curl -L -o hadoop-$HADOOP_VERSION.tar.gz https://dlcdn.apache.org/hadoop/common/hadoop-3.4.0/hadoop-3.4.0.tar.gz && \
    tar -xzvf hadoop-$HADOOP_VERSION.tar.gz && \
    mv hadoop-$HADOOP_VERSION $HADOOP_HOME && \
    rm hadoop-$HADOOP_VERSION.tar.gz

# Configurer SSH sans mot de passe pour localhost
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

# Après l'installation de Hadoop dans le Dockerfile
COPY config/core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml
COPY config/hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml
COPY config/yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml

# Copier le script de démarrage en tant que root
COPY start-hadoop.sh /usr/local/bin/start-hadoop.sh

COPY start-yarn.sh /usr/local/bin/start-yarn.sh

# Changer les permissions du script avant de changer d'utilisateur
RUN chmod +x /usr/local/bin/start-hadoop.sh

# Créer l'utilisateur hadoop et son groupe (si ce n'est pas déjà fait)
RUN groupadd -r hadoop && useradd -r -g hadoop -d /home/hadoop -m hadoop

# Changer le propriétaire des répertoires Hadoop pour l'utilisateur hadoop (si nécessaire)
RUN chown -R hadoop:hadoop $HADOOP_HOME /usr/local/bin/start-hadoop.sh

# Passer à l'utilisateur hadoop pour les commandes suivantes
USER hadoop

# Exposer les ports nécessaires pour Hadoop
EXPOSE 9870 8088 9000

# Copier le script de démarrage
COPY start-hadoop.sh /usr/local/bin/

CMD ["/usr/local/bin/start-hadoop.sh"]
