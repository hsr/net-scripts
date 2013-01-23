#!/bin/bash

if [ ! -z "$1" ] && [ ! -z "$2" ] && [ ! -z "$3" ]; then

	netstat -st > $3_old.txt
	sudo tcpdump -s 68 -ni br0 -w /tmp/$3_tcpdump.pcap &
	PID=$!
	netperf -H $1 -l $2 -t TCP_STREAM > $3_netperf.txt
	sudo kill ${PID}
	netstat -st > $3_new.txt

	./netstat-tcp-parser.py $3_old.txt $3_new.txt > $3_netstat.txt
	cat $3_netperf.txt
	cat $3_netstat.txt
else
	echo "Missing parameters!"
	echo "Usage: $0 <ip> <length> <output prefix>"
fi
