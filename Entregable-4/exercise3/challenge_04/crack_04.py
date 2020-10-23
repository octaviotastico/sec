import os

f = open('asd2.txt', 'wb+')
f.write(b'\x01\x04\x00\x80' + b'\x42\x00\x00\x00' * 1024 + b'\x01\x00\x00\x00')
f.close()
