#!/bin/bash

cd $(dirname $0)/..
source bin/activate
cd lstm
curl -o config.yaml http://169.254.169.254/latest/user-data/
while true; do
    python char_lstm.py config.yaml 2>>char_lstm.log >/dev/null
    sleep 5
done
