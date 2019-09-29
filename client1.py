#!/usr/bin/env python
#-*- encoding=utf-8 -*-
#该程序由队伍“C-moon”实现，包括钱非凡、贾潇风、陈恺凡，队长为钱非凡
#该程序主要实现对消息进行盲变换、对盲变换的信息进行去盲变换算法
#该程序遵循 https://blog.csdn.net/qmickecs/article/details/73556098 的建议
#完成时间：2019/09/21
import hashlib
import gmpy2
import random
import time
import socket

#欢迎界面
def welcome():
    print ' --- Welcome to C-moon Bank System! --- '
    print '|      0: Get pk                       |'
    print '|      1: Calculate M and get σ\'       |'
    print '|      2: Calculate σ and send {σ,m}   |'
    print '|      3: Exit                         |'
    print ' -------------------------------------- '

#获取公钥
def getpk():
    s = socket.socket()
    s.connect((ip_bank, port_bank))
    s.send('pk\n')
    time.sleep(0.5)
    info = s.recv(1024).split('\n')
    n = int(info[0])
    e = int(info[1])
    print '[*] n =', n
    print '[*] e =', e
    H = lambda m: int(hashlib.sha256(m).hexdigest(), 16)
    pk = [n,e,H]
    s.close()
    return pk

#计算M的值
#@R：付款人获取的随机数，范围在0～n之间
#@pk：RSA公钥
#@m：明文数据
def CalM(R, pk, m):
    n = pk[0]
    e = pk[1]
    H = pk[2]
    #付款人信息输入点
    H_m = H(m) % n
    R_e = gmpy2.powmod(R, e, n)
    M = R_e * H_m % n
    return M

#获取σ'的值
#@M：盲化后的数据
def GetSigmadot(M):
    s = socket.socket()
    s.connect((ip_bank, port_bank))
    s.send('msg:' + str(int(M)) + '\n')
    sigmadot = int(s.recv(1024))
    s.close()
    return sigmadot

#计算σ的值
#@R：付款人获取的随机数，范围在0～n之间
#@pk：RSA公钥
#@m：明文数据
#@sigma：σ的值
def CalSigma(R, pk, m, sigmadot):
    n = pk[0]
    R_ = gmpy2.invert(R, n)
    sigma = gmpy2.mul(sigmadot, R_) % n
    print '[+] σ =', sigma
    check = str(int(sigma)) + '|' + m
    while True:
        try:
            s = socket.socket()
            s.connect((ip_client2, port_client2))
            s.send('check:' + str(check) + '\n')
            s.close()
            break
        except Exception as e: #每隔5秒尝试连接client2
            print '[!]', e
            time.sleep(5)

if __name__ == '__main__':
    global ip_bank
    global port_bank
    global ip_client2
    global port_client2

    ip_bank = '127.0.0.1'
    port_bank = 9999
    ip_client2 = '127.0.0.1'
    port_client2 = 11111

    #输入需要连接的银行服务器ip:port
    while True:
        try:
            bank_info = raw_input('Please input bank\'s ip and port (default: 127.0.0.1 9999): ')
            if bank_info == '':
                break
            ip_bank= bank_info.split(' ')[0]
            port_bank = int(bank_info.split(' ')[1])
            break
        except Exception as e:
            print '[!]', e
        except KeyboardInterrupt: #ctrl+c正常退出
            exit()
    
    #输入需要连接的卖方服务器ip:port
    while True:
        try:
            client2_info = raw_input('Please input client2\'s ip and port (default: 127.0.0.1 11111): ')
            if client2_info == '':
                break
            ip_client2 = client2_info.split(' ')[0]
            port_client2 = int(client2_info.split(' ')[1])
            break
        except Exception as e:
            print '[!]', e
        except KeyboardInterrupt: #ctrl+c正常退出
            exit()

    while True:
        try:
            welcome()
            c = raw_input('Your choice:')
            c = int(c)

            if c == 0: #获取公钥
                try:
                    pk = getpk()
                except Exception as e:
                    print '[!]', e
            elif c == 1: #计算M值
                try:
                    n = pk[0]
                    R = random.randrange(0, n) #获取随机数R
                    m = raw_input('Please input your data:')
                    M = CalM(R, pk, m)
                    print '[+] M =', M
                    sigmadot = GetSigmadot(M)  #发送盲化后的M并接收银行发送的签名
                    print '[+] σ\' =', sigmadot
                except Exception as e:
                    print '[!]', e
            elif c == 2: #计算σ值
                try:
                    CalSigma(R, pk, m, sigmadot)
                except Exception as e:
                    print '[!]', e
            elif c == 3: #退出
                exit()
            else: #输入错误
                print '[-] Wrong choice!'
        except KeyboardInterrupt: #ctrl+c正常退出
            exit()
