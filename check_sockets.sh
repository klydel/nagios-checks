#!/bin/bash
#simple bash shell script to get total sockets and open files for a system
#need to source your nagios utils.sh for use
. /usr/share/nagios/libexec/utils.sh
sockinfo=`cat /proc/net/sockstat | grep sockets`
openfiles=`sudo /usr/sbin/lsof | wc -l`
printf "OK - $sockinfo openfiles: $openfiles | socketsUsed=`echo $sockinfo | awk '{print $3}'`;openfiles=$openfiles"
exit $STATE_OK
