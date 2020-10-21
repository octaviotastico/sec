key = 'kw6PZq3Zd;ekR[_1'
res = ''

def imul(edx, eax):
  x = edx * eax
  return x>>32, x & 0xffffffff

for i in range(len(key)):
  ebx = key[i]
  ecx = i + 1
  edx, eax = imul(0x66666667, ecx)
  eax = ecx >> 0x1f
  edx = (edx >> 3) - eax
  eax = edx
  eax <<= 2
  eax += edx
  eax <<= 2
  edx = ecx
  edx -= eax
  eax = edx
  eax ^= ord(ebx)
  res += chr(eax & 0xFF)

print(res) # ju5T_w4Rm1ng_UP!