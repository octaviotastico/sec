import matplotlib.pyplot as plt
import random

# Considerando que hay 26 letras de
# la A a la Z (sin contar la ñ), y
# 10 digitos del 0 al 9, tenemos un
# total de 36 caracteres distintos

# Para calcular la cantidad de palabras
# que se pueden formar de k caracteres,
# tenemos que elegir posicion por posicion algun caracter
# por lo tanto tenemos 36**n posibilidades
# para un palabra de largo n

words = 'abcdefghijklmnopqrstuvwxyz1234567890'

def random_words(k):
  return ''.join(random.choice(list(words), k))

def gen_file(name, n, k):
  with open(name, 'w+') as f:
    f.write('\n'.join([random_words(k) for i in range(n)]))

def cantidad(k):
  return len(words)**k

def sum_cantidad(k):
  # Using geometric series
  return (cantidad(k + 1) - 36) // 35 

def generate_graph():

  x = list(range(1, 21)) # Lengths
  y = [cantidad(i) for i in x] # Time calculation

  plt.plot(x, y, color="cornflowerblue", label='Tiempo para crackear')
  plt.grid(color='mediumslateblue', alpha=0.25, linestyle='-', linewidth=1)
  plt.ylabel('Tiempo (en milisegundos)')
  plt.xlabel('Cantidad de caracteres')
  plt.yscale('log')
  plt.title('Permutaciones de caracteres')
  plt.xticks(x)
  plt.show()

### A
print(f'Cantidad de palabras de largo menor o igual a 20: {sum_cantidad(20)}')

### B
generate_graph()

### C
gen_file('test', 100, 20)