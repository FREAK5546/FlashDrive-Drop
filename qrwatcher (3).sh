#!/bin/bash
while true; do
    if ! lsof -i:8080 > /dev/null 2>&1; then
        nohup python3 /home/joe/fileserver.py > /home/joe/server.log 2>&1 &
    fi
    if [ -f /home/joe/show_qr_trigger ]; then
        rm /home/joe/show_qr_trigger
        python3 /home/joe/showqr.py
    fi
    sleep 2
done
