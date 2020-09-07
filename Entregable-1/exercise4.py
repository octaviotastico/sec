import matplotlib.pyplot as plt
from collections import Counter
import os

prefx = {}
times = {}
BASE = './Tools/Dicts/SecLists/Passwords/'

def search_names(DIR):
  for dictionary in os.listdir(DIR):
    if os.path.isdir(os.path.join(DIR + dictionary)):
      search_names(DIR + dictionary + '/')
    else:
      print(f'Analizyng: {DIR + dictionary}')
      DICT = open(DIR + dictionary, 'r+', encoding='utf-8', errors='ignore').read().split('\n')
      for name in DICT:
        if name[:4] in prefx:
          prefx[name[:4]] += 1
        else:
          prefx[name[:4]] = 1
        if name in times:
          times[name] += 1
        else:
          times[name] = 1

def plot_frequency(x, y, t, s):
  bar_list = plt.bar(x, y, color='cornflowerblue', width=1, align='center')

  colors = 0
  for bar in bar_list:
    bar_list[colors].set_color('cornflowerblue') if colors % 2 else bar_list[colors].set_color('mediumslateblue')
    colors += 1

  plt.ylabel(s)
  plt.title(t)
  plt.xticks(rotation=75)
  plt.show()

def main():
  search_names(BASE)
  plot_frequency(
    dict(Counter(times).most_common(10)).keys(),
    dict(Counter(times).most_common(10)).values(),
    'Top 10 nicknames mas comunes',
    'Cantidad de apariciones de nicknames'
  )
  plot_frequency(
    dict(Counter(prefx).most_common(10)).keys(),
    dict(Counter(prefx).most_common(10)).values(),
    'Top 10 prefijos mas comunes',
    'Cantidad de apariciones de prefijos'
  )

main()
