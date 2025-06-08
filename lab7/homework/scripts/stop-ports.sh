#!/bin/bash

PORTS=(2181 2182 2183)
for PORT in "${PORTS[@]}"; do
    PID=$(lsof -ti :$PORT)
    echo "Killing process on port $PORT..."
    if [ -n "$PID" ]; then
        kill -9 $PID
        echo "Process on port $PORT killed."
    else
        echo "No process found on port $PORT."
    fi
done
