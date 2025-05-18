#!/bin/bash
cd "$(dirname "$0")"
nohup python3 main.py > flask.log 2>&1 &
echo "Flask app started in background. Logs: flask.log"
