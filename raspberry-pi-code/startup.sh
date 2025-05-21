#!/bin/bash

export DISPLAY=:0
export XAUTHORITY=/home/tlp/.Xauthority
LOGFILE=/home/tlp/Teleprance/raspberry-pi-code/robot.log

echo "STARTING ROBOT SYSTEM..." >> $LOGFILE
date >> $LOGFILE

# Wait for X to be ready
until xset q > /dev/null 2>&1; do
    echo "Waiting for X display..." >> $LOGFILE
    sleep 2
done

cd /home/tlp/Teleprance/raspberry-pi-code || exit

echo "Starting Flask..." >> $LOGFILE
python main.py >> $LOGFILE 2>&1 &

sleep 5

echo "Starting ngrok..." >> $LOGFILE
ngrok http --url=telepresence.ngrok.app 5000 >> $LOGFILE 2>&1 &

sleep 5

echo "Launching browser..." >> $LOGFILE
chromium-browser --noerrdialogs --disable-infobars --kiosk https://telepresence.ngrok.app/monitor >> $LOGFILE 2>&1 &
