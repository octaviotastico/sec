# Ejercicio 1

Contar que lo abrimos con cutter y leimos el codigo decompilado (mencionar archivo `test.c`)

...

Basicamente el programa genera una seguidilla de numeros randoms, les toma modulo 256, y va haciendo XOR sobre los caracteres del string.

Es importante aclarar que antes de generar los randoms, se setea una semilla. Dada una semilla, los numeros randoms generados son totalmente predecibles.

Para ver que string genero como resultado `d740a5dc607f78fbffe520efc7caebd2137940ddb26c30c2fd37ed743b77038d326a9c7e7e80`, debemos reversear el codigo en C. El algoritmo en reverso es sencillo ya que solo se utilizan XOR y numeros aleatorios "predecibles". El unico problema es que no conocemos la seed.

Cada vez que corremos el programa, obtenemos resultados distintos, asi que claramente esta seed cambia. Corriendolo reiteradas veces con cutter, note que la seed siempre terminaba con `0x66c`. Podria salir mal, pero me confie en que esto se iba a cumplir siempre.

Con esto en mente, bruteforceamos la seed (solo los 20 bytes mas significativos) chequeando que el string obtenido tenga el mismo MD5 que nos dan. El espacio de busqueda es 2^20. Y en cada elemento del espacio solo debemos aplicar la transformacion para cada letra, y MD5. Como estas cosas son poco pesadas y por suerte el programa nos devuelve: 

```bash
└──╼ $ gcc crack_pipe.c -o ej -lssl -lcrypto && ./ej
The flag is EKO{bullshit_PIE_over_x86}
```