#!/usr/bin/python2.7
#connects to mysql db and shows per user / per db connections and connection time avgs
# usage: ./get_mysql_processlist.py
# output: 
#OK - rdsadmin@mysql_user_conn:2,produser@Production_user_conn:156,produser@Production_avg_time:60,rdsadmin@mysql_avg_time:0
import MySQLdb

conn = MySQLdb.connect(host="", user="", passwd="", port=3360)
c = conn.cursor(MySQLdb.cursors.DictCursor)
c.execute("show processlist;")
ret = c.fetchall()
c.close()
conn.close()
result = {}
process_list = {
    'total_connections' : 0,
    }

def nagios_report(result):

   msg = [  k+":"+str(v)+"," for k,v in result.iteritems()]
   perf = [  k+"="+str(v)+";" for k,v in result.iteritems()]
   print "OK - %s | %s" % ( ''.join(msg), ''.join(perf))

for line in ret:
    process_list['total_connections'] += 1
    if line['User'] and line['db'] :
        userdb = line['User']+'@'+line['db']
    else:
        userdb = line['User']
    try:
        process_list[userdb].append(int(line['Time']))
    except:
        process_list[userdb] = []
        

for i in process_list:
    try:  
       user_conn = len(process_list[i])
    except:
       user_conn = 0

    if i is 'total_connections':
        result[i] = process_list[i]
    elif len(process_list[i]) > 0:
        result[i+'_avg_time'] = sum(process_list[i]) / user_conn
        result[i+'_user_conn'] = user_conn
    else:
        result[i+'_avg_time'] = 0
        result[i+'_user_conn'] = user_conn


nagios_report(result)

import sys
sys.exit()

    













































#stats[item[0]] = {item[1] : { 'command' : item[4], 'time' : item[5] }  }

    #stats[item[1]][item[4]] = stats[item[1]][item[4]] + item[5]
#for i in stats:
#    for k in stats[i]:
#        print stats[i][k]
    #scoreboard = dict((c, l[1].count(c)) for c in l[1])





