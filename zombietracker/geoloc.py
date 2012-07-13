import urllib2
import socket
import re
from xml.dom import minidom


def parse_content(tehxml):
    d = minidom.parseString(tehxml)
    coords = d.getElementsByTagName("gml:coordinates")
    if coords and coords[0].childNodes[0].nodeValue:
        lon, lat = coords[0].childNodes[0].nodeValue.split(',')
        return (lat, lon)


def get_cords(host):
    if not re.match(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b', host):
        ipaddr = socket.gethostbyname(host)
    else:
        ipaddr = host

    url = 'http://api.hostip.info/?ip=%s' % ipaddr
    try:
        result = parse_content(urllib2.urlopen(url).read())
    finally:
        pass

    return result
