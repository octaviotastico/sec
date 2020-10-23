exploit = b'A'*70 + b'\x04' + b'\x03' + b'\x02' + b'\x01' + b'A'*6 + b'DCBA'
f = open('crack_01_02', 'wb')
f.write(exploit)
f.close()
