#!/usr/bin/python
#checks a files modification time and deltas it against max_stale_time
#change monitor_files to whatever file you want
import os.path, time, sys
monitor_files = ['/var/log/www.log', '/var/log/httpd/apache-access.log']
max_stale_time = 240
warnings = []
totals = {}
def nagios_report(totals, warnings):
   if warnings:
      msg = [  k+":"+str(v)+"," for k,v in totals.iteritems()]
      perf = [  k+"="+str(v)+";" for k,v in totals.iteritems()]
      print "WARNING -%s is stale- %s | %s" % ( ','.join(warnings), ''.join(msg), ''.join(perf))
      sys.exit(1)
   else:
      msg = [  k+":"+str(v)+"," for k,v in totals.iteritems()]
      perf = [  k+"="+str(v)+";" for k,v in totals.iteritems()]
      print "OK - %s | %s" % ( ''.join(msg), ''.join(perf))
      sys.exit(0)


if __name__ == '__main__':
    now =  time.time()
    for f in monitor_files:
        ftime = os.path.getmtime(f)
        log_name = f.split('/')[-1]
        if ftime < now and now - ftime > max_stale_time:
            totals[log_name] =  now - ftime
            warnings.append(log_name)
        
        else:
            totals[log_name] = now - ftime

    nagios_report(totals, warnings)
