from mytools import *

###rsa
def fast_exp_mod(b, e, m):
    result = 1
    e=int(e)
    while e != 0:
        if e&1: #e是奇数
            result = (result * b) % m
        e >>= 1 #折半
        b = b*b % m
    return result

def miller_rabin(n,times): 
    if n==2: return True
    if n%2==0 or n<2 :return False
    m=n-1
    s=0
    while m&1==0:
        m=m>>1
        s+=1
    for i in range(times):
        b=fast_exp_mod(random.randint(2,n-1),m,n)
        if b==1 or b==n-1:
            continue
        for j in range(s-1):
            b=fast_exp_mod(b,2,n)
            if b==n-1:
                break
        else:
            return False
    return True

def create_prime(keylen):
    while True:
        n=random.randint(2**(keylen-1),2**(keylen))
        if(miller_rabin(n,8)==True):return n

def create_keys(keylen):
    p,q=create_prime(keylen),create_prime(keylen)
    n=p*q
    phi=(p-1)*(q-1)
    while True: #从pq选择e，实际中更多是固定e，筛选pq
        e=random.randint(7,phi)
        if gcd(e,phi)==1:break
    d=inf(e,phi)
    PU=(e,n)#公钥
    PR=(d,n)#私钥
    return PU,PR

def rsa_encrypt(M, e, n):
    return fast_exp_mod(M, e, n)
def rsa_decrypt( C, d, n):
    return fast_exp_mod(C, d, n)

def string_decode(str):
    return reduce(lambda x,y:x*0x100+y,list(map(ord,str)))
def string_encode(num):
    str=''
    while num>0:
        str+=chr(num&0xff)
        num=num>>8
    return str[::-1]
def test_rsa():
    #plain=input()
    plain="Hello"
    print('明文为: ',plain)
    M=string_decode(plain)
    print('明文编码为: ',hex(M))
    PU,PR=create_keys(20)
    print('...生成密钥中...')
    print('公钥为：',PU)
    print('私钥为：',PR)
    print('...公钥加密中...')
    C=rsa_encrypt(M,PU[0],PU[1])
    print('密文编码为: ',hex(C))
    cipher=string_encode(C)
    print('密文为: ',cipher ,'/',(bytes(cipher.encode(encoding='utf-8'))))
    print('...私钥解密中...')
    M=rsa_encrypt(C,PR[0],PR[1])
    print('解密编码为: ',hex(M))
    res=string_encode(M)
    print('解密明文为: ',res)    
if __name__ == "__main__":
    test_rsa()