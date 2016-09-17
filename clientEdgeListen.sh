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
set logFile="/users/jonganz/logs/clientEdge-throughput-`date +%m-%d-%y_%H:%M`.csv"
echo "Experiment started at `date +%m-%d-%y_%T`"
bwm-ng -o csv -F $logFile -t 100 &
set bwm=$!
sleep 120

foreach i ( 1 2 3 )
  cat $logFile | tail -20 | sed '/total/d' | sort -n -t';' -k 3 | tail -1 | awk -F';' '{print $2}' | tr -d " " > /users/jonganz/logs/which.interface.Edge
  scp /users/jonganz/logs/which.interface.Edge client:/users/jonganz/logs/which.interface.Client
  while !( -f /users/jonganz/logs/dropConnection.now )
  end
  set interface=`cat /users/jonganz/logs/which.interface.Edge`
  sudo ifconfig $interface down
  echo "$interface down at `date +%m-%d-%y_%T`" | tee -a $logFile
  if ( $i == 3 ) then
    sleep 110
  else
    sleep 175
  endif

  foreach interfaceFile ( which.interface.Edge which.interface.Client dropConnection.now )
    if ( -f /users/jonganz/logs/$interfaceFile ) then
      rm /users/jonganz/logs/$interfaceFile
    endif
  end

  sudo ifconfig $interface up
  echo "$interface back up at `date +%m-%d-%y_%T`" | tee -a $logFile
  sleep 5
end

sleep 20
kill -2 $bwm
echo "Experiment completed at `date +%m-%d-%y_%T`"
