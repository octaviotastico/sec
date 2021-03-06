# Ejercicio 1

**Url objetivo**: https://www.famaf.unc.edu.ar/

Con un simple `ping www.famaf.unc.edu.ar`, podemos ver que la **IP** es: 200.16.17.123 (tipo A)

Y el **host** es: ratri.famaf.unc.edu.ar (PTR)

Ahora que tenemos la IP de famaf, podemos usar nmap, y revisar que **puertos** estan abiertos:<br/>

22 - TCP - SSH - Versión OpenSSH 7.4p1 Debian 10+ deb9u7 (protocol 2.0)<br/>
80 - TCP - HTTP - Versión ngix 1.10.3<br/>
443 - TCP - SSL/HTTP - Versión ngix 1.10.3<br/>

Además, obtenemos informacion adicional, como el **Sistema operativo**: Linux 3.X (3.16)

Estos datos tambien se pueden obtener con [shodan.io](https://www.shodan.io/host/200.16.17.123).
Hay ademas una lista completa de IPs en el archivo `ip-list.md`.

Incluyendo **otros DNS relacionados**:<br/>
memos.famaf.unc.edu.ar (200.16.17.123)<br/>
grc.famaf.unc.edu.ar (200.16.17.123)<br/>
sysfamaf.famaf.unc.edu.ar (200.16.17.123)<br/>
tickets.famaf.unc.edu.ar (200.16.17.123)<br/>
agni.famaf.unc.edu.ar (200.16.17.123)<br/>
webmet.ohmc.com.ar - Redirecciona a grc.famaf.unc.edu.ar<br/>
shannon.famaf.unc.edu.ar (200.16.17.249)<br/>
ra.famaf.unc.edu.ar (200.16.17.49) - Redirecciona a famaf.unc.edu.ar<br/>

En el archivo `host-list.md` esta la lista completa con todos los host que pude encontrar.

Buscando **emails**, el patrón con el que se crean generalmente es: `{nombre}{apellido[0]}@famaf.unc.edu.ar`.

Algunos de ellos son:<br/>
ingreso@famaf.unc.edu.ar<br/>
posgrado@famaf.unc.edu.ar<br/>
biblio@famaf.unc.edu.ar<br/>
revista@famaf.unc.edu.ar<br/>
revm@famaf.unc.edu.ar<br/>
nicolasw@famaf.unc.edu.ar<br/>
bc@famaf.unc.edu.ar</br>
benotti@famaf.unc.edu.ar</br>
Los demás estan listados en el archivo `mail-list.md`.

Para ésta búsqueda se pueden usar páginas como [hunter.io](https://hunter.io/try/search/famaf.unc.edu.ar), o herramientas como [theHarvester](https://github.com/laramies/theHarvester).
