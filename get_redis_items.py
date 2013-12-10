#!/usr/bin/env python
# simple script to pull key lengths from redis
# set key name in queues list
# reports back to nagios
# usage: get_redis_items.py myhost.mydomain.com 6379
# output: 
#OK - mykey1-example1:0,mykey1-example2:1697 | mykey1-example1=0;mykey1-example2=1697;
import socket
import sys
queue_threshold = 10000
warning = []
host = sys.argv[1]
port = int(sys.argv[2])
command = "llen "
queues = [
"mykey1-example",
"mykey2-example",
]
totals = {}

def nagios_report(totals, warning):
   if warning:
      msg = [  k+":"+v+"," for k,v in totals.iteritems()]
      perf = [  k+"="+v+";" for k,v in totals.iteritems()]
      print "Warning - %s High -  %s | %s" % ( ','.join(warning), ''.join(msg), ''.join(perf))
      sys.exit(1)
   else:
      msg = [  k+":"+v+"," for k,v in totals.iteritems()]
      perf = [  k+"="+v+";" for k,v in totals.iteritems()]
      print "OK - %s | %s" % ( ''.join(msg), ''.join(perf))
      sys.exit(0)

def redis_connect(host, port):
    redis_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    redis_conn.settimeout(10)
    redis_conn.connect((host, port))
    return redis_conn

def redis_command(redis_conn, command):
    redis_conn.sendall(command)
    data = redis_conn.recv(4096)
    return data

if __name__ == '__main__':
    redis_conn = redis_connect(host, port)
    for q in queues:
        data = redis_command(redis_conn, command + q + "\r\n\r\n")
        metric = data.strip().replace(":", "")
        if int(metric) < queue_threshold:
           totals[q] = metric
        else:
           totals[q] = metric
           warning.append(q)
    redis_conn.close()

    nagios_report(totals, warning)


