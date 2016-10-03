#!/bin/csh

if !( -d /users/jonganz/logs ) then
  mkdir /users/jonganz/logs
endif

foreach interfaceFile ( which.interface.Edge which.interface.Client dropConnection.now start.edge )
  if ( -f /users/jonganz/logs/$interfaceFile ) then
    rm /users/jonganz/logs/$interfaceFile
  endif
end

cd /users/jonganz
while !( -f /users/jonganz/logs/start.edge )
end
set logFile="/users/jonganz/logs/clientEdge-throughput-`date +%s`.csv"
echo "Experiment started at `date +%s`"
bwm-ng -o csv -F $logFile -t 100 &
set bwm=$!
sleep 120

foreach i ( 1 2 3 )
  set activeInterfaceLine=`cat $logFile | tail -300 | sed '/total/d' | sed '/lo/d' | sort -n -t';' -k 3 | tail -1`
  set activeInterface=`echo $activeInterfaceLine | awk -F';' '{print $2}'`
  set activeSpeed=`echo $activeInterfaceLine | awk -F';' '{print $3}'`
  echo "found $activeInterface with speed $activeSpeed bytes/sec"
  echo $activeInterface > /users/jonganz/logs/which.interface.Edge
  scp /users/jonganz/logs/which.interface.Edge client:/users/jonganz/logs/which.interface.Client
  while !( -f /users/jonganz/logs/dropConnection.now )
  end
  set interface=`cat /users/jonganz/logs/which.interface.Edge`
  sudo ifconfig $interface down
  echo "$interface down at `date +%s`" | tee -a $logFile
  if ( $i == 3 ) then
    sleep 110
  else
    sleep 175
  endif

  foreach interfaceFile ( which.interface.Edge which.interface.Client dropConnection.now start.edge )
    if ( -f /users/jonganz/logs/$interfaceFile ) then
      rm /users/jonganz/logs/$interfaceFile
    endif
  end

  sudo ifconfig $interface up
  echo "$interface back up at `date +%s`" | tee -a $logFile
  sleep 5
end

sleep 20
kill -2 $bwm
echo "Experiment completed at `date +%s`"
