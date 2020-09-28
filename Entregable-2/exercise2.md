# Ejercicio 2

Cuando ingresamos al sitio, nos encontramos con una imagen y un simple texto:
> The site is not yet complete, Come Back Later! 

Pero una vez que recargamos la pagina, esta vez vemos:
```
SyntaxError: Unexpected token F in JSON at position 79
    at JSON.parse (<anonymous>)
    at Object.exports.unserialize (/under/node_modules/node-serialize/lib/serialize.js:62:16)
    at /under/server.js:12:29
    at Layer.handle [as handle_request] (/under/node_modules/express/lib/router/layer.js:95:5)
    at next (/under/node_modules/express/lib/router/route.js:137:13)
    at Route.dispatch (/under/node_modules/express/lib/router/route.js:112:3)
    at Layer.handle [as handle_request] (/under/node_modules/express/lib/router/layer.js:95:5)
    at /under/node_modules/express/lib/router/index.js:281:22
    at Function.process_params (/under/node_modules/express/lib/router/index.js:335:12)
    at next (/under/node_modules/express/lib/router/index.js:275:10)
```

Pareciera ser que a la pagina le estamos mandando algo la segunda vez que entramos... Quizas una cookie?

Interceptando la request con un proxy, podemos leer
```
Cookie: profile=eyJ1c2VybmFtZSI6IkFkbWluIiwiY3NyZnRva2VuIjoidTMydDRvM3RiM2dnNDMxZnMzNGdnZGdjaGp3bnphMGw9IiwiRXhwaXJlcz0iOkZyaWRheSwgMTMgT2N0IDIwMTggMDA6MDA6MDAgR01UIn0%3D
```

El prefijo 'ey' me suena de '{' en base64, y ademas vemos la presencia de un %3D que pareciera indicar que esta url-encoded.

Asi que pasandolo por url-decode + base64 en cyber chef obtenemos:
```
{"username":"Admin","csrftoken":"u32t4o3tb3gg431fs34ggdgchjwnza0l=","Expires=":Friday, 13 Oct 2018 00:00:00 GMT"}
```

Ahora entendemos el stack trace. Justamente este JSON esta mal hecho, deberia decir `"Expires=": "Friday ..."`, pero dice `"Expires=" : Friday ... "` (falta una comilla)

Agregando la comilla y encodeando en orden inverso para mandarselo por el proxy, la pagina ahora nos saluda:
> Hello Admin

Esto es peligroso, ya que esta tomando nuestro `user` como el valor de la cookie, la cual esta solo encodeada en b64. Esto no es peligroso en esta pagina, pero si hiciese algun tipo de consulta/cambios en el sistema dado el user, seria peligroso.

Ademas, tampoco se chequea el campo `Expires=` del token, ya que lo deje con la misma fecha (2018).