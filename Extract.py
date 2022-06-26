import struct
import json

data = open('shop.bin','rb').read()
menu = json.load(open('menu.json'))
item = json.load(open('item.json'))
shopnames = json.load(open('shopnames.json'))
f = {}

def beautify(number,digits=3):
    text = hex(number)[2:].upper()
    text = text.zfill(digits)
    return text

def count(address,file=data):
    return struct.unpack('H',file[address:address+2])[0]

#Shop -> Inventory -> Product
shopamount = count(6)
shopoffset = 0x10

for i in range(shopamount):
    shopdata = []
    shop = shopoffset + 0x18*i
    shop = data[shop:shop+0x18]
    invamount = count(0x10,shop)
    invoffset = count(0x14,shop)
    for j in range(invamount):
        invdata  = {}
        prodlist = []
        prodname = []
        inv = invoffset + 8*j
        inv = data[inv:inv+8]
        invflag = beautify(count(0,inv),2)
        if invflag in menu:
            invname = menu[invflag]
        else:
            invname = 'Always Unlocked'
        prodamount = count(2,inv)
        prodoffset = count(4,inv)
        for k in range(prodamount):
            prod = prodoffset + 2*k
            prod = data[prod:prod+2]
            prod = beautify(count(0,prod))
            prodlist.append(prod)
            prodname.append(item[prod])
        invdata['Menu Flag'] = invflag
        invdata['Menu Flag Name'] = invname
        invdata['Products'] = prodlist
        invdata['Product Names'] = prodname
        shopdata.append(invdata)
    f[shopnames[beautify(count(4,shop))]] = shopdata

json.dump(f,open('result.json','w'),indent='\t')
