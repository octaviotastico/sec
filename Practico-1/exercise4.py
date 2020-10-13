import binascii

def is_valid(s):
    # Assuming it's a flag
    opened = [i for i, x in enumerate(s) if x == "{"]
    closed = [i for i, x in enumerate(s) if x == "}"]
    return all(32 <= ord(c) <= 126 for c in s) and len(opened) == 1 and len(closed) == 1 and opened[0] < closed[0]

def do_otp(message, key):
    k = "".join([key[i % len(key)] for i in range(len(message))]) # Complete the key
    x = int(message, 16) ^ int(k, 16)
    return '%x' % x

msg = "0a001b1c16737b031d1601170616011700731c1608061d620b120b"

results = []

for i in range(0, 2**16):
    decoded = do_otp(msg, format(i, '06x'))
    try:
        decoded = binascii.unhexlify(decoded) # Could fail
        print(decoded)
        # if(is_valid(decoded)):
            # print(decoded)
    except Exception as ex:
        print(str(ex))
        pass

print('\n'.join(results))