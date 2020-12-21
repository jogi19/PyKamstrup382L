#!/bin/bash
stty 300  -F /dev/ttyUSB1 1:4:da7:a30:3:1c:7f:15:4:10:0:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0


( sleep 1; echo -e "\x2f\x3f\x21\x0d\x0a" > /dev/ttyUSB1 ) &
#sende "/?!" mit Return an Raspi (Udo's Erweiterung + IR-Kopf seriell)
while read -t8 line
do
    echo $line # > /home/pi/lgread.log
done < /dev/ttyUSB1

exit


