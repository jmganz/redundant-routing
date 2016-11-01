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
touch /users/jonganz/logs/start.client
scp /users/jonganz/logs/start.client clientEdge:/users/jonganz/logs/start.edge
set rightNow=`date +%s`
set logFile="/users/jonganz/logs/client-throughput-$rightNow.csv"
echo "Experiment started at `date +%s`"
bwm-ng -o csv -F $logFile -t 100 &
set bwm=$!
sleep 20

/usr/bin/iperf3 -c server -f m -t 600 --logfile /users/jonganz/logs/iperf3-client-log-$rightNow.log &
echo "iperf started at `date +%s`" | tee -a $logFile
sleep 110

foreach i ( 1 2 3 )
  sleep 5
  while !( -f /users/jonganz/logs/which.interface.Client )
  end
  set interface=`cat /users/jonganz/logs/which.interface.Edge`
  scp /users/jonganz/logs/which.interface.Client clientEdge:/users/jonganz/logs/dropConnection.now
  echo "$interface down at `date +%s`" | tee -a $logFile
  if ( $i == 3 ) then
    sleep 110
  else
    sleep 175
  endif
  echo "$interface back up at `date +%s`" | tee -a $logFile
end

sleep 25

foreach interfaceFile ( which.interface.Edge which.interface.Client dropConnection.now start.edge )
  if ( -f /users/jonganz/logs/$interfaceFile ) then
    rm /users/jonganz/logs/$interfaceFile
  endif
end

kill -2 $bwm
echo "Experiment completed at `date +%l:%M`"
tail -5 /users/jonganz/logs/iperf3-client-log-$rightNow.log
