#!/bin/bash
#simple script to check write / read count/latency for a cassandra server.
#warpper for nodeprobe

#source nagios util helper for exits
. /opt/nagios/libexec/utils.sh

rwstats=(`/opt/nagios/libexec/nodeprobe -host 127.0.0.1 -port 20645 cfstats | awk '/Profile/,EOF' | tr '\n' ' '`)
read_count=${rwstats[4]}
read_latency=${rwstats[7]}
write_count=${rwstats[11]}
write_latency=${rwstats[14]}

if [ -z "$read_count" ] ; then
    printf "Something is wrong" 
    exit $STATE_WARNING
fi
printf "Read_Count:$read_count, Read_Latency: $read_latency ms, Write_Count: $write_count, Write_Latency: $write_latency ms | Read_Count=$read_count;Read_Latency=${read_latency}ms;Write_Count=$write_count;Write_Latency=${write_latency}ms;" 

exit $STATE_OK
