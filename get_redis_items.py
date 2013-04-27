#!/usr/bin/env python
# simple script to pull key lengths from redis
# set key name in queues list
# reports back to nagios
# usage: get_redis_items.py myhost.mydomain.com 6379

import socket
import sys
host = sys.argv[1]
port = int(sys.argv[2])
command = "llen "
queues = [
"mykey1-example",
"mykey2-example",
]
totals = {}

def nagios_report(totals):

   msg = [  k+":"+v+"," for k,v in totals.iteritems()]
   perf = [  k+"="+v+";" for k,v in totals.iteritems()]
   print "OK - %s | %s" % ( ''.join(msg), ''.join(perf))

def redis_connect(host, port, command):
    redis = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    redis.settimeout(5)
    redis.connect((host, port))
    redis.sendall(command)
    data = redis.recv(4096)
    redis.close()
    return data

if __name__ == '__main__':
    for q in queues:
        data = redis_connect(host, port, command + q + "\r\n\r\n")
        totals[q] = data.strip().replace(":", "")

    nagios_report(totals)


