#!/usr/bin/env python
# simple script to pull INFO command from redis
# usage: get_redis_stats.py redis.blah.com 6379
#OK - connected_clients:149,used_cpu_sys:21958.38,keyspace_misses:37416922,used_memory:17703624,rejected_connections:0,blocked_clients:4,used_memory_lua:31744,instantaneous_ops_per_sec:125,used_memory_rss:22880256,used_cpu_user:7928.96,latest_fork_usec:9608,mem_fragmentation_ratio:1.29,rdb_last_bgsave_time_sec:0, | connected_clients=149;used_cpu_sys=21958.38;keyspace_misses=37416922;used_memory=17703624;rejected_connections=0;blocked_clients=4;used_memory_lua=31744;instantaneous_ops_per_sec=125;used_memory_rss=22880256;used_cpu_user=7928.96;latest_fork_usec=9608;mem_fragmentation_ratio=1.29;rdb_last_bgsave_time_sec=0;

import socket
import sys
host = sys.argv[1]
port = int(sys.argv[2])
command = "INFO"
METRIC = [
   "connected_clients",
   "used_memory",
   "used_memory_lua",
   "instantaneous_ops_per_sec",
   "latest_fork_usec",
   "used_memory_rss",
   "blocked_clients",
   "rejected_connections",
   "mem_fragmentation_ratio",
   "rdb_last_bgsave_time_sec",
   "rdb_changes_since_last_save"
   "keyspace_hits",
   "keyspace_misses",
   "used_cpu_sys",
   "used_cpu_user"
]
MAXTHRESHOLDS= {
   "connected_clients": 500,
   "used_memory": 95997896,
   "used_memory_lua": 100000,
   "instantaneous_ops_per_sec": 500,
   "latest_fork_usec": 100000,
   "used_memory_rss": 95997896,
   "blocked_clients": 100,
   "rejected_connections": 100,
   "mem_fragmentation_ratio": 2.0,
   "rdb_last_bgsave_time_sec": 5,
   "rdb_changes_since_last_save": 20000
   }
totals = {}
warnings = []

def nagios_report(totals, warnings):
   if warnings:
      msg = [  k+":"+str(v)+"," for k,v in totals.iteritems()]
      perf = [  k+"="+str(v)+";" for k,v in totals.iteritems()]
      print "WARNING -%s is warning- %s | %s" % ( ','.join(warnings), ''.join(msg), ''.join(perf))
      sys.exit(1)
   else:
      msg = [  k+":"+str(v)+"," for k,v in totals.iteritems()]
      perf = [  k+"="+str(v)+";" for k,v in totals.iteritems()]
      print "OK - %s | %s" % ( ''.join(msg), ''.join(perf))
      sys.exit(0)

def redis_connect(host, port, command):
    redis = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    redis.settimeout(5)
    redis.connect((host, port))
    redis.sendall(command)
    data = redis.recv(4096)
    redis.close()
    return data

def format_data(data):
    for line in data.split("\n"):

        if ":" in line and line.split(":")[0] in METRIC:
            mname = line.split(":")[0]
            mval = line.split(":")[1].strip()
            totals[mname] = mval
            if mname in MAXTHRESHOLDS and float(mval) > MAXTHRESHOLDS[mname]:
                warnings.append(mname) 
    return totals

if __name__ == '__main__':
   data = redis_connect(host, port, command + "\r\n\r\n")
   nagios_report(format_data(data), warnings)

