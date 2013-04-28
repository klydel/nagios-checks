### Nagios Plugins

Collection of Nagios plugins

check_core_dumps
-----------

uses $coredir to scan for core dumps, alerts to nagios.  Requires Nagios/Plugin/Functions.pm.
<pre><code>
    perl check_core_dumps
    OK: Total Coredumps: 0
</code></pre>


check_dfs_space
-----------
script to check hadoop's dfs used space percentage.
gets dfs used percentage by visiting hadoops dfshealth page.
<pre><code>
    ./check_dfs_space nym-hadoop1 50070
    OK: DFS Remaining Space at: 80%
</code></pre>


check_memcached_stats.py
-----------
script to get memcached stats.  Also returns performance data for graphing.
script returns ok status for everything at the moment.  just using this to chart.
<pre><code>
    ./check_memcached_stats.py
    OK - GetHits:5290181,GetMisses:1961090,DeleteHits:24959,Evictions:0,HitRatio:0.729552239876,GetPercent:100.0,MissPercent:27.0447760124,CurrentItems:12952,CurrentConnections:77
</code></pre>


check_rds
-----------
wrapper for mon-get-stats.  Used to get database stats from Amazon RDS.  Requires Amazon api tools. 
only returns OK status currently, you can add checks though.
<pre><code>
    ./check_rds MyRDS WriteIOPS 6000 1000
    OK - WriteIOPS=104.42188776105472
</code></pre>


check_rps_vip
-----------
Uses Apache's mod_status page to get request per second (rps) stats from all servers in a group.  If you had 150 servers (named nym-web1 to nym-web150), you could run this script like so:
<pre><code>
    ./check_rps_vip nym-web
    OK : Total RPS for nym-web: 15000 | RequestsPerSecond=15000
</code></pre>


check_sockets.sh
-----------
bash shell script to get total sockets and open files for a system.


disableNagiosChecks
-----------
Script used to disable all nagios alerts for a given server. Requires a nagios username and password.
<pre><code>
    ./disableNagiosChecks nym-web1
    
    for i in {1..50} ; do ./disableNagiosChecks nym-web$i ; done    
</code></pre>


get_mysql_status.py
-----------
Gets mysql stats for a server usering "SHOW GLOBAL STATUS". Returns performace data.  Requires mysql username, password, and port.
<pre><code>
    ./get_mysql_status.py
    OK - Aborted_clients:14,Threads_connected:10,Qcache_inserts:0,Qcache_queries_in_cache:0,Innodb_buffer_pool_wait_free:0,Innodb_buffer_pool_pages_dirty:43,Innodb_row_lock_time_avg:46,Innodb_buffer_pool_pages_flushed:73,Innodb_os_log_pending_writes:0,Threads_cached:0,Innodb_data_pending_reads:0,Qcache_hits:0,Innodb_data_pending_writes:0,Slow_queries:32,Innodb_os_log_pending_fsyncs:0,Innodb_log_waits:34,Innodb_row_lock_waits:80,Open_tables:400,Innodb_data_pending_fsyncs:0,Qcache_free_memory:0,Threads_running:2,Open_files:95,Table_locks_waited:187    

</code></pre>


get_redis_items.py
-----------
script to pull key lengths from redis, reports to nagios with perf data.  Update script with key names inside queues list.
<pre><code>
    ./get_redis_items.py myhost.mydomain.com 6379
    OK - mykey1-example:198,mykey2-example:89


</code></pre>


get_redis_stats.py
-----------
script to pull INFO command from redis.  gets connected_clients, used_memory, used_memory_lua, instantaneous_ops_per_sec, instantaneous_ops_per_sec, latest_fork_usec, used_memory_rss, blocked_clients, rejected_connections.  
<pre><code>
    ./get_redis_stats.py myhost.mydomain.com 6379
    OK - connected_clients:193,blocked_clients:2,rejected_connections:0,used_memory:12340208,used_memory_lua:31744,iops_per_sec:44,fork_usec:5


</code></pre>



network_stats.pl
-----------
script to grab network interface stats from /sys/class/net on linux.  Outpus perf data as well.
<pre><code>
    ./network_stats.pl eth1
    OK - collisions=0: multicast=6: rx_bytes=16756639755735: rx_compressed=0: rx_crc_errors=0: rx_dropped=0: rx_errors=0: rx_fifo_errors=0: rx_frame_errors=0: rx_length_errors=0: rx_missed_errors=25731: rx_over_errors=0: rx_packets=39310580998: tx_aborted_errors=0: tx_bytes=20133836511769: tx_carrier_errors=0: tx_compressed=0: tx_dropped=0: tx_errors=0: tx_fifo_errors=0: tx_heartbeat_errors=0: tx_packets=46496395859: tx_window_errors=0: 


</code></pre>






