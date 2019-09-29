#!/usr/bin/env python
import re

def check_ip(ip):
    if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip):
        print "IP vaild"
        return True
    else:
        print "IP invaild"
        return False

if __name__ == '__main__':
    ip = raw_input('Please input an IP address:')
    print check_ip(ip)
