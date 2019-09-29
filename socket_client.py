#!/usr/bin/env python
import socket

def nc(ip, port):
    s = socket.socket()
    s.connect((ip, port))
    s.send('Hello')
    s.close()

if __name__ == '__main__':
    nc('0.0.0.0', 9999)

