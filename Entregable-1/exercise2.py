import os, sys

args = sys.argv

MODE = 'SHA1'
DIR = './dicts/'
PWD = '941d4637d8223d958d7f2324572c7e319dcea01f'

def get_args():
  global MODE
  global DIR
  global PWD

  if '-d' in args:
    DIR = args[ args.index('-d') + 1 ]
  if '--dir' in args:
    DIR = args[ args.index('--dir') + 1 ]
  if '-m' in args:
    MODE = args[ args.index('--m') + 1 ]
  if '--mode' in args:
    MODE = args[ args.index('--mode') + 1 ]
  if '-p' in args:
    PWD = args[ args.index('-p') + 1 ]
  if '--pwd' in args:
    PWD = args[ args.index('--pwd') + 1 ]

def get_algorithms():
  if MODE == 'ALL':
    algorithms = os.popen('hashcat -h | grep MD4 -A212 | cut -d"|" -f1 | sort | uniq').read()
    algorithms = algorithms.replace(' ', '')[:-1].split('\n')
  else:
    algorithms = os.popen(f'hashcat -h | grep {MODE} -m1 | cut -d"|" -f1').read()
    algorithms = algorithms.replace(' ', '').split('\n')[:-1]
  return algorithms

def crack_pwd(dictionary, algorithms):
  for alg in algorithms:
    output = os.popen(f'hashcat --generate-rules=5 --quiet -O -m {alg} {PWD} {dictionary} 2>/dev/null').read()
    print(dictionary)

def crack_with_dict(algorithms):
  dicts = os.listdir(DIR)
  for i in range(len(dicts)):
    crack_pwd(DIR + dicts[i], algorithms)

def main():
  get_args()
  crack_with_dict(get_algorithms())

if __name__ == "__main__":
  main()