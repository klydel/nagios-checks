#!/usr/bin/python2.7
import MySQLdb
import sys
#usage:
#./get_mysql_status.py 
#OK - Innodb_data_pending_fsyncs:0,Innodb_os_log_pending_fsyncs:0,Innodb_row_lock_time_avg:3708,Threads_cached:0,Innodb_buffer_pool_wait_free:0,Innodb_data_pending_reads:0,Threads_running:2,Innodb_log_waits:47,Innodb_data_pending_writes:0,Open_files:87,Innodb_os_log_pending_writes:0,Threads_connected:1287,Innodb_buffer_pool_pages_dirty:65947, | Innodb_data_pending_fsyncs=0;Innodb_os_log_pending_fsyncs=0;Innodb_row_lock_time_avg=3708;Threads_cached=0;Innodb_buffer_pool_wait_free=0;Innodb_data_pending_reads=0;Threads_running=2;Innodb_log_waits=47;Innodb_data_pending_writes=0;Open_files=87;Innodb_os_log_pending_writes=0;Threads_connected=1287;Innodb_buffer_pool_pages_dirty=65947;
#notusing: Qcache_inserts,Qcache_queries_in_cache,Qcache_hits,Slow_queries,Innodb_row_lock_waits,Open_tables
#testing: Com_stmt_execute, Sort_merge_passes
#http://dev.mysql.com/doc/refman/5.0/en/server-status-variables.html
METRIC = [
   "Innodb_buffer_pool_wait_free",
   "Threads_connected",
   "Innodb_buffer_pool_pages_dirty",
   "Innodb_row_lock_time_avg",
   "Innodb_os_log_pending_writes",
   "Threads_cached",
   "Innodb_data_pending_reads",
   "Innodb_data_pending_writes",
   "Innodb_os_log_pending_fsyncs",
   "Innodb_log_waits",
   "Innodb_data_pending_fsyncs",
   "Threads_running",
   "Open_files",
]
MAXTHRESHOLDS= {
   "Threads_connected": 3000,
   "Innodb_row_lock_time_avg": 5000,
   "Innodb_buffer_pool_pages_dirty": 200000
   }
totals = {}
warnings = []

def nagios_report(totals):
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

def mysql_connect(host="localhost", user="root", passwd="", port=3306):
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd, port=port)
    c = conn.cursor()
    c.execute("show global status;")
    ret = dict(c.fetchall())
    c.close()
    conn.close()
    return ret

def format_data(rawdata):
    for m in METRIC:
        totals[m] = rawdata[m]
        if m in MAXTHRESHOLDS and float(rawdata[m]) > MAXTHRESHOLDS[m]:
            warnings.append(m)
    return totals

if __name__ == '__main__':
    rawdata = mysql_connect("localhost", "nagiosuser", "pass", 3360)
    nagios_report(format_data(rawdata))
