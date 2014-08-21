#!/usr/bin/python
# runs rkhunter and parses output to return to nagios
# whitelist files if you wish to ignore
from subprocess import Popen, PIPE
import sys

rkhunter_bin = '/usr/bin/rkhunter'
rkhunter_args = '-c --enable all --disable none --rwo'
listener_whitelist = ['/sbin/dhclient']
suspicious_whitelist = []
deleted_files_whitelist = []
network_listeners_string = 'is listening on the network'
outdated_dats_string = 'exists on the system, but it is not present in the'
suspicious_files_string = 'contains some suspicious content and should be checked'
deleted_files_string = 'The following processes are using deleted files'
inode_change_string = 'The file properties have changed'
totals = {
   'network_listeners' : [],
   'outdated_dats' : [],
   'suspicious_files' : [],
   'deleted_files' : [],
   'inode_change' : [],
}


def nagios_report(totals, warning):
   if warning:
      msg = [  k+":"+','.join(v)+"," for k,v in totals.iteritems() if len(v) > 1]
      print "WARNING -%s " % ( ''.join(msg) )
      sys.exit(1)
   else:
      print "OK - Scan OK"
      sys.exit(0)

def run_rkhunter():
        warning = False
        rkhunter_cmd = "%s %s" % (rkhunter_bin, rkhunter_args)
        output = Popen(rkhunter_cmd.split(), stdout=PIPE).communicate()[0].strip()
        rkoutput = iter(output.split('\n'))
        for line in rkoutput:
            if outdated_dats_string in line:
                totals['outdated_dats'].append(line.split("'")[1])
                warning = True

            elif suspicious_files_string in line:
                s = line.split("'")[1]
                if s not in suspicious_whitelist:
                    totals['suspicious_files'].append(s)
                    warning = True

            elif deleted_files_string in line:
                process = next(rkoutput)
                d = process.split()[1]
                if d not in deleted_files_whitelist:
                    totals['deleted_files'].append(d)
                    warning = True

            elif network_listeners_string in line:
                l = line.split("'")[1]
                if l not in listener_whitelist:
                    totals['network_listeners'].append(l)
                    warning = True

            elif inode_change_string in line:
                process = next(rkoutput)
                totals['inode_change'].append(process.split('/')[-1])
                warning = True
        return warning


if __name__ == '__main__':
    warning = run_rkhunter()
    nagios_report(totals, warning)
