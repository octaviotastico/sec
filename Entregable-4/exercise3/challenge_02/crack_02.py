exploit = b'A'*70 + b'\x01' + b'\x02' + b'\x03' + b'\x04'
f = open('crack_02', 'wb')
f.write(exploit)
f.close()