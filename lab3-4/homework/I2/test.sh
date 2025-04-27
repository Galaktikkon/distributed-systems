#!/bin/bash
cd client
for i in {1..20}
do
  python3 main.py Dedicated$i &
done
wait