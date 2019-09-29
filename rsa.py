#!/usr/bin/env python
#-*- encoding=utf-8 -*-
# === Author: assassinq
# === Date: 2019-09-21
import hashlib
import gmpy2
import time
import libnum

# 生成大素数
def getprime(rs):
    p = gmpy2.mpz_urandomb(rs, 1024)
    while not gmpy2.is_prime(p):
        p = p + 1
    return p

# 产生密钥
def keygen():
    rs = gmpy2.random_state(int(time.time()))
    p = getprime(rs)
    q = getprime(rs)
    n = p * q
    e = 0x10001
    pk = [n, e]
    d = gmpy2.invert(e, (p - 1) * (q - 1))
    sk = d
    return pk, sk

def encrypt(m, e, n):
    m = libnum.s2n(m)
    return gmpy2.powmod(m, e, n)

def decrypt(c, d, n):
    m = gmpy2.powmod(c, d, n)
    return libnum.n2s(m)

if __name__ == '__main__':
    pk, sk = keygen()
    n = pk[0]
    e = pk[1]
    d = sk
    m = raw_input('Please input your message:')
    c = encrypt(m, e, n)
    print 'This is ciphertext:', c
    res = decrypt(c, d, n)
    print 'This is plaintext:', res

