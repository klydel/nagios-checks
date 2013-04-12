#!/usr/bin/env python

import socket
import sys

host = sys.argv[1]
port = int(sys.argv[2])

def nagios_return(code, msg, perf):
	if code == 3:
		print "UNKNOWN - %s" % (msg) 
	elif code == 2:
		print "CRITICAL - %s" % (msg, perf)
	elif code == 1:
		print "WARNING - %s" % (msg, perf)
	elif code == 0:
		print "OK - %s | %s" % (msg, perf)
	sys.exit()

def query_memcached_stats(host, port):
	c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	try:
        	c.connect( (host, port) )
        	c.send('stats\n')
        	response = c.recv(1024)
        	c.close()
        	return response
    	except Exception, e:
		print e
		nagios_return(3, "Unable to Connect", "ERROR")

def process_response( response ):
    stats = {}
    for line in response.split('\n'):
        fields = line.split(' ')
        if fields[0] == "STAT":
            stat = fields[2].replace('\r', '')
            stats[fields[1]] = stat
    return stats

raw_stats = query_memcached_stats(host, port)
stats = process_response(raw_stats)

hit_ratio = ( float(stats["get_hits"]) / float(stats["cmd_get"]) )
delete_hits = stats["delete_hits"]
get_hits = stats["get_hits"]
get_misses = stats["get_misses"]
total_pct = float(stats["get_hits"]) + float(stats["get_misses"])
get_pct = 100 * float(stats["cmd_get"]) / total_pct 
miss_pct = 100 * float(stats["get_misses"]) / total_pct
evictions = stats["evictions"]
curr_connections = stats["curr_connections"]
curr_items = stats["curr_items"]

msg = "GetHits:%s,GetMisses:%s,DeleteHits:%s,Evictions:%s,HitRatio:%s,GetPercent:%s,MissPercent:%s,CurrentItems:%s,CurrentConnections:%s" % (get_hits, get_misses, delete_hits, evictions, hit_ratio, get_pct, miss_pct, curr_items, curr_connections)
perf = "GetHits=%s;GetMisses=%s;DeleteHits=%s;Evictions=%s;HitRatio=%s;GetPercent=%s;MissPercent=%s;CurrentItems=%s;CurrentConnections=%s;" % (get_hits, get_misses, delete_hits, evictions, hit_ratio, get_pct, miss_pct, curr_items, curr_connections)

nagios_return(0, msg, perf)

