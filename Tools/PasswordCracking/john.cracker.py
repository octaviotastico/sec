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

  print(DIR)

  if '-p' in args:
    PWD = args[ args.index('-p') + 1 ]
  if '--pwd' in args:
    PWD = args[ args.index('--pwd') + 1 ]

def crack_pwd(dictionary):
    os.popen(f'/usr/sbin/john --format=raw-md5 --wordlist={dictionary} {PWD} 2>/dev/null')

def crack_with_dict():
  dicts = os.listdir(DIR)
  for i in range(len(dicts)):
    crack_pwd(DIR + dicts[i])

def main():
  get_args()
  crack_with_dict()

if __name__ == "__main__":
  main()