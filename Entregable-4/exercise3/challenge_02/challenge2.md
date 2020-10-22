# Challenge 02

Al igual que el challenge 01, éste challenge consiste en aprovecharse de la vulnerabilidad de la funcion `gets` para llegar a printear "YOU WIN!", sobreescribiendo la cookie.

La diferencia que tiene este ejercicio con el anterior, es que el valor de cookie tiene que ser non ASCII. En el challenge 01, con escribir 'A'*80 + 'DCBA' bastaba, pero en este, necesitamos mandar bytes, y no caracteres.

Para ésto, hay que llenar los 70 caracteres de buf, y luego escribir 0x01020304 dentro de cookie.
