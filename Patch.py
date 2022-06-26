import struct
import json

source = json.load(open('result.json'))
header = open('shop_header.bin','rb').read()
data   = bytearray(header)

#Parse json file
invall     = [] #Lists all inventory/product (not including duplicates)
invoffsets = {} #Lists code -> offset for all inventory/product
invoffset  = 0  #Offset of all inventory/product *so far*
produniq    = [] #Used for the very end of the file
prodall     = []
prodoffsets = {}
prodoffset  = 0
for i in source.values():
    invcode = ''
    for j in i:
        #Make names irrelevant
        del j['Menu Flag Name']
        del j['Product Names']
        invcode += j['Menu Flag']
        x = j['Products']
        if len(x) == 0:
            invcode += 'ZZZZ'
        prodcode = ''
        for k in x:
            prodcode += k
            invcode  += k
            if k not in produniq:
                produniq.append(k)
        if prodcode not in prodoffsets:
            prodall.append(x)
            prodoffsets[prodcode] = prodoffset
            prodoffset += 2*len(x)
    if invcode not in invoffsets:
        invall.append(i)
        invoffsets[invcode] = invoffset
        invoffset += 8*len(i)

#Make bin file
#SHOP
for i in range(len(source)):
    x = 0x10 + 0x18*i
    y = list(source.values())[i]
    z = invall.index(y)
    z = list(invoffsets.values())[z]
    data[x+0x10:x+0x12] = struct.pack('H',len(y))
    data[x+0x14:x+0x16] = struct.pack('H',z+len(header))
#INVENTORY
for i in invall:
    for j in i:
        x = j['Products']
        y = prodall.index(x)
        y = list(prodoffsets.values())[y]
        data += struct.pack('H',int(j['Menu Flag'],16))
        data += struct.pack('H',len(x))
        data += struct.pack('I',y+len(header)+invoffset)
#PRODUCT
for i in prodall:
    for j in i:
        data += struct.pack('H',int(j,16))
#UNIQUE PRODUCTS
data[0xC:0x10] = struct.pack('I',len(data))
for i in produniq:
    data += struct.pack('H',int(i,16))
data += bytearray(2) #Null-termination
#Padding
z = 0x10A0 - len(data)
if z < 0:
    print('OFFSET ERROR! FILE TOO LONG!')
    raise Exception()
else:
    print(z,'free bytes available.')
    data += bytearray(z)

f = open('shop.bin','wb')
f.write(data)
f.close()
