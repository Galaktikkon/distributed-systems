#!/bin/bash

BIN_DIR="$(pwd)/apache-zookeeper/bin"

if [ ! -d "$BIN_DIR" ]; then
    echo "Error: Apache ZooKeeper binary directory not found at $BIN_DIR"
    exit 1
fi

CLUSTER_DIR="$(pwd)/cluster"

if [ ! -d "$CLUSTER_DIR" ]; then
    echo "Error: Cluster directory not found at $CLUSTER_DIR"
    exit 1
else
    for i in 1 2 3; do
        echo "Stopping ZooKeeper instance $i..."
        $BIN_DIR/zkServer.sh stop "$CLUSTER_DIR/zk$i/zoo.cfg"
    done
fi
