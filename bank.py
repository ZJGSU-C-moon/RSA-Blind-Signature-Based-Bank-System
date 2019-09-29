#!/usr/bin/env python
#-*- encoding=utf-8 -*-
#该程序由队伍“C-moon”实现，包括钱非凡、贾潇风、陈恺凡，队长为钱非凡
#该程序主要实现RSA公私钥对生成算法、对用户端发送信息进行签名、存储并验证{σ,m}
#该程序遵循 https://blog.csdn.net/qmickecs/article/details/73556098 的建议
#完成时间：2019/09/21
import hashlib
import gmpy2
import random
import time
import socket

allcheck = []  #全局变量用来存储所有{σ,m}信息

#输入为随机数种子，返回大素数
#@rs：随机数种子
def getprime(rs):
    p = gmpy2.mpz_urandomb(rs, 1024)
    while not gmpy2.is_prime(p):
        p = p + 1
    return p

#生成公私钥对并返回
def keygen():
    rs = gmpy2.random_state(int(time.time())) #随机数种子
    p = getprime(rs)  #大素数p       
    q = getprime(rs)  #大素数q
    n = p * q         #大整数n
    e = 0x10001
    H = lambda m: int(hashlib.sha256(m).hexdigest(), 16) #hash函数
    pk = [n, e, H]   #公钥对
    d = gmpy2.invert(e, (p - 1) * (q - 1)) #私钥
    sk = d
    return pk, sk

#输入公私钥对已经盲变换后的信息,返回签名
#@pk：RSA公钥
#@sk：RSA私钥
#@M：盲化后的数据
def sign(pk, sk, M):
    n = pk[0]
    d = sk
    sigma = gmpy2.powmod(M, d, n)  #签名
    return sigma

#读取已存储的信息防止双花
#@check：{σ,m}信息
def check_double_spending(check):
    global allcheck
    if check in allcheck:
        return False
    else:
        allcheck.append(check)
        return True

#银行服务
#@s：socket信息参数
#@pk：公钥对
#@sk：私钥
def server(s, pk, sk):
    c, addr = s.accept()
    info = c.recv(1024)[:-1]
    if info.startswith('pk'):                     #如果要获取公钥传输格式为: pk 
        print '[*] Sending pk to', addr
        n = pk[0]
        e = pk[1]
        c.send(str(n) + "\n")
        c.send(str(e) + "\n")
    elif info.startswith('msg'):                  #传输的message格式为: msg:xxxxxx
        print '[*] Sending σ\' to', addr
        M = int(info[4:])
        sigmadot = sign(pk, sk, M)
        c.send(str(sigmadot) + "\n")  
    elif info.startswith('check'):                #传输的需要验证信息格式为: check:xxxxx 
        print '[*] Sending check result to', addr
        check = info[6:]
        res = check_double_spending(check)
        c.send(str(res) + "\n")
    else:
        print '[-] Message wrong!'
    c.close()

#监听端口以及各种功能的实现
#@ip：银行服务器IP地址
#@port：银行服务器端口
def listen(ip, port):
    print '[+] Listening on', (ip + ':' + str(port))
    try:
        s = socket.socket()
        s.bind((ip, port))
        s.listen(5)
    except Exception as e: #检测ip和端口能否使用
        print '[!]', e
        exit()
    pk, sk = keygen() #生成公私钥对
    while True:
        try:
            server(s, pk, sk)  #启用银行服务
        except KeyboardInterrupt: #ctrl+c正常退出
            exit()

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 9999
    while True:
        try:
            info = raw_input('Please input bank\'s ip and port (default: \'127.0.0.1 9999\'): ')
            if info == '':
                break
            ip = info.split(' ')[0]
            port = int(info.split(' ')[1])
            break
        except Exception as e: #检测端口是否为整数
            print '[!]', e
        except KeyboardInterrupt: #ctrl+c正常退出
            exit()
    listen(ip, port) #开始监听端口
