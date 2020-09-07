import matplotlib.pyplot as plt
import os

times = {}
BASE = './Tools/Dicts/SecLists/Passwords/'
EKO = open('./Tools/Dicts/eko.dict').read().split('\n')

def search_names(DIR):
  for dictionary in os.listdir(DIR):
    if os.path.isdir(os.path.join(DIR + dictionary)):
      search_names(DIR + dictionary + '/')
    else:
      print(f'Analizyng: {DIR + dictionary}')
      DICT = open(DIR + dictionary, 'r+', encoding='utf-8', errors='ignore').read()
      for name in EKO:
        if name in DICT:
          times[name] += 1

def plot_frequency():
  colors = 0
  bar_list = plt.bar(times.keys(), times.values(), color="cornflowerblue", width=1, align='center')
  for bar in bar_list:
    if colors % 2:
      bar_list[colors].set_color('cornflowerblue')
    else:
      bar_list[colors].set_color('mediumslateblue')
    colors += 1

  plt.ylabel('Cantidad de apariciones')
  plt.title('Frecuencia de aparicion')
  plt.xticks(rotation=75)
  plt.show()

def main():
  for name in EKO:
    times[name] = 0
  search_names(BASE)
  plot_frequency()

main()
