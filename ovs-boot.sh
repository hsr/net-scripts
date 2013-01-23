#!/bin/bash

function err() {
    if [ -z "$1" ] || [ -z "$2" ]; then
        return
    fi
    if [ "${1}" != "0" ]; then
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

    insmod datapath/linux/openvswitch.ko &> /dev/null
    err "$?" "Coudn't insert ovs mod. Maybe it is already there";
    mkdir -p /usr/local/etc/openvswitch &> /dev/null
    err "$?" "Ovs db directory exists ";
    ovsdb-tool create /usr/local/etc/openvswitch/conf.db \
        vswitchd/vswitch.ovsschema &> /dev/null
    err "$?" "Ovs db file exists";
    
    ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock \
                     --remote=db:Open_vSwitch,manager_options \
                     --private-key=db:SSL,private_key \
                     --certificate=db:SSL,certificate \
                     --bootstrap-ca-cert=db:SSL,ca_cert \
                     --pidfile --detach &> /dev/null
    err "$?" "ovsdb seems to be already running";
    
    ovs-vsctl --no-wait init &> /dev/null
    err "$?" "ovsdb seems to be already initialized";

    ovs-vswitchd --pidfile --detach &> /dev/null
    err "$?" "ovsdb seems to be already running";
    
    cd - &>/dev/null

fi
