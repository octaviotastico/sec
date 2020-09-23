import requests
from bs4 import BeautifulSoup
import json

seed = 'http://paste.ubuntu.com/p/HnGHwGk4rQ/'

name, content, graph = {}, {}, {}

name[seed] = 0

def dfs(url):
    print(f"I'm on {url}")

    if(name[url] not in graph):
        graph[name[url]] = []

    try:
        resp = requests.get(url)
        if(resp.status_code == 404): return
    except:
        return # Not a valid url?

    # Get the paste and format it
    soup = BeautifulSoup(resp.content, 'html.parser')
    paste = soup.find_all('pre')[1]
    urls = list(map(lambda x: x.strip(), paste.text.split('\n')))[:-1]

    content[url] = urls # Save content

    for n_url in urls:
        if(n_url not in name): # Prevent cycles
            name[n_url] = len(name)
            graph[name[url]].append(name[n_url])
            dfs(n_url)

dfs(seed)

with open('output.txt', 'w+') as f:
    f.write(json.dumps(content, indent=2))


# La flag es EKO{pastepastepaste...paste...sux} despues de hacer doble base64 sobre una url obtenida