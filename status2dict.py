#!/usr/bin/env python
""" This takes the nagios realtime status dada and outputs as dict or json. """

import re
import sys
import datetime
import json
status_file="/var/log/nagios/status.dat"
hosttoken='hoststatus'
servicetoken='servicestatus'
programtoken='programstatus'

def GetDefinitions(filename,obj):
    """ Parse the status.dat file and extract matching object definitions """
    file=open(filename)
    content=file.read().replace("\t"," ")
    file.close
    pat=re.compile(obj +' \{([\S\s]*?)\}',re.DOTALL)
    finds=pat.findall(content)
    return finds


def GetDirective(item,directive):
    """ parse an object definition, return the directives """
    pat=re.compile(' '+directive + '[\s= ]*([\S, ]*)\n')
    m=pat.search(item)
    if m:
        return m.group(1)


def JsonAttr(definition,directive):
    """ returns directive:'value' """
    return "%s:%s" % (directive,GetDirective(definition,directive).strip())


def ParseDataFile():
    """ Parse and output """
    nagios_root_dict = {}
    hosts=GetDefinitions(status_file,hosttoken)

    for hostdef in hosts:
        hostname = JsonAttr(hostdef,"host_name").split(':')[1]
        nagios_root_dict[hostname] = {}
        services=GetDefinitions(status_file,servicetoken)

        for servicedef in services:
            if(GetDirective(servicedef,"host_name").strip()==GetDirective(hostdef,"host_name").strip()):
                try:
                    servicename = JsonAttr(servicedef,"service_description").split(":")[1]
                    performancedata = JsonAttr(servicedef,"performance_data").split(":")[1]
                    nagios_root_dict[hostname][servicename] = performancedata.strip()
                except:
                    pass
    return nagios_root_dict



if __name__ == "__main__":
    sys.exit(ParseDataFile())

