#!/usr/bin/python2.7
#get stats from elasticsearch
#usage : ./get_elasticsearch_stats.py myserver
#output:
#OK - Spiderman - jvm_mem_heap_used_in_bytes:3030145064,jvm_mem_heap_committed_in_bytes:4277534720,jvm_threads_count:78,indices_search_fetch_current:0,jvm_mem_non_heap_used_in_bytes:55179904,os_mem_used_in_bytes:7731814400,indices_get_current:0,os_mem_actual_used_in_bytes:4950654976,indices_merges_current_size_in_bytes:0,jvm_mem_non_heap_committed_in_bytes:83001344,indices_indexing_delete_current:0,indices_merges_current_docs:0,indices_indexing_index_current:0,indices_merges_current:0,indices_search_query_current:0,os_cpu_user:1,os_swap_used_in_bytes:9027584 | jvm_mem_heap_used_in_bytes=3030145064;jvm_mem_heap_committed_in_bytes=4277534720;jvm_threads_count=78;indices_search_fetch_current=0;jvm_mem_non_heap_used_in_bytes=55179904;os_mem_used_in_bytes=7731814400;indices_get_current=0;os_mem_actual_used_in_bytes=4950654976;indices_merges_current_size_in_bytes=0;jvm_mem_non_heap_committed_in_bytes=83001344;indices_indexing_delete_current=0;indices_merges_current_docs=0;indices_indexing_index_current=0;indices_merges_current=0;indices_search_query_current=0;os_cpu_user=1;os_swap_used_in_bytes=9027584

from boto.ec2.connection import EC2Connection
import boto.ec2
from datetime import datetime, timedelta
import sys
import json

BOTO_CFG = '/var/spool/nagios/.boto'
EC2_REGION = "us-east-1"
ES_URL = 'http://%s:9200/_cluster/nodes/stats?all=true'
METRIC = [
   "jvm,mem,heap_used_in_bytes",
   "jvm,mem,non_heap_used_in_bytes",
   "jvm,mem,heap_committed_in_bytes",
   "jvm,mem,non_heap_committed_in_bytes",
   "jvm,threads,count",
   "indices,search,fetch_current",
   "indices,search,query_current",
   "indices,get,current",
   "indices,indexing,index_current",
   "indices,indexing,delete_current",
   "indices,merges,current_size_in_bytes",
   "indices,merges,current_docs",
   "indices,merges,current",
   "os,mem,used_in_bytes",
   "os,mem,actual_used_in_bytes",
   "os,swap,used_in_bytes",
   "os,cpu,user",
]
MAXTHRESHOLDS= {
   "jvm_mem_heap_used_in_bytes": 4379836008,
   }
totals = {}
host = sys.argv[1]

def parse_config():
   import ConfigParser
   config = ConfigParser.ConfigParser()
   config.read([BOTO_CFG])
   aws_access_key_id = config.get('Credentials', 'aws_access_key_id')
   aws_secret_access_key = config.get('Credentials', 'aws_secret_access_key')
   return aws_access_key_id,aws_secret_access_key

def nagios_report(totals, warnings, es_name):
   if warnings:
      msg = [  k+":"+str(v)+"," for k,v in totals.iteritems()]
      perf = [  k+"="+str(v)+";" for k,v in totals.iteritems()]
      print "WARNING -%s is warning- %s | %s" % ( ','.join(warnings), ''.join(msg), ''.join(perf))
      sys.exit(1)
   else:
      msg = [  k+":"+str(v)+"," for k,v in totals.iteritems()]
      perf = [  k+"="+str(v)+";" for k,v in totals.iteritems()]
      print "OK - %s - %s | %s" % ( es_name, ''.join(msg), ''.join(perf))
      sys.exit(0)

def connect_to_ec2(aws_access_key_id,aws_secret_access_key):
    return EC2Connection(aws_access_key_id,aws_secret_access_key)

def get_all_reservations(conn):
    return conn.get_all_instances()

def get_all_instances(reservations):
    return [i for r in reservations for i in r.instances]

def get_instance_ids(instances):
    return {i.tags['Name']: i.id for i in instances}

def connect_and_list():
    try:
       akey,aid = parse_config()
       conn = connect_to_ec2(akey,aid)
       reservations = get_all_reservations(conn)
       instances = get_all_instances(reservations)
       return instances
    except:
       print "WARNING - Unable to Connect to EC2"
       sys.exit(1)

def url_connect(url):
   import urllib2
   try:
      result = urllib2.urlopen(url, timeout=15)
      return result
   except urllib2.URLError, e:
      print "CRITICAL - %s | %s" % ( 'No Connection to Service', e.reason)
      sys.exit(1)


if __name__ == '__main__':
       instanceids = connect_and_list()
       for i in instanceids:
          if host.strip() in i.tags['Name']:
             dns_name = i.private_dns_name.replace('.ec2.internal','')
             p_ip = i.private_ip_address
       data = url_connect(ES_URL % (host.strip()))
       response = json.load(data)
       
       for i in response['nodes']:
          if response['nodes'][i]['hostname'] == dns_name or p_ip in response['nodes'][i]['transport_address']:
             try:
                es_name = response['nodes'][i]['name']
             except:
                es_name = 'unknown'
             for m in METRIC:
                totals[m.replace(',','_')] = reduce(dict.get, m.split(','), response['nodes'][i])
       nagios_report(totals, None, es_name)
