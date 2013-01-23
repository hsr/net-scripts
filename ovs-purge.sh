#!/bin/bash

function err() {
    if [ -z "$1" ] || [ -z "$2" ]; then
        return
    fi
    if [ ! -z ${1} ]; then
        shift
        echo "${@}"
    fi
}

if [ -z "$1" ]; then
    echo "Usage: $0 <OVS_PATH>"
    echo ""
    echo "Where OVS_PATH is the path where openvswitch was extracted"
    echo "and compiled."
    exit 1
else
    OVS_PATH=${1}

    cd ${OVS_PATH}

    OVS_PIDS=$(pgrep ovs)
    for P in ${OVS_PIDS}; do
        [ "${P}" != "${BASHPID}" ] && kill ${P}
    done

    [ ! -z "$(lsmod | grep brcompat)" ] && rmmod brcompat_mod &> /dev/null

    [ ! -z "$(lsmod | grep openvswitch)" ] && rmmod openvswitch &> /dev/null

    cd - &>/dev/null
fi
