# Script made to open crash files, and modify them.

def open_and_return(filename):
  data = b''
  f = open(f'./afl-files/crashes/{filename}', 'rb')
  # data += f.read().replace(b'\xc9', b'\x41')
  data += f.read().replace(b'\x10', b'\x41', 898)
  f.close()
  return data

def create_new_file(data, filename):
  f = open(f'./afl-files/crashes/new_{filename}', 'wb')
  f.write(data)
  f.close()

import sys
filename = sys.argv[1]
create_new_file(open_and_return(filename), filename)
