# Ejercicio 5

En todos los ejercicios suponga que las BWA estan levantada en 192.168.1.20

## XSS reflected

### Easy version

Mirando el codigo, vemos que no hay ningun tipo de sanitizer

```
 <?php

if(!array_key_exists ("name", $_GET) || $_GET['name'] == NULL || $_GET['name'] == ''){

 $isempty = true;

} else {
        
 echo '<pre>';
 echo 'Hello ' . $_GET['name'];
 echo '</pre>';
    
}

?> 
```

Esto nos permite hacer XSS simplemente ingresando a:
`http://192.168.1.20/dvwa/vulnerabilities/xss_r/?name=<script>alert(1)</script>`

### Medium version

El nuevo codigo, evita que mandemos el tag `<script>`

```
 <?php

if(!array_key_exists ("name", $_GET) || $_GET['name'] == NULL || $_GET['name'] == ''){

 $isempty = true;

} else {

 echo '<pre>';
 echo 'Hello ' . str_replace('<script>', '', $_GET['name']);
 echo '</pre>'; 

}

?> 
```

Pero de nuevo, podemos mandar tranquilamente el tag con un espacio en el medio `http://192.168.1.20/dvwa/vulnerabilities/xss_r/?name=<script >alert(1)</script>`

### Hard version

El nuevo codigo pareciera estar escapando los caracteres especiales de HTML
```
 <?php
    
if(!array_key_exists ("name", $_GET) || $_GET['name'] == NULL || $_GET['name'] == ''){
    
 $isempty = true;
        
} else {
    
 echo '<pre>';
 echo 'Hello ' . htmlspecialchars($_GET['name']);
 echo '</pre>';
        
}

?> 
```

Leyendo la documentacion, vemos que la funcion convierte:

| Symbol   |      Replacement      |
|:----------:|:-------------:|
| & | \&amp; |
| " | \&quot; |
| ' | \&#039; or \&apos; |
| < | \&lt; |
| > | \&gt; |

De igual manera, el caracter `'` solo se reemplaza cuando la flag ` ENT_QUOTES` esta seteada, asi que deberiamos buscar algo con este caracter

Me parece que esto no se puede romper con HTML, pero seria vulnerable a SQL injection en todo caso, ya que podemos usar `'` y `\` (ya que no hay un `strip_slashes`)

## XSS stored

### Easy version

Mirando el codigo, vemos que se hace un `INSERT` en una tabla de la DB. Se hace el escaping correspondiente para evitar sql-injections.

```
 <?php

if(isset($_POST['btnSign']))
{

   $message = trim($_POST['mtxMessage']);
   $name    = trim($_POST['txtName']);
   
   // Sanitize message input
   $message = stripslashes($message);
   $message = mysql_real_escape_string($message);
   
   // Sanitize name input
   $name = mysql_real_escape_string($name);
  
   $query = "INSERT INTO guestbook (comment,name) VALUES ('$message','$name');";
   
   $result = mysql_query($query) or die('<pre>' . mysql_error() . '</pre>' );
   
}

?> 
```

De igual manera, el string `<script>X</script>` deberian sobrevivir sin problemas, y guardarse en la DB. Entonces, cada vez que alguien carge una pagina que muestre resultados, se ejecutara el script X

Mandamos entonces: 
> name: asd

> message: \<script>alert(1)\</script>

### Medium version

La diferencia con el codigo anterior es que ahora en el mensaje se aplica un buen escaping (`strip_tags` + `htmlespecialchars`), pero porque no al nombre?

```
 <?php

if(isset($_POST['btnSign']))
{

   $message = trim($_POST['mtxMessage']);
   $name    = trim($_POST['txtName']);
   
   // Sanitize message input
   $message = trim(strip_tags(addslashes($message)));
   $message = mysql_real_escape_string($message);
   $message = htmlspecialchars($message);
    
   // Sanitize name input
   $name = str_replace('<script>', '', $name);
   $name = mysql_real_escape_string($name);
  
   $query = "INSERT INTO guestbook (comment,name) VALUES ('$message','$name');";
   
   $result = mysql_query($query) or die('<pre>' . mysql_error() . '</pre>' );
   
}

?> 
```

Desde el front-end, podemos comprobar que no nos deja escribir algo tan largo... Se ve que confian en eso. Lamentablemente tenemos el codigo, y sabemos que es una request POST a la misma url. Solo nos queda ver como superamos la linea `$name = str_replace('<script>', '', $name);`

Si le ponemos un espacio antes del `>` (como antes), tiene el mismo efecto el tag, por lo tanto, usando un proxy, reemplazamos:
> name = \<script >alert(1); \</script>

### Hard version

No pareciera ser rompible, pero pensando aun