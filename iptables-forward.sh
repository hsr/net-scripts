#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
    echo "Usage: $0 <input iface> <input port> <output ip> <output port>"
    exit 1
else
    IFACE=${1}
    IPORT=${2}
    OADDR=${3}
    OPORT=${4}

    sudo iptables -t nat -A PREROUTING -p tcp -i ${IFACE} --dport ${IPORT} \
        -j DNAT --to-destination ${OADDR}:${OPORT}

    sudo iptables -A FORWARD -p tcp -d ${OADDR} --dport ${OPORT} \
        -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT

fi
