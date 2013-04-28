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


