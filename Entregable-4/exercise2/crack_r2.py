A = "kw6PZq3Zd;ekR[_1"

nuestro = []

def imul(edx, eax):
    x = edx * eax
    return x>>32, x&0xffffffff

def doit(i):
    eax = ecx = i + 1
    ebx = ord(A[i])
    edx = 0x66666667

    edx, eax = imul(edx, eax)

    edx >>= 3
    eax = ecx >> 31
    edx -= eax
    eax = (edx << 2) + edx
    eax <<= 2
    edx = ecx - eax
    eax = edx
    eax ^= ebx

    important = eax & 0xff

    nuestro.append(important)

for i in range(len(A)): doit(i)

res = ""
for i in range(len(nuestro)): res += chr(nuestro[i])
print(res) # ju5T_w4Rm1ng_UP!