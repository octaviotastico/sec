password = "5tr0vZBrX:xTyR-P!"

real = ""

for i in range(len(password)):
    real += chr(ord(password[i]) ^ i)

print(real) # 5up3r_DuP3r_u_#_1