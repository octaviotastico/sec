from subprocess import Popen as call, PIPE as pipe, check_output, STDOUT
from numpy import arange

def main():
  for randomness in arange(0.01, 1.01, 0.01):
    for seed in range(1000000):
      # Create a new file
      proc = call([ f'cat ./parser-bmp/mono.bmp | zzuf -r {randomness} -s {seed} > ./zzuf-files/{randomness}-{seed}.bmp' ], stdin=pipe, stdout=pipe, shell=True)
      input, error = proc.communicate()
      print(input)

      # Test the new file
      proc = call([ f'./parser-bmp/parse ./zzuf-files/{randomness}-{seed}.bmp' ], stdin=pipe, stdout=pipe, shell=True)
      input, error = proc.communicate()
      print(input)
      print(error)

      # If file didn't break the program, delete it
      if b'File parsed successfully!' in input:
        call(f'rm ./zzuf-files/{randomness}-{seed}.bmp', stdin=pipe, stdout=pipe, shell=True)
        continue

      # If the file made the parse hang, just rename it
      try:
        proc.wait(timeout=1)
      except:
        call(f'mv ./zzuf-files/{randomness}-{seed}.bmp ./zzuf-files/hang-{randomness}-{seed}.bmp', stdin=pipe, stdout=pipe, shell=True)
        continue

      # The file didn't get the parse hanging, and din't parsed succesfuly, so it break the parse
      if b'File parsed successfully!' not in input:
        call(f'mv ./zzuf-files/{randomness}-{seed}.bmp ./zzuf-files/crash-{randomness}-{seed}.bmp', stdin=pipe, stdout=pipe, shell=True)
        continue

main()
