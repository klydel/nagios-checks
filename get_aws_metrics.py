#!/usr/bin/python2.7
#generic wrapper for mon get stats in python 
#usage : ./get_aws_metrics.py myhost NetworkOut Maximum
#OK - NetworkOut:45398267 | NetworkOut=45398267
#additionally, you can use it for ebs volume metrics:
#./get_aws_metrics2.py vol-ffffffff VolumeReadOps Sum
#OK - VolumeReadOps:0 | VolumeReadOps=0
from boto.ec2.connection import EC2Connection
import boto.ec2
from datetime import datetime, timedelta
import sys

BOTO_CFG = '.boto'
EC2_REGION = "us-east-1"
EC2_TAG = 'role'
DNAME = 'InstanceId'
NSPACE = 'AWS/EC2'
DATE_TPL = '%Y-%m-%dT%H:%M'
MON_COMMAND = '/opt/aws/apitools/mon/bin/mon-get-stats'
MON_ARGS = '%s --start-time %s --end-time %s --statistics "%s" --namespace %s --dimensions "%s=%s" --aws-credential-file=/opt/aws/credential-file-path.conf'
host = sys.argv[1]
metric = sys.argv[2]
statistic = sys.argv[3]

def parse_config():
   import ConfigParser
   config = ConfigParser.ConfigParser()
   config.read([BOTO_CFG])
   aws_access_key_id = config.get('Credentials', 'aws_access_key_id')
   aws_secret_access_key = config.get('Credentials', 'aws_secret_access_key')
   return aws_access_key_id,aws_secret_access_key

def nagios_report(metric, d):
   msg = "%s:%d" % (metric, d)
   perf = "%s=%d" % (metric, d)
   print "OK - %s | %s" % (msg, perf)

def get_mon_data(dimension, metric, stat, DNAME, NSPACE):
    from subprocess import Popen, PIPE
    mon_cmd = "%s %s" % (MON_COMMAND, MON_ARGS % (metric,start,end,stat,NSPACE,DNAME,dimension))
    try:
        output = Popen(mon_cmd.split(), stdout=PIPE).communicate()[0].strip()
        bytes = output.split('\n')[-1:]
        bytes = bytes[0].split()[2]
        return float(bytes)
    except:
        print "UNKNOWN - UNKNOWN ERROR OCCURED"
        sys.exit(1)

def clean_host_name(hostname):
    if 'large' in hostname:
        return hostname.replace("-large", "")
    else:
        return hostname

def connect_to_ec2(aws_access_key_id,aws_secret_access_key):
    return EC2Connection(aws_access_key_id,aws_secret_access_key)

def get_all_reservations(conn):
    return conn.get_all_instances()

def get_all_instances(reservations):
    return [i for r in reservations for i in r.instances]

def get_instance_ids(instances):
    return {clean_host_name(i.tags['Name']): i.id for i in instances if EC2_TAG in i.tags}

def connect_and_list():
    try:
       akey,aid = parse_config()
       conn = connect_to_ec2(akey,aid)
       reservations = get_all_reservations(conn)
       instances = get_all_instances(reservations)
       instanceids = get_instance_ids(instances)
       return instanceids
    except:
       print "WARNING - Unable to Connect to EC2"
       sys.exit(1)

if __name__ == '__main__':
    end = datetime.now().strftime(DATE_TPL)
    hourago = datetime.now() - timedelta(hours=1)
    start = hourago.strftime(DATE_TPL)
    if 'vol' in host:
       DNAME = 'VolumeId'
       NSPACE = 'AWS/EBS'
       nagios_report(metric, get_mon_data(host, metric, statistic, DNAME, NSPACE))
    else:
       DNAME = 'InstanceId'
       NSPACE = 'AWS/EC2'
       instanceids = connect_and_list()
       nagios_report(metric, get_mon_data(instanceids[host], metric, statistic, DNAME, NSPACE))
