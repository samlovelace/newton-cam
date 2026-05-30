#!/bin/bash
#
source ~/rover-env/bin/activate

uvicorn stream:app --host 0.0.0.0 --port 8000 &
UVICORN_PID=$!

ngrok http 8000

kill $UVICORN_PID
