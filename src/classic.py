from mytools import *
from thisthis import *

###caser
caser=lambda s,offset:''.join(map(lambda i:chr(((ord(i)-ord('A')+offset )%26+ord('A'))if isupper(i) else ((ord(i)-ord('a')+offset)%26+ord('a'))if islower(i) else ord(i)),s))
caser_encode=caser
caser_decode=lambda s,o:caser(s,-o%26)
def caser_brute(cipher):
    try:
        for i in range(1,26):
            test=caser(cipher,i)
            #print test
            if 'Zen' in test: ###只是判断python之禅,实际应该用词法测试来判别
                print( test)
                print('key is:'+str(i))
                assert 0==1
        print('Not Found')
    except:
        print('Found')
def caser_test():
    print('...凯撒加密...')
    plain="Python Zen is too long."
    print("明文为:",plain)
    cipher=caser(plain,random.randint(1,25))
    print("密文为:",cipher)
    print('破解明文：')
    caser_brute(cipher)
    print()


###allfine
allfine_encode=lambda k1,k2,text:''.join(list(map((lambda c:(upper[(k1*upper.index(c)+k2)%26]if isupper(c) else lower[(k1*lower.index(c)+k2)%26])if isaphbt(c) else c),str(text))))
allfine_decode=lambda k1,k2,text:''.join(list(map((lambda c:(upper[(k1*(upper.index(c)-k2))%26]if isupper(c) else lower[(k1*(lower.index(c)-k2))%26])if isaphbt(c) else c),str(text))))
def allfine_test():
    print('...仿射加密...')
    goodkey=[i for i in range(1,26)if gcd(i,26)==1]
    print('密钥空间：',goodkey)
    E_key=[7,3]
    print('所选加密密钥：',E_key)
    #E_key[0]=int(input('请输入第一个密钥，和26互素: '))
    #E_key[1]=int(input('请输入第一个密钥，和26互素: '))
    D_key=[0]*2
    D_key[0]=E_key[0]**11 % 26                  #快速求逆，这里用了欧拉定理求逆
    D_key[1]=E_key[1]
    print('计算解密密钥：',D_key)
    plain="Allfine also easy to crack"
    print("明文为:",plain)
    cipher=allfine_encode(E_key[0],E_key[1],plain)
    print("密文为:",cipher)
    result=allfine_decode(D_key[0],D_key[1],cipher)
    print("解密结果为:",result)
    print()
    
###vigenere
vigenere_shift=lambda message,key,op: ''.join(list(map(lambda i:(lambda c,key:lower[(ord(c.lower())-ord('a')+key)%26] if isaphbt(c) else c)(message[i],list(map(lambda b:((ord(b)-ord('a'))*op)%26,key.lower()))[i%len(key)]),[i for i in range(len(message))])))
vigenere_encode=lambda x,key:vigenere_shift(x,key,1)
vigenere_decode=lambda x,key:vigenere_shift(x,key,-1)
def vigenere_test():
    print('...维吉尼亚加密...')
    keystream='gamous'
    print('密钥流为：',keystream)
    plain="Vigenere is safer than Allfine"
    print("明文为:",plain)
    cipher=vigenere_encode(plain,keystream)
    print("密文为:",cipher)
    result=vigenere_decode(cipher,keystream)
    print("解密结果为:",result)
    print()

if __name__ == "__main__":
    print('')
    caser_test()
    allfine_test()
    vigenere_test()
    