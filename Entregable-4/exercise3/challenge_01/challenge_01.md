# Challenge 01

En éste challenge hay que aprovecharse de la vulnerabilidad de la funcion `gets` para llegar a printear "YOU WIN!".

El problema con `gets`, es que ésta función lee hasta encontrar el caracter '0x00' (fin de línea), y gracias a ésto, se puede realizar un ataque conocido como "smash the stack".

Consiste en basicamente sobreescribir el stack para cambiar el valor de la cookie, y poder entrar al if.

Para ésto, hay que llenar los 80 caracteres de buf, y luego escribir 0x41424344 dentro de cookie.
