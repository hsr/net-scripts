#!/bin/bash
sudo iptables -Z
sudo iptables -F
sudo iptables -A FORWARD -o eth0 -i br0 -s 192.168.0.0/16 -m conntrack --ctstate NEW -j ACCEPT
sudo iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A POSTROUTING -t nat -j MASQUERADE
sudo iptables-save | sudo tee /etc/iptables.sav
sudo iptables-restore < /etc/iptables.sav
sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
