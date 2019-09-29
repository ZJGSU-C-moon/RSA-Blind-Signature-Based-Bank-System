#!/usr/bin/env python
#-*- encoding=utf-8 -*-
# === Author: assassinq
# === Date: 2019-09-21
import hashlib
import gmpy2
import random
import time

# 生成大素数
# @rs: 随机数种子
def getprime(rs):
    # 生成长度为1024比特的素数
    p = gmpy2.mpz_urandomb(rs, 1024)
    while not gmpy2.is_prime(p):
        p = p + 1
    return p

# 产生密钥
def keygen():
    rs = gmpy2.random_state(int(time.time()))
    p = getprime(rs)
    q = getprime(rs)
    # 计算公钥n
    n = p * q
    e = 0x10001
    H = lambda m: int(hashlib.sha256(m).hexdigest(), 16)
    # 生成公钥pk
    pk = [n, e, H]
    # 计算私钥sk
    d = gmpy2.invert(e, (p - 1) * (q - 1))
    sk = d
    # 返回公私钥对
    return pk, sk

# 签名函数
# @pk：RSA公钥
# @sk：RSA私钥
# @m：用户输入数据
def sign(pk, sk, m):
    n = pk[0]
    e = pk[1]
    H = pk[2]
    d = sk
    R = random.randrange(0, n)
    H_m = H(m) % n
    print 'Sign H(m) =', H_m
    R_e = gmpy2.powmod(R, e, n)
    M = R_e * H_m % n
    M_d = gmpy2.powmod(M, d, n)
    R_ = gmpy2.invert(R, n)
    sigma = gmpy2.mul(M_d, R_) % n
    return sigma

# 验证函数
# @pk：RSA公钥
# @sigma：盲签名结果
def verify(pk, sigma):
    n = pk[0]
    e = pk[1]
    print 'Verify H(m) =', gmpy2.powmod(sigma, e, n)

if __name__ == '__main__':
    m = raw_input('Please input your message:')
    # 获取公私钥对
    pk, sk = keygen()
    # 盲签名
    sigma = sign(pk, sk, m)
    print 'Sigma =', sigma
    # 验证签名
    verify(pk, sigma)

