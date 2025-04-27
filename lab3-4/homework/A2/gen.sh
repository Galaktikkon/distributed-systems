#!/bin/bash

mkdir -p server/gen
python \
    -m grpc_tools.protoc -I=proto --python_out=server/gen \
    --grpc_python_out=server/gen proto/run.proto

mkdir -p client/gen
protoc \
  --proto_path=proto \
  --java_out=client/src/main/java \
  --grpc-java_out=client/src/main/java \
  proto/run.proto

