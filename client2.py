#!/usr/bin/env python
#-*- encoding=utf-8 -*-
#该程序由队伍“C-moon”实现，包括钱非凡、贾潇风、陈恺凡，队长为钱非凡
#该程序主要实现读取{σ,m}并进行签名验证算法
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
    print '|          0: Get pk                   |'
    print '|          1: Verify                   |'
    print '|          2: Check Double Spending    |'
    print '|          3: Exit                     |'
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

#利用socket监听设定好的端口，接收用户发来需要验证真实性的信息。
#验证成功打印输出"[*] Right"，失败打印输出"[*] Wrong"。
#@pk：公钥
def verify(pk):
    try:
        s = socket.socket()
        s.bind((ip_client2, port_client2))
        s.listen(5)
    except Exception as e:
        print '[!]', e
        exit()

    while True:
        try:
            c, addr = s.accept()
            info = c.recv(1024)[:-1]
            print info
            if info.startswith('check'):
                check = info[6:].split('|')
                sigma = int(check[0]) #去盲化的σ值
                m = check[1] #明文数据
                c.close()
                break
            else:
                print '[-] Received something wrong...'
                c.close()
        except KeyboardInterrupt: #ctrl+c正常退出
            return

    n = pk[0]
    e = pk[1]
    H = lambda m: int(hashlib.sha256(m).hexdigest(), 16) #hash函数
    H_m = H(m) % n #付款人盲变换后的数据
    #计算付款人盲变换后的数据
    res = gmpy2.powmod(sigma, e, n)
    if res == H_m: #验证成功
        print '[*] Right'
    else: #验证失败
        print '[*] Wrong'
    return info

#检查是否双花,如果收到yes,说明不是双花则打印Checked True,否则打印Checked False
#@info：{σ,m}信息对
def check_double_spending(info):
    s = socket.socket()
    s.connect((ip_bank, port_bank))
    s.send(info + '\n')
    res = s.recv(1024)[:-1]
    if res == 'True':
        print '[*] Checked True'
    elif res == 'False':
        print '[*] Checked False'
    else:
        print '[-] Received error!'
    s.close()

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
            ip_bank = bank_info.split(' ')[0]
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
            elif c == 1: #验证σ签名是否正确
                info = verify(pk)
            elif c == 2: #利用接收到的{σ,m}检验双花
                check_double_spending(info)
            elif c == 3: #退出程序
                exit()
            else: #输入错误
                print '[-] Wrong choice!'
        except KeyboardInterrupt: #ctrl+c正常退出
            exit()
