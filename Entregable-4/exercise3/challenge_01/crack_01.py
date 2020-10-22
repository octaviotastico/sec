exploit = 'A'*80 + 'DCBA'
f = open('crack_01', 'wb')
f.write(exploit)
f.close()