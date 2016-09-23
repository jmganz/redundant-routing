#!/bin/csh

echo "Executing server.sh"
cd /users/jonganz/installScripts
sudo route add -net 10.1.1.0/24 gw 10.1.9.3
sudo route add -net 10.1.2.0/24 gw 10.1.9.3
sudo route add -net 10.1.3.0/24 gw 10.1.9.3
sudo route add -net 10.1.4.0/24 gw 10.1.9.3
sudo route add -net 10.1.5.0/24 gw 10.1.9.3
sudo route add -net 10.1.6.0/24 gw 10.1.9.3
sudo route add -net 10.1.7.0/24 gw 10.1.9.3
sudo route add -net 10.1.8.0/24 gw 10.1.9.3
sudo route add -net 10.1.10.0/24 gw 10.1.9.3
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A FORWARD -p tcp --dport 80 -j ACCEPT
sudo sysctl -w net.ipv4.conf.all.proxy_arp=1

sudo dpkg -i /users/jonganz/installScripts/debs/libstatgrab10_0.91-1_amd64.deb
sudo dpkg -i /users/jonganz/installScripts/debs/bwm-ng_0.6-3.2build1_amd64.deb
sudo dpkg -i /users/jonganz/installScripts/debs/libiperf0_3.1.3-1_amd64.deb
sudo dpkg -i /users/jonganz/installScripts/debs/inetutils-traceroute_1.8-6_amd64.deb
sudo dpkg -i /users/jonganz/installScripts/debs/iperf3_3.1.3-1_amd64.deb
sleep 1
/usr/bin/iperf3 -s -B 10.1.9.2 &
echo "server.sh Finished"
