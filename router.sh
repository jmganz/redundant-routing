#!/bin/csh

echo "Executing router.sh"
cd /users/jonganz
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A FORWARD -p tcp --dport 80 -j ACCEPT
sudo sysctl -w net.ipv4.conf.all.proxy_arp=1

sudo dpkg -i /users/jonganz/old-debs/libstatgrab10_0.91-1_amd64.deb
sudo dpkg -i /users/jonganz/old-debs/bwm-ng_0.6-3.2build1_amd64.deb
echo "router.sh Finished"
