import os, sys, threading

MODE = 'ALL'
DIR = './dicts/'
THREADS = 4
PWDS = ''

args = sys.argv
def get_args():
  if '-d' in args:
    DIR = args[ args.index('-d') + 1 ]
  if '--dir' in args:
    DIR = args[ args.index('--dir') + 1 ]
  if '-m' in args:
    MODE = args[ args.index('--m') + 1 ]
  if '--mode' in args:
    MODE = args[ args.index('--mode') + 1 ]
  if '-t' in args:
    THREADS = args[ args.index('-t') + 1 ]
  if '--threads' in args:
    THREADS = args[ args.index('--threads') + 1 ]
  if '-p' in args:
    PWDS = args[ args.index('-p') + 1 ]
  if '--pwds' in args:
    PWDS = args[ args.index('--pwds') + 1 ]

def get_args_values():
  if MODE == 'ALL':
    modes = os.popen('hashcat -h | grep MD4 -A212 | cut -d"|" -f1 | sort | uniq').read()
    modes = modes.replace(' ', '')[:-1].split('\n')
  else:
    modes = os.popen(f'hashcat -h | grep {MODE} -m1 | cut -d'|' -f1').read()
    modes = modes.replace(' ', '').replace('\n', '')

def crack_pwd(DICT):
  if type(MODE) == list:
    for M in MODE:
      os.system(f'hashcat --generate-rules=5 --quiet -O -m {M} {PWDS} {DICT} 2>/dev/null')
  else:
    os.system(f'hashcat --generate-rules=5 --quiet -O -m {MODE} {PWDS} {DICT} 2>/dev/null')

def crack_with_dict(start):
  i = start
  dicts = os.listdir(DIR)
  while True:
    DICT = dicts[i]
    crack_pwd(DICT)
    i += THREADS
    if i >= len(dicts):
      return

def main():
  threads = []
  get_args_values()
  for THREAD in range(THREADS):
    t = threading.Thread(target=crack_with_dict, args=(THREAD))
    threads.append(t)
    t.start()

if __name__ == "__main__":
  main()