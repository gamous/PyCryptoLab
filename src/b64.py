def b64encode(s):
    table='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    lack=-len(s)%3
    #to bits
    st=''.join(list(map(lambda a: '{:08b}'.format(ord(a)),s)))+lack*8*'0'
    #split with step 6
    sl=[st[i*6:i*6+6] for i in range(int(len(st)/6)-lack)]
    #build string
    res= ''.join(list(map(lambda s: table[int(s,2)],sl)))+'='*lack
    return res
def b64decode(s):
    table='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    lack=s[-3:].count('=')
    li=list(map(table.index,s[:-lack]if lack else s))
    bits=''.join(list(map(lambda a: '{:06b}'.format(a),li)))
    li=[bits[i*8:i*8+8] for i in range(int(len(bits)/8))]
    res= ''.join(list(map(lambda b:chr(int(b,2)),li)))
    return res
if __name__=="__main__":
    print(b64encode('gamma{'))