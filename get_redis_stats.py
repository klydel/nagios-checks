#!/usr/bin/env python
# simple script to pull INFO command from redis
# usage: get_redis_stats.py myhost.mydomain.com 6379
#gets connected_clients, used_memory, used_memory_lua, instantaneous_ops_per_sec, instantaneous_ops_per_sec, latest_fork_usec, used_memory_rss, blocked_clients, rejected_connections
# possible slower: client_biggest_input_buf, blocked_clients, client_longest_output_list

import socket
import sys
host = sys.argv[1]
port = int(sys.argv[2])
command = "INFO"

def nagios_report(d):
    msg = "connected_clients:%s,blocked_clients:%s,rejected_connections:%s,used_memory:%s,used_memory_lua:%s,iops_per_sec:%s,fork_usec:%s" % (d['connected_clients'],d['blocked_clients'],d['rejected_connections'],d['used_memory'],d['used_memory_lua'],d['instantaneous_ops_per_sec'],d['latest_fork_usec'])
    perf = "connected_clients=%s;blocked_clients=%s;rejected_connections=%s;used_memory=%s;used_memory_lua=%s;iops_per_sec=%s;fork_usec=%s;" % (d['connected_clients'],d['blocked_clients'],d['rejected_connections'],d['used_memory'],d['used_memory_lua'],d['instantaneous_ops_per_sec'],d['latest_fork_usec'])
    print "OK - %s | %s" % (msg, perf)

def redis_connect(host, port, command):
    redis = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    redis.settimeout(5)
    redis.connect((host, port))
    redis.sendall(command)
    data = redis.recv(4096)
    redis.close()
    return data

def format_data(data):
    e = {}
    for line in data.split("\n"):
        if ":" in line:
            e[line.split(":")[0]] = line.split(":")[1].strip()
    return e

if __name__ == '__main__':
   data = redis_connect(host, port, command + "\r\n\r\n")
   nagios_report(format_data(data))

