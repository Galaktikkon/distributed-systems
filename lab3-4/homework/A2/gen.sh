#!/bin/bash

mkdir -p server/gen
python \
    -m grpc_tools.protoc -I=proto --python_out=server/gen \
    --grpc_python_out=server/gen proto/run.proto

mkdir -p client/gen
cd client
npx grpc_tools_node_protoc \
  --proto_path=../proto \
  --js_out=import_style=commonjs,binary:./gen \
  --grpc_out=grpc_js:./gen \
  --plugin=protoc-gen-ts=./node_modules/.bin/protoc-gen-ts \
  --ts_out=grpc_js:./gen \
  ../proto/run.proto

cd ..