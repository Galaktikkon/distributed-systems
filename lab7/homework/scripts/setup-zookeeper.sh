#!/bin/bash
rm -rf apache-zookeeper
wget https://archive.apache.org/dist/zookeeper/zookeeper-3.8.4/apache-zookeeper-3.8.4-bin.tar.gz
tar -xzf apache-zookeeper-3.8.4-bin.tar.gz
rm apache-zookeeper-3.8.4-bin.tar.gz
mv apache-zookeeper-3.8.4-bin apache-zookeeper
mv apache-zookeeper/conf/zoo_sample.cfg apache-zookeeper/conf/zoo.cfg
