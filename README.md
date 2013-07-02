### Nagios Plugins

Collection of Nagios checks

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
only returns OK status currently for most checks, you can add further checks though.
<pre><code>
    ./check_rds_new myhost WriteIOPS 800
    OK - WriteIOPS=67.22689075630252 |WriteIOPS=67.22689075630252\n
</code></pre>


check_rps_vip
-----------
Uses Apache's mod_status page to get request per second (rps) stats from all servers in a group.  If you had 150 servers (named nym-web1 to nym-web150), you could run this script like so:
<pre><code>
    for i in {1..150} ; do ./check_rps_vip nym-web$i ; done
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
script to grab network interface stats from /sys/class/net on linux.  Outputs perf data as well.
<pre><code>
    ./network_stats.pl eth1
    OK - collisions=0: multicast=6: rx_bytes=16756639755735: rx_compressed=0: rx_crc_errors=0: rx_dropped=0: rx_errors=0: rx_fifo_errors=0: rx_frame_errors=0: rx_length_errors=0: rx_missed_errors=25731: rx_over_errors=0: rx_packets=39310580998: tx_aborted_errors=0: tx_bytes=20133836511769: tx_carrier_errors=0: tx_compressed=0: tx_dropped=0: tx_errors=0: tx_fifo_errors=0: tx_heartbeat_errors=0: tx_packets=46496395859: tx_window_errors=0: 


</code></pre>



get_apache_status.py
-----------
gets apache status via mod_status.  Outputs perf data as well.
<pre><code>
    ./get_apache_status.py http://localhost/server-status?auto
    OK - Sending:1,Uptime:1280,IdleWorkers:8,Total Accesses:8586,Total kBytes:12146,BytesPerReq:1448.58,CPULoad:16.0617,BytesPerSec:9716.8,Waiting:8,ReqPerSec:6.70781,Reading:25,Open:222,BusyWorkers:26, | Sending=1;Uptime=1280;IdleWorkers=8;Total Accesses=8586;Total kBytes=12146;BytesPerReq=1448.58;CPULoad=16.0617;BytesPerSec=9716.8;Waiting=8;ReqPerSec=6.70781;Reading=25;Open=222;BusyWorkers=26;


</code></pre>



get_aws_metrics.py
-----------
python wrapper for amazon apitools script mon-get-stats.  uses boto, needs a .boto file for aws auth, as well as whatever auth file you would normally use for mon-get-stats (will fix).  Outputs perf data as well.
<pre><code>
        ./get_aws_metrics.py mywebserver1 NetworkOut Maximum
        OK - NetworkOut:45398267 | NetworkOut=45398267

        or

        ./get_aws_metrics.py vol-xxxx VolumeReadOps Sum 
        OK - VolumeReadOps:0 | VolumeReadOps=0

</code></pre>



get_mysql_processlist.py
-----------
connects to mysql db and shows per user / per db connections and connection time avgs.  Outputs perf data as well.
<pre><code>
        ./get_mysql_processlist.py
        OK - rdsadmin@mysql_user_conn:2,produser@Production_user_conn:156,produser@Production_avg_time:60,rdsadmin@mysql_avg_time:0

</code></pre>




get_mongo_stats.py
-----------
simple script to get db stats from mongo.  Outputs perf data as well.
<pre><code>
        ./get_mongo_stats.py http://mymongoserver:28018/serverStatus?json=1
        OK - cursors_clientCursors_size:4,globalLock_activeClients_readers:0,connections_current:64,backgroundFlushing_average_ms:5.58905591302,globalLock_currentQueue_readers:0,globalLock_currentQueue_writers:0,mem_virtual:22409,mem_mappedWithJournal:20988,cursors_totalOpen:4,mem_mapped:10494,globalLock_activeClients_writers:0,cursors_timedOut:99,mem_resident:7018 | cursors_clientCursors_size=4;globalLock_activeClients_readers=0;connections_current=64;backgroundFlushing_average_ms=5.58905591302;globalLock_currentQueue_readers=0;globalLock_currentQueue_writers=0;mem_virtual=22409;mem_mappedWithJournal=20988;cursors_totalOpen=4;mem_mapped=10494;globalLock_activeClients_writers=0;cursors_timedOut=99;mem_resident=7018;

</code></pre>




get_elasticsearch_stats.py
-----------
simple script to get stats from elasticsearch. Really only works for ec2 hosts right now.  Outputs perf data as well.
<pre><code>
        ./get_elasticsearch_stats.py myserver
        OK - Spiderman - jvm_mem_heap_used_in_bytes:3030145064,jvm_mem_heap_committed_in_bytes:4277534720,jvm_threads_count:78,indices_search_fetch_current:0,jvm_mem_non_heap_used_in_bytes:55179904,os_mem_used_in_bytes:7731814400,indices_get_current:0,os_mem_actual_used_in_bytes:4950654976,indices_merges_current_size_in_bytes:0,jvm_mem_non_heap_committed_in_bytes:83001344,indices_indexing_delete_current:0,indices_merges_current_docs:0,indices_indexing_index_current:0,indices_merges_current:0,indices_search_query_current:0,os_cpu_user:1,os_swap_used_in_bytes:9027584 | jvm_mem_heap_used_in_bytes=3030145064;jvm_mem_heap_committed_in_bytes=4277534720;jvm_threads_count=78;indices_search_fetch_current=0;jvm_mem_non_heap_used_in_bytes=55179904;os_mem_used_in_bytes=7731814400;indices_get_current=0;os_mem_actual_used_in_bytes=4950654976;indices_merges_current_size_in_bytes=0;jvm_mem_non_heap_committed_in_bytes=83001344;indices_indexing_delete_current=0;indices_merges_current_docs=0;indices_indexing_index_current=0;indices_merges_current=0;indices_search_query_current=0;os_cpu_user=1;os_swap_used_in_bytes=9027584

</code></pre>




check_custom_service.sh
-----------
bash script to get res mem, virtmem, cpupercent, mempercent of a process, sums all children pids as well.  Outputs perf data.
<pre><code>
	./check_custom_service.sh www-data httpd 600 1024 85 85                      
	OK - RESMEM=230MB:VIRTMEM=858MB:USEDCPU=9.4%:USEDMEM=13.8%

</code></pre>






