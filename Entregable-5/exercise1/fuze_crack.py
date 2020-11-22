from subprocess import Popen as call, PIPE as pipe
from numpy import arange

def main():
  for randomness in arange(0.01, 1.01, 0.01):
    for seed in range(1000000):
      # Create a new file
      proc = call([ f'cat ./parser-bmp/mono.bmp | zzuf -r {randomness} -s {seed} > ./files/{randomness}-{seed}.bmp' ], stdin=pipe, stdout=pipe, shell=True)
      input, error = proc.communicate()
      print(input)

      # Test the new file
      proc = call([ f'./parser-bmp/parse ./files/{randomness}-{seed}.bmp' ], stdin=pipe, stdout=pipe, shell=True)
      input, error = proc.communicate()
      print(input)
      print(error)

      # If file didn't break the program, delete it
      # if b'File parsed successfully!' in input:
        # call(f'rm ./files/{randomness}-{seed}.bmp', stdin=pipe, stdout=pipe, shell=True)

main()
