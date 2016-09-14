#!/bin/csh

#print `date +%m-%d-%y_%H:%M`
set logFile="clientEdge-throughput-`date +%m-%d-%y_%H:%M`.csv"
bwm-ng -o csv -F $logFile -t 100 &
set bwm=$!
sleep 10

while !( -f dropConnection.now )
end
set interface=`cat dropConnection.now`
sudo ifconfig $interface down
echo "$interface down at `date +%m-%d-%y_%H:%M`" | tee -a $logFile
rm dropConnection.now
sleep 60
sudo ifconfig $interface up
echo "$interface back up at `date +%m-%d-%y_%H:%M`" | tee -a $logFile
while !( -f dropConnection.now )
end
set interface=`cat dropConnection.now`
sudo ifconfig $interface down
echo "$interface down at `date +%m-%d-%y_%H:%M`" | tee -a $logFile
rm dropConnection.now
sleep 60
sudo ifconfig $interface up
echo "$interface back up at `date +%m-%d-%y_%H:%M`" | tee -a $logFile
while !( -f dropConnection.now )
end
set interface=`cat dropConnection.now`
sudo ifconfig $interface down
echo "$interface down at `date +%m-%d-%y_%H:%M`" | tee -a $logFile
rm dropConnection.now
sleep 60
sudo ifconfig $interface up
echo "$interface back up at `date +%m-%d-%y_%H:%M`" | tee -a $logFile
sleep 70
kill -2 $bwm



#wget server &
#wget=$!
#echo $wget
#sleep 10
#while kill -0 $wget 2> /dev/null
#do
#  sleep 10
#done
#sleep 10
#kill -2 $bwm
