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

Esto nos permite hacer XSS simplemente mandando ingresando a:
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

De igual manera, el caracter `'` solo se reemplaza cuando la flag ` ENT_QUOTES` esta seteada, asi que deberiamos buscar algo con este caracter ????

## XSS stored

### Easy version

### Medium version

### Hard version
