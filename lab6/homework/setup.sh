#!/bin/bash

konsole --noclose -e python3 src/admin/main.py admin &
konsole --noclose -e python3 src/supplier/main.py supplier1 tlen,buty &
konsole --noclose -e python3 src/supplier/main.py supplier2 tlen,plecak &
konsole --noclose -e python3 src/team/main.py team1 &
konsole --noclose -e python3 src/team/main.py team2 &
