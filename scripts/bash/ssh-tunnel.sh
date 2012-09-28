#!/bin/bash

sshpass -p stack ssh -f -L 11111:172.31.0.2:22 stack@198.101.133.84 sleep 120
scp -i ~/workspace/alamoaio.pem -P 11111 ~/workspace/functions.sh ubuntu@localhost: