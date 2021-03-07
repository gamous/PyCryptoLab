from functools import reduce
import random

upper=''.join([chr(i) for i in range(ord('A'),ord('Z')+1)])
lower=''.join([chr(i) for i in range(ord('a'),ord('z')+1)])
isupper=lambda c:1 if c in upper else 0
islower=lambda c:1 if c in lower else 0
isaphbt=lambda c:isupper(c) or islower(c)

gcd=lambda a,b:a if(b==0) else gcd(b,a%b)
#拓展欧几里得
ex_gcd=lambda a,b: (1,0,a) if(b==0) else (lambda t: (t[1],(t[0]-(a//b)*t[1]),t[2]))(ex_gcd(b,a%b))
#求逆
inf=lambda a,p: (lambda t: (t[0]+p)%p if t[2]==1 else (print('No Sol'),exit(0)))(ex_gcd(a,p)) 

###crt
#print(ex_gcd(2,7))
#print(inf(2,7))
def getnum(step=0):
    recv_num=[1]
    while True:
        recv=input('Input(until dot):')
        if recv=='.':return recv_num
        recv=int(recv)
        isPrime=1
        for num in recv_num:#check
            if gcd(num,recv)!=1:
                isPrime=0
                break
        if isPrime or step:
            recv_num.append(recv)
        else:
            print('Not rela prime number.')
def crt(m,b):
    M=reduce((lambda x,y:x*y),m)
    c=[M/x for x in m]
    print("模积序列Mi为:",c)
    y=list(map(inf,c,m))
    print("逆元序列y为:",y)
    r=[b[i]*c[i]*y[i] for i in range(len(m))]
    x=reduce((lambda x,y:x+y),r) % M
    return x
def test_crt():
    #print('第一步 输入互质模数')
    #m=getnum()
    m=[1,3,5,7]
    #print('第二步 输入求模余数')
    #b=getnum(step=1)
    b=[1,2,3,2]
    print("结果为:%d"%crt(m,b))
if __name__=='__main__':
    test_crt()