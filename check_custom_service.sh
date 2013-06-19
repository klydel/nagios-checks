#!/bin/bash
#bash script to get res mem, virtmem, cpupercent, mempercent of a process
#sums all children pids as well
#usage: ./check_custom_service $user $anyARGSofpid $memoryMB $VirtMemoryMB $CPUpercent $MEMpercent
#./check_custom_service.sh www-data httpd 600 1024 85 85
#example output:
#OK - RESMEM=230MB:VIRTMEM=858MB:USEDCPU=9.4%:USEDMEM=13.8% 
#need utils.sh from nagios plugins
. /opt/nagios/plugins/utils.sh
MXMEM=$3
MXVIRT=$4
MXCPUP=$5
MXMEMP=$6
function warn {
	 echo "WARNING - $WARNIN - RESMEM:$USEDMEMR mb, VIRTMEM:$USEDVIRTR mb, USEDCPU:${USEDCPUP}%, USEDMEM:${USEDMEMP}% | RESMEM=${USEDMEMR};VIRTMEM=${USEDVIRTR};USEDCPU=${USEDCPUP}%;USEDMEM=${USEDMEMP}%;"
	 exit $STATE_WARNING
}
ERROR=""
#if user, check log for exceptions, you can add more
if [ "$1" == "mycustomjvmuser" ]
   then
	EXCEP=`tail -n 2 /opt/$1/logs/service.log | grep "Exception" | wc -l`
	if [[ "$EXCEP" -gt "0" ]]
	   then
             echo "WARNING - $1 Exception Found: `tail -n 2 /opt/$1/logs/service.log | grep 'Exception'`" ; exit $STATE_WARNING ; fi;
	fi

PT=()
PT+=(`ps -o pid,user,rss,vsize,%cpu,%mem,ucomm,args -u $1 --no-heading | grep $2 | awk '{print $1}'`)
if [ ${#PT[@]} -gt 0 ] ;then true; else echo  "CRITICAL - No Process Running with args: $2" ; exit $STATE_CRITICAL; fi;
USEDMEMR="0"
USEDVIRTR="0"
USEDCPUP="0.0"
USEDMEMP="0.0"
for i in "${PT[@]}"
do
  OT=`ps -o pid,user,rss,vsize,%cpu,%mem,ucomm -p $i --no-heading`
  if [ -n "$OT" ] ; then true; else echo "CRITICAL - No Process Running with args: $2" ; exit $STATE_CRITICAL; fi;
  APP=(`echo $OT | awk '{print $3,$4,$5,$6}' `)
  USEDMEM=$(( $USEDMEM + ${APP[0]}))
  USEDVIRT=$(( $USEDVIRT + ${APP[1]}))
  USEDCPUP=$( echo $USEDCPUP + ${APP[2]} | bc )
  USEDMEMP=$( echo $USEDMEMP + ${APP[3]} | bc )
done
USEDMEMR=$(($USEDMEM/1024))
USEDVIRTR=$(($USEDVIRT/1024))
 if [[ "$USEDMEMR" -gt "$MXMEM" ]] 
  then
      WARNIN="Memory Usage High"
      warn
  elif  [[ "$USEDVIRTR" -gt "$MXVIRT" ]]
  then
      WARNIN="Virtual Memory Usage High"
      warn

  elif [[ `echo $USEDCPUP'>'$MXCPUP | bc -l` -gt 0 ]]
  then
      WARNIN="Used CPU % High"
      warn

  elif [[ `echo $USEDMEMP'>'$MXMEMP | bc -l` -gt 0 ]]
  then
      WARNIN="Used Memory % High"
      warn
  else
      STAT="RESMEM=${USEDMEMR}MB;VIRTMEM=${USEDVIRTR}MB;USEDCPU=${USEDCPUP}%;USEDMEM=${USEDMEMP}%"
      echo "OK - $STAT |$STAT\n"
      exit $STATE_OK
  fi
