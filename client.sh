#!/bin/csh

echo "Executing client.sh"
cd /users/jonganz
sudo route add -net 10.1.1.0/24 gw 10.1.3.3
sudo route add -net 10.1.2.0/24 gw 10.1.3.3
sudo route add -net 10.1.4.0/24 gw 10.1.3.3
sudo route add -net 10.1.5.0/24 gw 10.1.3.3
sudo route add -net 10.1.6.0/24 gw 10.1.3.3
sudo route add -net 10.1.7.0/24 gw 10.1.3.3
sudo route add -net 10.1.8.0/24 gw 10.1.3.3
sudo route add -net 10.1.9.0/24 gw 10.1.3.3
sudo route add -net 10.1.10.0/24 gw 10.1.3.3
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A FORWARD -p tcp --dport 80 -j ACCEPT
sudo sysctl -w net.ipv4.conf.all.proxy_arp=1

sudo dpkg -i /users/jonganz/old-debs/libstatgrab10_0.91-1_amd64.deb
sudo dpkg -i /users/jonganz/old-debs/bwm-ng_0.6-3.2build1_amd64.deb
sudo dpkg -i /users/jonganz/old-debs/libiperf0_3.1.3-1_amd64.deb
sudo dpkg -i /users/jonganz/old-debs/iperf3_3.1.3-1_amd64.deb
sudo dpkg -i /users/jonganz/old-debs/inetutils-traceroute_1.8-6_amd64.deb
echo "client.sh Finished"
