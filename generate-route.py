#!/usr/bin/env python

"""
urllib: needed for the urlencode method
re: needed to search for API key in response
ssl: needed to suppress/ignore SSL errors
"""

import urllib
import urllib2
import ssl
import re


##############################################################
# API REQUEST
##############################################################
def api_request(url, values):
    """
    API driver function. The middle-man between the script and firewall.

    :param url:     string - URL to connect to ("https://192.168.1.1/api")
    :param values:  dictionary - the API command to be executed
    :return:        if successful, returns an XML response as a string
                    if unsuccessful, returns None
    """

    # must encode the dictionary of values
    data = urllib.urlencode(values)

    # ignore SSL errors
    context = ssl._create_unverified_context()

    try:
        request = urllib2.Request(url, data)
        return urllib2.urlopen(request, context=context).read()

    except urllib2.URLError:
        print("ERROR Connecting to {url}. Check IP address.".format(url=url))
        return None


##############################################################
# KEYGEN
##############################################################
def keygen(username, password, url):
    """
    Fetches the API key from the firewall.

    :param username:    string - "username"
    :param password:    string - "password"
    :param url:         string - URL to connect to ("https://192.168.1.1/api")
    :return:            if successful, returns the API key as a string
                        if unsuccessful, returns None
    """

    values = {'type': 'keygen', 'user': username, 'password': password}
    response = api_request(url, values)

    try:
        key = re.search(r"(<key>)(\w+)", response)
        return key.group(2)
    except AttributeError:
        print("ERROR Obtaining API key from {url}. Check credentials.".format(url=url))
        return None


##############################################################
# MAIN
##############################################################
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
