#S-box和P变换设计原理。
#多轮加密原理。
#子密钥产生原理
#解密对称原理 
_block_size=8
#S_box
S_box=[
[#s1
    [14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
    [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
    [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
    [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13] ],
[#s2
    [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
    [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
    [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
    [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9] ],
[#s3
    [10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
    [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
    [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
    [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12] ],
[#s4
    [ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
    [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
    [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
    [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14] ],
[#s5  
    [ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
    [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
    [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
    [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3] ],
[#s6
    [12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
    [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
    [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
    [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13] ],
[#s7   
    [ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
    [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
    [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
    [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12] ],
[#s8
    [13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
    [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
    [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
    [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11] ]
]
#初始置换
IP_table=[
58, 50, 42, 34, 26, 18, 10, 2,
60, 52, 44, 36, 28, 20, 12, 4,
62, 54, 46, 38, 30, 22, 14, 6,
64, 56, 48, 40, 32, 24, 16, 8,
57, 49, 41, 33, 25, 17,  9, 1,
59, 51, 43, 35, 27, 19, 11, 3,
61, 53, 45, 37, 29, 21, 13, 5,
63, 55, 47, 39, 31, 23, 15, 7 
]
#初始逆置换
INV_IP_table=[
40,  8, 48, 16, 56, 24, 64, 32,
39,  7, 47, 15, 55, 23, 63, 31,
38,  6, 46, 14, 54, 22, 62, 30,
37,  5, 45, 13, 53, 21, 61, 29,
36,  4, 44, 12, 52, 20, 60, 28,
35,  3, 43, 11, 51, 19, 59, 27,
34,  2, 42, 10, 50, 18, 58, 26,
33,  1, 41,  9, 49, 17, 57, 25 
]
#P盒
P_box=[
16,  7, 20, 21, 29, 12, 28, 17,
 1, 15, 23, 26,  5, 18, 31, 10,
 2,  8, 24, 14, 32, 27,  3,  9,
19, 13, 30,  6, 22, 11,  4, 25 
]

#置换选择1 64->56
KEY_table1=[ 
57, 49, 41, 33, 25, 17,  9,
 1, 58, 50, 42, 34, 26, 18,
10,  2, 59, 51, 43, 35, 27,
19, 11,  3, 60, 52, 44, 36,
63, 55, 47, 39, 31, 23, 15,
 7, 62, 54, 46, 38, 30, 22,
14,  6, 61, 53, 45, 37, 29,
21, 13,  5, 28, 20, 12,  4 
]
#置换选择2 56->48
KEY_table2=[
14, 17, 11, 24,  1,  5,
 3, 28, 15,  6, 21, 10,
23, 19, 12,  4, 26,  8,
16,  7, 27, 20, 13,  2,
41, 52, 31, 37, 47, 55,
30, 40, 51, 45, 33, 48,
44, 49, 39, 56, 34, 53,
46, 42, 50, 36, 29, 32 
]
# 密钥移位表
KEY_shift_step = [ 1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2,2, 1 ]
# 拓展置换表
EXTEND_table=[
32,  1,  2,  3,  4,  5,
 4,  5,  6,  7,  8,  9,
 8,  9, 10, 11, 12, 13,
12, 13, 14, 15, 16, 17,
16, 17, 18, 19, 20, 21,
20, 21, 22, 23, 24, 25,
24, 25, 26, 27, 28, 29,
28, 29, 30, 31, 32,  1 
]
#生成子密钥
def left_shift(l, step):
    return l[step:] + l[:step]
def gen_subkey(key):
    subkey = []
    #置换选择1
    key0 = [key[KEY_table1[i]-1] for i in range(56)]
    #生成16轮密钥
    for i in range(16):
        #分组
        lo16 = key0[0:28]
        hi16 = key0[28:56]
        #左移
        lo16 = left_shift(lo16, KEY_shift_step[i])
        hi16 = left_shift(hi16, KEY_shift_step[i])
        #合并
        key0 = lo16 + hi16
        #置换选择2
        key1=[key0[KEY_table2[i]-1] for i in range(48)]
        subkey.append(key1)
    return subkey
#0~15 int -> 4 bit_str_list
def int2bit(n,len=4):
    return list(map(int,(bin(n).split('0b')[-1]).rjust(len,'0')[-len:]))
def bytes2int(_bytes):
    res=0
    for i in _bytes:
        res=(res<<8)+(i&0xff)
    return res
def bytes2bit(text):#64
    return int2bit(bytes2int(text),64)
def int2bytes(num):
    res=b''
    while num>0:
        res+=bytes([num&0xff])
        num=num>>8
    return res[::-1]
def bit2bytes(bits):
    return int2bytes(int(''.join(map(str,bits)),2))
#IP置换
def permute_IP(text):   
    return [text[IP_table[i]-1] for i in range(64)]
#IP逆置换
def permute_INV_IP(text): 
    return [text[INV_IP_table[i]-1] for i in range(64)]
#print(permute_INV_IP(permute_IP([i for i in range(64)])))
#拓展变换 32->48 bit
def permute_Extend(text):
    return [text[EXTEND_table[i] - 1] for i in range(48)]
#print(permute_Extend([i%2 for i in range(32)]))
#48 bit->32bit 
def permute_S(text):
    chunks=[text[i:i + 6] for i in range(0, 48, 6)]
    res=[]
    for i in range(8):
        chunk=chunks[i]
        row=int(str(chunk[0])+str(chunk[-1]),2)
        col=int(''.join([str(i) for i in chunk[1:-1]]),2)
        res+=int2bit(S_box[i][row][col])
    return res
#P置换部分 32->32 bit
def permute_P(text):
    return [text[P_box[i]-1] for i in range(32)]
#定长数组异或
def xor(bit1, bit2,num):
    return [bit1[i]^bit2[i] for i in range(num)]
#f函数
def f(right,subkey):
	return permute_P(permute_S(xor(permute_Extend(right),subkey,48)))
#迭代置换 32,32-f->32,32 16轮
def iterator(text,subkey):
    hi32,lo32=text[32:],text[:32]
    for i in range(16):
        lo32,hi32=hi32,xor(f(hi32,subkey[i]),lo32,32)
    return permute_INV_IP(hi32+lo32)
#明文加密 64->64
def des_encrypt(plain,key):
    plain=bytes2bit(plain[:8])
    key=bytes2bit(key)
    return bit2bytes(iterator(permute_IP(plain),gen_subkey(key)))
#密文解密 64->64
def des_decrypt(cipher,key):
    cipher=bytes2bit(cipher[:8])
    key=bytes2bit(key)
    return bit2bytes(iterator(permute_IP(cipher),gen_subkey(key)[::-1]))
#单元测试
def test_des():
    M=b'gamous23'
    K=b'mykey123'
    C=des_encrypt(M,K)
    print(C)
    P=des_decrypt(C,K)
    print(P)
    assert M==P
if __name__ == "__main__":
    test_des()
