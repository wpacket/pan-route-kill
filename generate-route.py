#!/usr/bin/env python

import urllib
import urllib2
import ssl
import re

def api_request(url, values):

    data = urllib.urlencode(values)
    context = ssl._create_unverified_context()

    try:
        request = urllib2.Request(url, data)
        return urllib2.urlopen(request, context=context).read()

    except urllib2.URLError:
        print("ERROR Connecting to {url}. Check IP address.".format(url=url))
        return None


def keygen(username, password, url):

    values = {'type': 'keygen', 'user': username, 'password': password}
    response = api_request(url, values)

    try:
        key = re.search(r"(<key>)(\w+)", response)
        return key.group(2)
    except AttributeError:
        print("ERROR Obtaining API key from {url}. Check credentials.".format(url=url))
        return None


if __name__ == '__main__':
    ip = "192.168.55.128"
    username = "admin"
    password = "admin"

    url = "https://{ip}/api".format(ip=ip)
    api = keygen(username, password, url)

    #print(api)
    ip_address_base = "42.42."

    for i in range(40,254):
        for j in range(1,254):

            address = ip_address_base+str(i)+"."+str(j)

            value = {'type': 'config', 'action': 'set', 'Key': api, 'xpath': '/config/devices/entry[@name='+"'"+"localhost.localdomain"+"'"+']/network/virtual-router/entry[@name='+"'"+"outside-vr"+"'"+']/routing-table/ip/static-route/entry[@name='+"'"+str(i)+"-"+str(j)+"'"+']', 'element': '<destination>'+address+'/32</destination ><nexthop><discard/></nexthop>'}
            #print value
            response = api_request(url, value)
            print address+" creation :"+response
