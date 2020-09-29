# Ejercicio 3

Cuando ingresamos a la pagina, vemos que nos muestra varias imagenes, pero hay una en particular que no se muestra

Si inspeccionamos esta imagen, vemos que su `src` es `meme?id=5`

Yendo a esa url, vemos que nos salta un error 500.

Si cambiamos el id por alguno de los valores `1, 2, 3, 4` vemos que se muestran las imagenes del HOME en 'formato texto'

En ese momento corri `sqlmap` sobre la url para ver si el parametro `id` era vulnerable, y me salio que lo era a time-based injection

Gracias a la herramienta, automaticamente pude averiguar el nombre de la base de datos, nombre de las tablas, etc.

```
sqlmap -u "http://143.0.100.198:5010/meme?id=1" --dbs
sqlmap -u "http://143.0.100.198:5010/meme?id=1" -D memes_db --tables
sqlmap -u "http://143.0.100.198:5010/meme?id=1" -D memes_db -T tb_name --dump
```

Ahora entendia porque no podia ver la imagen con `id=5`, justamente, su filename no tenia sentido

# Meter la tabla aca

Ahi tuve otra idea mas. Me imagine que lo que hacia la url, era obtener el path del archivo a mostrar. Luego, yo podria supuestamente cargar cualquier archivo si proporcionaba bien el path.

Esto no me funciono con archivos comunes que quise encontrar, y entonces volvi a usar `sqlmap` para leer algunos archivos del sistema

Por ejemplo, lei el /etc/passwd y /etc/hosts de la maquina

```
sqlmap -u "http://143.0.100.198:5010/meme?id=1" --file-read=/etc/passwd
sqlmap -u "http://143.0.100.198:5010/meme?id=1" --file-read=/etc/hosts
```

# Meter los archivos

No obstante, en este momento ya estaba perdido, y solo pude continuar gracias a la pista proporcionada.

Como sabia que la url pedia un archivo, simplemente hice un script para probar todas las palabras del archivo proporcionado en el zip.

De esta manera, encontre que podia acceder a `http://143.0.100.198:5010/meme?id=0 UNION SELECT 'main.py'`

Justamente en ese archivo, se encontraba la flag `SEGURIDAD-OFENSIVA-FAMAF`
