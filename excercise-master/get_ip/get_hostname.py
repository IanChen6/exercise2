# -*- coding:utf-8 -*-
__author__ = 'IanChen'
import socket

hostnamne=socket.gethostname()
print(hostnamne)
ip=socket.gethostbyname(hostnamne)
print(ip)