#!/bin/csh

set logFile="clientEdge-throughput-`date +%m-%d-%y_%H:%M`.csv"
bwm-ng -o csv -F $logFile -t 100 &
set bwm=$!
sleep 30

cat $logFile | tail -20 | sed '/total/d' | sort -n -t';' -k 3 | tail -1 | awk -F';' '{print $2}' | tr -d " " > which.interface
scp which.interface client:/users/jonganz/which.interface
while !( -f dropConnection.now )
end
set interface=`cat dropConnection.now`
sudo ifconfig $interface down
echo "$interface down at `date +%m-%d-%y_%H:%M`" | tee -a $logFile
rm dropConnection.now
rm which.interface
sleep 60
sudo ifconfig $interface up
echo "$interface back up at `date +%m-%d-%y_%H:%M`" | tee -a $logFile
sleep 50
cat $logFile | tail -20 | sed '/total/d' | sort -n -t';' -k 3 | tail -1 | awk -F';' '{print $2}' | tr -d " " > which.interface
scp which.interface client:/users/jonganz/which.interface
while !( -f dropConnection.now )
end
set interface=`cat dropConnection.now`
sudo ifconfig $interface down
echo "$interface down at `date +%m-%d-%y_%H:%M`" | tee -a $logFile
rm dropConnection.now
rm which.interface
sleep 60
sudo ifconfig $interface up
echo "$interface back up at `date +%m-%d-%y_%H:%M`" | tee -a $logFile
sleep 50
cat $logFile | tail -20 | sed '/total/d' | sort -n -t';' -k 3 | tail -1 | awk -F';' '{print $2}' | tr -d " " > which.interface
scp which.interface client:/users/jonganz/which.interface
while !( -f dropConnection.now )
end
set interface=`cat dropConnection.now`
sudo ifconfig $interface down
echo "$interface down at `date +%m-%d-%y_%H:%M`" | tee -a $logFile
rm dropConnection.now
rm which.interface
sleep 60
sudo ifconfig $interface up
echo "$interface back up at `date +%m-%d-%y_%H:%M`" | tee -a $logFile
sleep 70
kill -2 $bwm
