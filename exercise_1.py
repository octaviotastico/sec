from itertools import permutations as p
import matplotlib.pyplot as plt
from math import perm
import numpy as np

# Considerando que hay 26 letras de
# la A a la Z (sin contar la ñ), y
# 10 digitos del 0 al 9, tenemos un
# total de 36 caracteres distintos

# Para calcular la cantidad de palabras
# que se pueden formar de k caracteres,
# tenemos que calcular las permutaciones
# de 36 y k (nPr(36, k)) donde k es la
# longitud del string que queremos generar.
# Es decir, un total de -> 36! / (36-k)!

# Si quisieramos saber ese numero para
# un k que no esta fijo, sino que en un
# rango, por ejemplo, 1 <= k <= 20,
# simplemente tenemos que hacer la sumatoria
# de las permutaciones de todos los k

words = 'abcdefghijklmnñopqrstuvwxyz1234567890'
# all_perms = lambda : sum([list(map(list, p(words, i))) for i in range(len(words) + 1)], [])

def random_words(k):
  return ''.join(np.random.choice(list(words), k))

def gen_file(n, k):
  f = open('dict', 'w+')
  for i in range(n):
    f.write(random_words(k) + '\n')

def n_all_perm(k = 36):
  n = 0
  for i in range(1, k + 1):
    n += perm(36, i)
  return n

def generate_graph():

  x = list(range(1, 21)) # Lengths
  y = [ perm(i, i) for i in range(1, 21) ] # Time calculation all perms of lengths

  plt.plot(x, y, color="cornflowerblue", label='Tiempos de crackeo')
  plt.grid(color='mediumslateblue', alpha=0.25, linestyle='-', linewidth=1)
  plt.ylabel('Tiempo (en milisegundos)')
  plt.xlabel('Cantidad de caracteres')
  plt.yscale('log')
  plt.title('Permutaciones de caracteres')
  plt.show()

### A
print(f'Todas las permutaciones posibles de longitud 1 \nhasta 20 son: {n_all_perm(20)}')

### B
generate_graph()

### C
gen_file(100, 20)