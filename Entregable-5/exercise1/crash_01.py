def open_and_return():
  data = b''
  address = b'\x43\x42\x41\x44'
  f = open('./afl-files/crashes/id:000001,sig:11,src:000074,op:havoc,rep:128', 'rb')
  image = f.read()
  data += image[:1106] #.replace(b'\x10', b'\x49')
  data += address
  data += image[1106:] #.replace(b'\x10', b'\x49')
  f.close()
  return data

def create_new_file(data):
  f = open(f'./afl-files/crashes/new_id:000001,sig:11,src:000074,op:havoc,rep:128', 'wb')
  f.write(data)
  f.close()

create_new_file(open_and_return())
