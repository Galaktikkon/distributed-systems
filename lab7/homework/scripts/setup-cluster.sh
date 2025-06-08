#!/bin/bash

BASE_DIR=$(pwd)/cluster
rm -rf "$BASE_DIR"
echo "Setting up ZooKeeper cluster in $BASE_DIR"
mkdir -p "$BASE_DIR"

for i in 1 2 3; do
    echo -ne "\rSetting up ZooKeeper instance $i..."

    NODE_DIR="$BASE_DIR/zk$i"
    DATA_DIR="$NODE_DIR/data"

    mkdir -p "$DATA_DIR"

    echo "$i" >"$DATA_DIR/myid"

    CLIENT_PORT=$((2180 + i))

    cat <<EOF >"$NODE_DIR/zoo.cfg"
tickTime=2000
initLimit=5
syncLimit=2
dataDir=$DATA_DIR
clientPort=$CLIENT_PORT
server.1=127.0.0.1:2888:3888
server.2=127.0.0.1:2889:3889
server.3=127.0.0.1:2890:3890
EOF

done
echo -e "\rZooKeeper cluster setup complete! "
