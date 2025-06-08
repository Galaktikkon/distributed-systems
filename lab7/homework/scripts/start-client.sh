#!/bin/bash

BIN_DIR="$(pwd)/apache-zookeeper/bin"

konsole --noclose -e $BIN_DIR/zkCli.sh -server 127.0.0.1:2181
