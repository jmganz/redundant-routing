#!/bin/csh

#print `date +%m-%d-%y_%H:%M`
cd /users/jonganz
set logFile="client-throughput-`date +%m-%d-%y_%H:%M`.csv"
bwm-ng -o csv -F $logFile -t 50 &
set bwm=$!
sleep 10

iperf3 -c server -t 600 --logfile iperf3-client-log-`date +%m-%d-%y_%H:%M`.log &
sleep 120
set interface=`cat which.interface`
cp which.interface dropConnection.now
echo "$interface down at `date +%m-%d-%y_%H:%M`" | tee -a $logFile
sleep 60
echo "$interface back up at `date +%m-%d-%y_%H:%M`" | tee -a $logFile
sleep 120
set interface=`cat which.interface`
cp which.interface dropConnection.now
echo "$interface down at `date +%m-%d-%y_%H:%M`" | tee -a $logFile
sleep 60
echo "$interface back up at `date +%m-%d-%y_%H:%M`" | tee -a $logFile
sleep 120
set interface=`cat which.interface`
cp which.interface dropConnection.now
echo "$interface down at `date +%m-%d-%y_%H:%M`" | tee -a $logFile
sleep 60
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
