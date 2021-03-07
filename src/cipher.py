import aes,des
import argparse,sys,base64
_encodeing='utf-8'
_block_mode='ecb'
_crypto_mothed='aes'
_block_size=16
_block_iv=b"".join([bytes([i]) for i in range(16)])
_encrypt_func=getattr(sys.modules[_crypto_mothed],_crypto_mothed+'_encrypt')
_decrypt_func=getattr(sys.modules[_crypto_mothed],_crypto_mothed+'_decrypt')

def cut_bytes(_bytes):
    res=[_bytes[i:i+_block_size] for i in range(0,len(_bytes),_block_size)]
    res[-1]=res[-1].ljust(_block_size,b'\0')
    return res
def gen_key(_str):
    return bytes(_str.ljust(_block_size,'\0'),encoding=_encodeing)[0:_block_size]
def getfunc(funcname):
    return getattr(sys.modules[__name__],funcname)
def xor_block(b1, b2):
    return bytes([b1[i] ^ b2[i] for i in range(_block_size)])

def ecb_encrypt(data,key):
    plain=cut_bytes(data)
    cipher=b''.join([_encrypt_func(p,key) for p in plain])
    return cipher
def ecb_decrypt(data,key):
    cipher=cut_bytes(data)
    plain=b''.join([_decrypt_func(c,key) for c in cipher])
    return plain.rstrip(b'\0')

def cbc_encrypt(data,key):
    plain=cut_bytes(data)
    block=_block_iv
    cipher=b''
    for p in plain:
        block=_encrypt_func(xor_block(p,block),key)
        cipher+=block
    return cipher
def cbc_decrypt(data,key):
    cipher=cut_bytes(data)
    block=_block_iv
    plain=b''
    for c in cipher:
        plain+=xor_block(_decrypt_func(c,key),block)
        block=c
    return plain.rstrip(b'\0')

def encrypt(data,key):
    return getfunc(_block_mode+'_encrypt')(data,key)
def decrypt(data,key):
    return getfunc(_block_mode+'_decrypt')(data,key)

def encrypt_str(text,key):
    text=bytes(text,encoding=_encodeing)
    key=gen_key(key)
    C=encrypt(text,key)
    return C
def decrypt_str(text,key):
    text=base64.b64decode(text.encode(encoding="ascii"))
    key=gen_key(key)
    P=decrypt(text,key)
    return P

def encrypt_file(source,key):
    with open(source,'rb') as fp:
        data=fp.read()
    key=gen_key(key)
    C=encrypt(data,key)
    return C
def decrypt_file(source,key):
    with open(source,'rb') as fp:
        data=fp.read()
    key=gen_key(key)
    P=decrypt(data,key)
    return P


def check_argv(keywords,argvs):
    for keyword in keywords:
        if keyword in argvs:
            return True
    return False

def _read_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group=group.add_mutually_exclusive_group()
    group.add_argument(
        '-c', '--ciphertext',
        default=None,
        help='cipher text to decrypt',
    )
    group.add_argument(
        '-p', '--plaintext',
        default=None,
        help='plain text to encrypt',
    )
    group.add_argument(
        '-C', '--cipherfile',
        default=None,
        help='cipher file to decrypt',
    )
    group.add_argument(
        '-P', '--plainfile',
        default=None,
        help='plain file to encrypt',
    )
    parser.add_argument(
        '-o', '--output',
        default=None,
        help='output path',
    )
    parser.add_argument(
        '-m', '--mothed',
        default='aes',
        help='crypto mothed',
        metavar='des|aes'
    )
    parser.add_argument(
        '-M', '--mode',
        default='ecb',
        help='block encrypt mode',
        metavar='cbc|ecb'
    )
    parser.add_argument(
        '-k', '--key',
        default=None,
        help='key to encrypt or decrypt',
    )
    parser.add_argument(
        '-i', '--iv',
        default=None,
        help='block encrypt init vector (default:[0..f])',
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='cipher-system 1.0.0 by gamous 2020.12.31',
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = _read_args()
    #init
    if check_argv(['ecb','cbc'],args.mode):
        _block_mode=args.mode
    else:
        print('fatal: unrecognized mode %s'%args.mode)
        exit(-1)
    if check_argv(['aes','des'],args.mothed):
        _crypto_mothed=args.mothed
        _block_size=getattr(sys.modules[_crypto_mothed],'_block_size')
        _encrypt_func=getattr(sys.modules[_crypto_mothed],_crypto_mothed+'_encrypt')
        _decrypt_func=getattr(sys.modules[_crypto_mothed],_crypto_mothed+'_decrypt')
    else:
        print('fatal: unrecognized mothed %s'%args.mothed)
        exit(-1)
    if(args.iv):
        _block_iv=gen_key(args.iv)
    if(args.plaintext):
        data=encrypt_str(args.plaintext,args.key)
        print(base64.b64encode(data).decode())
    elif(args.ciphertext):
        data=decrypt_str(args.ciphertext,args.key)
        #print(data.decode())
        print(data)
    if(args.plainfile):
        data=encrypt_file(args.plainfile,args.key)
        if(not args.output):
            print('warning: output path not found')
    elif(args.cipherfile):
        data=decrypt_file(args.cipherfile,args.key)
        if(not args.output):
            print('warning: output path not found')
    if(args.output):
        with open(args.output,'wb+') as fp:
            fp.write(data)
            print('write success!')
    