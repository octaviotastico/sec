# Ejercicio 1

Para enfrentar este ejercicio, lo primero que hicimos fue analizar el binario rápido, con strings y hexdump. No obtuvimos nada en especial, no encontramos ninguna funcion rara llamada `flag` o `vuln` como suelen tener muchos CTF. Así que procedimos a usar tools mas copadas, como Cutter, que nos permite analizar el assembly y decompilarlo a código C.

Ahí pudimos entender un poco más de que se trataba el programa. Reconstruimos la funcion `main` para poder hacer pruebas y ejecutarla en el archivo `test.c`.

Básicamente lo que hace, es generar una seguidilla de numeros randoms, les toma módulo 256, y va haciendo XOR sobre los caracteres del string.

Es importante aclarar que antes de generar los randoms, se setea una semilla. Dada una semilla, los numeros randoms generados son totalmente predecibles.

Para ver qué string generó "`d740a5dc607f78fbffe520efc7caebd2137940ddb26c30c2fd37ed743b77038d326a9c7e7e80`" como resultado, debemos reversear el código en C. El algoritmo en reverso es sencillo ya que solo se utilizan XOR y numeros aleatorios "predecibles". El único problema es que no conocemos la seed.

Cada vez que corremos el programa, obtenemos resultados distintos, asi que claramente esta seed cambia. Pero lo interesante de este ejercicio, es ver **como** cambia.

Al principio creíamos que la seed tenía algo que ver con la dirección del main, y al parecer, estabamos en lo correcto, porque corriendolo reiteradas veces con cutter, notamos que la seed siempre terminaba con `0x66c`, al igual que la funcion main.

Con esto en mente, bruteforceamos la seed (solo los 20 bytes mas significativos, es decir, 0x66c + 0x1000 * x), y chequeamos que el string obtenido tenga el mismo MD5 que el que nos dan. El espacio de búsqueda es 2^20. Y en cada elemento del espacio solo debemos aplicar la transformación para cada letra, y MD5. Como éstas cosas son poco pesadas, el programa termina bien, y pudimos obtener la seed:

```bash
└──╼ $ gcc crack_pipe.c -o ej -lssl -lcrypto && ./ej
The flag is EKO{bullshit_PIE_over_x86}
```