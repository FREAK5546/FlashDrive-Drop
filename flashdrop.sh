#!/bin/bash
exec > /home/joe/flashdrop.log 2>&1
sleep 3
nmcli device wifi hotspot ifname wlp1s0 ssid "FileDrop" password "12345678"
sleep 2
sudo rm -f /home/joe/qr.png
qrencode -o /home/joe/qr.png "http://10.42.0.1:8080"
touch /home/joe/show_qr_trigger
