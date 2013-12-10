#!/usr/bin/env python
#uses flower for celery to get processed items from celery queue.  sleeps for sleeptime before getting second sample. if values processed are same, warn.
#change queues list for your celery worker names.
# example output:
#./get_celery_worker_status.py http://flowerhost:flowerport/api/workers
#WARNING -celery.worker2 is stale - celery.worker1:685,celery.worker2:4 | celery.worker1=685;celery.worker2=4;

import json
import sys
import time

url = sys.argv[1]
sleeptime = 45
totals = {}
warnings = []
watch = 'completed_tasks'
queues = ['celery.worker1','celery.worker2']

def nagios_report(totals):
   if warnings:
      msg = [  k+":"+str(v)+"," for k,v in totals.iteritems()]
      perf = [  k+"="+str(v)+";" for k,v in totals.iteritems()]
      print "WARNING -%s is stale - %s | %s" % ( ','.join(warnings), ''.join(msg), ''.join(perf)) 
      sys.exit(1)
   else:
      msg = [  k+":"+str(v)+"," for k,v in totals.iteritems()]
      perf = [  k+"="+str(v)+";" for k,v in totals.iteritems()]
      print "OK - %s | %s" % ( ''.join(msg), ''.join(perf))
      sys.exit(0)

def flower_connect(url):
   import urllib2
   try:
      result = urllib2.urlopen(url, None, 10)
      return result
   except urllib2.URLError, e:
      print "CRITICAL - %s | %s" % ( 'No Connection to Service', e)
      sys.exit(1)

def get_sample():
   result = flower_connect(url)
   sample = json.loads(result.readlines()[0])
   return sample

if __name__ == '__main__':

   sample1 = get_sample()
   time.sleep(sleeptime)
   sample2 = get_sample()

   for k in sample1:
      totals[str(k)] = sample2[k][watch]
      if sample1[k][watch] == sample2[k][watch] and k in queues:
          warnings.append(str(k))

   nagios_report(totals)


