#!/usr/bin/env python
import socket

def listen(ip, port):
    s = socket.socket()
    s.bind((ip, port))
    s.listen(5)
    while True:
        c, addr = s.accept()
        info = c.recv(1024)
        print 'recv:', info
        c.close()

if __name__ == '__main__':
    listen('0.0.0.0', 9999)

