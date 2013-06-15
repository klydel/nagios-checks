#!/usr/bin/env python
# simple script to get db stats from mongo
# usage: ./get_mongo_stats.py http://myserver:28018/serverStatus?json=1
# example output:
#OK - cursors_clientCursors_size:4,globalLock_activeClients_readers:0,connections_current:64,backgroundFlushing_average_ms:5.58905591302,globalLock_currentQueue_readers:0,globalLock_currentQueue_writers:0,mem_virtual:22409,mem_mappedWithJournal:20988,cursors_totalOpen:4,mem_mapped:10494,globalLock_activeClients_writers:0,cursors_timedOut:99,mem_resident:7018 | cursors_clientCursors_size=4;globalLock_activeClients_readers=0;connections_current=64;backgroundFlushing_average_ms=5.58905591302;globalLock_currentQueue_readers=0;globalLock_currentQueue_writers=0;mem_virtual=22409;mem_mappedWithJournal=20988;cursors_totalOpen=4;mem_mapped=10494;globalLock_activeClients_writers=0;cursors_timedOut=99;mem_resident=7018;

import sys
import json

HOSTURL = sys.argv[1]
METRIC = [
"cursors,totalOpen",
"cursors,clientCursors_size",
"cursors,timedOut",
"connections,current",
"backgroundFlushing,average_ms",
"mem,resident",
"mem,virtual",
"mem,mapped",
"mem,mappedWithJournal",
"globalLock,currentQueue,readers",
"globalLock,currentQueue,writers",
"globalLock,activeClients,readers",
"globalLock,activeClients,writers",
]
MAXTHRESHOLDS= {
   'connections_current' : 1000,
   'mem_resident' : 500000,
   'mem_mapped' : 1000000,
   'backgroundFlushing_average_ms' : 10,
   }
MINTHRESHOLDS = {
   'connections_available' : 5000,
   }
totals = {}

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

def check_thresholds(totals):
   warnings = []
   for t in MAXTHRESHOLDS:
      if totals[t] > MAXTHRESHOLDS[t]:
         warnings.append(t)
   return warnings
      
def get_custom(response):
   pass

def url_connect(url):
   import urllib2
   try:
      result = urllib2.urlopen(url, timeout=5)
      return result
   except urllib2.URLError, e:
      print "CRITICAL - %s | %s" % ( 'No Connection to Service', e.reason)
      sys.exit(1)


if __name__ == '__main__':
   data = url_connect(HOSTURL)
   response = json.load(data)
   for m in METRIC:
      totals[m.replace(',','_')] = reduce(dict.get, m.split(','), response)
   warnings = check_thresholds(totals)
   nagios_report(totals, warnings)



