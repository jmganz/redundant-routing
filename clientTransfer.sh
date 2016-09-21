#!/bin/csh

if !( -d /users/jonganz/logs ) then
  mkdir /users/jonganz/logs
endif

foreach interfaceFile ( which.interface.Edge which.interface.Client dropConnection.now )
  if ( -f /users/jonganz/logs/$interfaceFile ) then
    rm /users/jonganz/logs/$interfaceFile
  endif
end

cd /users/jonganz
scp /users/jonganz/logs/start.client clientEdge:/users/jonganz/logs/start.edge
set logFile="/users/jonganz/logs/client-throughput-`date +%m-%d-%y_%H:%M`.csv"
echo "Experiment started at `date +%m-%d-%y_%T`"
bwm-ng -o csv -F $logFile -t 100 &
set bwm=$!
sleep 20

/usr/bin/iperf3 -c server -t 600 --logfile /users/jonganz/logs/iperf3-client-log-`date +%m-%d-%y_%H:%M`.log &
sleep 110

foreach i ( 1 2 3 )
  sleep 5
  while !( -f /users/jonganz/logs/which.interface.Client )
  end
  set interface=`cat /users/jonganz/logs/which.interface.Edge`
  scp /users/jonganz/logs/which.interface.Client clientEdge:/users/jonganz/logs/dropConnection.now
  echo "$interface down at `date +%m-%d-%y_%T`" | tee -a $logFile
  if ( $i == 3 ) then
    sleep 110
  else
    sleep 175
  endif
  echo "$interface back up at `date +%m-%d-%y_%T`" | tee -a $logFile
end

sleep 25

foreach interfaceFile ( which.interface.Edge which.interface.Client dropConnection.now )
  if ( -f /users/jonganz/logs/$interfaceFile ) then
    rm /users/jonganz/logs/$interfaceFile
  endif
end

kill -2 $bwm
echo "Experiment completed at `date +%m-%d-%y_%T`"
