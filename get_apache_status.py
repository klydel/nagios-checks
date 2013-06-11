#!/usr/bin/env python
# run like: ./get_apache_status.py http://localhost/server-status?auto
# example output:
#./get_apache_status.py http://localhost/server-status?auto
#
#OK - Sending:1,Uptime:1280,IdleWorkers:8,Total Accesses:8586,Total kBytes:12146,BytesPerReq:1448.58,CPULoad:16.0617,BytesPerSec:9716.8,Waiting:8,ReqPerSec:6.70781,Reading:25,Open:222,BusyWorkers:26, | Sending=1;Uptime=1280;IdleWorkers=8;Total Accesses=8586;Total kBytes=12146;BytesPerReq=1448.58;CPULoad=16.0617;BytesPerSec=9716.8;Waiting=8;ReqPerSec=6.70781;Reading=25;Open=222;BusyWorkers=26;

import sys
url = sys.argv[1]
totals = {}
SCOREBOARD_MAP = {'_' : 'Waiting', 'S' : 'Starting', 'R' : 'Reading', 'W' : 'Sending', 'K' : 'Keepalive', 'D' : 'DNS', 'C' : 'Closing', 'L' : 'Logging', 'G' : 'Finishing', 'I' : 'Cleanup', '.' : 'Open'}

def nagios_report(totals):
   msg = [  k+":"+v+"," for k,v in totals.iteritems()]
   perf = [  k+"="+v+";" for k,v in totals.iteritems()]
   print "OK - %s | %s" % ( ''.join(msg), ''.join(perf))

def apache_connect(url):
	import urllib2
	try:
  		result = urllib2.urlopen(url)
  		return result
	except urllib2.URLError, e:
                print "CRITICAL - %s | %s" % ( 'No Connection to Service', e.reason)
                sys.exit(1)

if __name__ == '__main__':
	data = apache_connect(url)
	for line in data.readlines():
		l = [x.strip() for x in line.split(":")]
		if 'Scoreboard' in line:
			scoreboard = dict((c, l[1].count(c)) for c in l[1])
			for k,v in scoreboard.iteritems():
				totals[SCOREBOARD_MAP[k]] = str(v)
		else:
			totals[l[0]] = str(l[1])
		
    	nagios_report(totals)


