#!/bin/bash

BIN_DIR="$(pwd)/apache-zookeeper/bin"
CLUSTER_DIR="$(pwd)/cluster"

for i in 1 2 3; do
    echo "Starting ZooKeeper instance $i..."
    $BIN_DIR/zkServer.sh start "$CLUSTER_DIR/zk$i/zoo.cfg"
done
