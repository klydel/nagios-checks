#!/usr/bin/python
import MySQLdb

ret = []
conn = MySQLdb.connect(host="", user="", passwd="", port=)
c = conn.cursor()
c.execute("show global status;")

ret = dict(c.fetchall())

ac = ret['Aborted_clients']
tco =  ret['Threads_connected']
qi = ret['Qcache_inserts']
qqin = ret['Qcache_queries_in_cache']
ibpwf = ret['Innodb_buffer_pool_wait_free']
ibppd = ret['Innodb_buffer_pool_pages_dirty']
irlta = ret['Innodb_row_lock_time_avg']
ibppf = ret['Innodb_buffer_pool_pages_flushed']
iolpw =  ret['Innodb_os_log_pending_writes']
tca = ret['Threads_cached']
idpr = ret['Innodb_data_pending_reads']
qh = ret['Qcache_hits']
idpw = ret['Innodb_data_pending_writes']
sq = ret['Slow_queries']
iolpf = ret['Innodb_os_log_pending_fsyncs']
ilw = ret['Innodb_log_waits']
irlw = ret['Innodb_row_lock_waits']
ot = ret['Open_tables']
idpf = ret['Innodb_data_pending_fsyncs']
qfm = ret['Qcache_free_memory']
tr = ret['Threads_running']
of = ret['Open_files']
tlw = ret['Table_locks_waited']

conn.close()
msg = "Aborted_clients:%s,Threads_connected:%s,Qcache_inserts:%s,Qcache_queries_in_cache:%s,Innodb_buffer_pool_wait_free:%s,Innodb_buffer_pool_pages_dirty:%s,Innodb_row_lock_time_avg:%s,Innodb_buffer_pool_pages_flushed:%s,Innodb_os_log_pending_writes:%s,Threads_cached:%s,Innodb_data_pending_reads:%s,Qcache_hits:%s,Innodb_data_pending_writes:%s,Slow_queries:%s,Innodb_os_log_pending_fsyncs:%s,Innodb_log_waits:%s,Innodb_row_lock_waits:%s,Open_tables:%s,Innodb_data_pending_fsyncs:%s,Qcache_free_memory:%s,Threads_running:%s,Open_files:%s,Table_locks_waited:%s" % (ac,tco,qi,qqin,ibpwf,ibppd,irlta,ibppf,iolpw,tca,idpr,qh,idpw,sq,iolpf,ilw,irlw,ot,idpf,qfm,tr,of,tlw)
perf = "Aborted_clients=%s;Threads_connected=%s;Qcache_inserts=%s;Qcache_queries_in_cache=%s;Innodb_buffer_pool_wait_free=%s;Innodb_buffer_pool_pages_dirty=%s;Innodb_row_lock_time_avg=%s;Innodb_buffer_pool_pages_flushed=%s;Innodb_os_log_pending_writes=%s;Threads_cached=%s;Innodb_data_pending_reads=%s;Qcache_hits=%s;Innodb_data_pending_writes=%s;Slow_queries=%s;Innodb_os_log_pending_fsyncs=%s;Innodb_log_waits=%s;Innodb_row_lock_waits=%s;Open_tables=%s;Innodb_data_pending_fsyncs=%s;Qcache_free_memory=%s;Threads_running=%s;Open_files=%s;Table_locks_waited=%s;" % (ac,tco,qi,qqin,ibpwf,ibppd,irlta,ibppf,iolpw,tca,idpr,qh,idpw,sq,iolpf,ilw,irlw,ot,idpf,qfm,tr,of,tlw)

print "OK - %s | %s" % (msg, perf)
