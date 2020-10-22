# Challenge 03

Al igual que el challenge 01 y 02, éste challenge consiste en aprovecharse de la vulnerabilidad de la funcion `gets` para llegar a printear "YOU WIN!", pero ésta vez, no sale sobreescribiendo la cookie.

La dificultad de este ejercicio consiste en que ya no podemos usar la vulnerabilidad de gets para sobreescribir cookie y entrar facilmente dentro del if, ya que el valor de cookie debe ser: "0x000D0A00", eso implica escribir: **"A" * 60 + "0x00" "0x0D" "0x0A" "0x00"**.

Pero como habiamos dicho antes, gets solo lee hasta encontrarse un 0x00, y es justamente lo que encuentra luego de las primeras 60 A's, asi que se nos tiene que ocurrir algo mas inteligente, ya que no podemos nunca poner ese valor dentro de la cookie.

Lo que podemos hacer es lo siguiente: Existe un registro llamado `eip`, que controla el flujo de ejecución de un programa.

Si logramos pisarlo y sobreescribir su valor, estaríamos cabiando el valor de retorno del main, y entonces ganamos! Ya que podemos retornar dentro del if, hacia el printf("YOU WIN!").

Entonces, como dijimos antes, el objetivo ya no es modificar el valor de cookie sino que aprovecharnos de gets, para sobreescribir el registro `eip`, y llegar a partes del programa que nunca seríamos capaces de llegar si no fuera de otra forma.

Para ésto, hay que llenar los 60 caracteres de buf, luego llenar la cookie, que es un **int**, i.e 4 bytes, y finalmente llenar el registro **ebp**, tambien de 4 bytes.

Luego de esos 68 bytes, hay que poner la direccion de retorno que querramos, en nuestro caso, la del printf, pero todavia no la sabemos...

Para conocerla, podemos hacer:

```
>>> objdump -M intel -S obj

08048438 <main>:
8048438:	55                   	push   ebp
8048439:	89 e5                	mov    ebp,esp
804843b:	83 ec 40             	sub    esp,0x40
804843e:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [ebp-0x4],0x0
8048445:	8d 45 c0             	lea    eax,[ebp-0x40]
8048448:	50                   	push   eax
8048449:	e8 d2 fe ff ff       	call   8048320 <gets@plt>
804844e:	83 c4 04             	add    esp,0x4
8048451:	81 7d fc 00 0a 0d 00 	cmp    DWORD PTR [ebp-0x4],0xd0a00
8048458:	75 0d                	jne    8048467 <main+0x2f>
804845a:	68 44 85 04 08       	push   0x8048544
804845f:	e8 cc fe ff ff       	call   8048330 <puts@plt>
8048464:	83 c4 04             	add    esp,0x4
8048467:	b8 00 00 00 00       	mov    eax,0x0
804846c:	c9                   	leave
804846d:	c3                   	ret
804846e:	90                   	nop
804846f:	90                   	nop
```

Y vemos que esa dirección es: `0x0804845a`