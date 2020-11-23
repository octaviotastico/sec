# Ejercicio 1

Este ejercicio lo intente resolver con 2 tools distintas.

## zzuf

La primera, con [zzuf](http://caca.zoy.org/wiki/zzuf), la primera tool que menciona el práctico.

Ésta tool basicamente nos permite fuzzear un archivo de entrada, y guardarlo en un archivo nuevo de salida.

Entonces, lo que hice fue crear un script en python, que cambiara entre los parametros `-r` y `-s`, que son, el porcentaje de 'daño' que se le va a hacer al archivo, y la semilla de randomness, que sería algo asi como la aleatoriedad de la ubicación de los cambios que se van a hacer al archivo, y que caracteres nuevos va a escribir en su lugar.

Gracias a este script, pude descubrir algunas imágenes de input que rompian el programa, aunque casi siempre, la mayoria no lo rompía, sino que lo dejaba colgado.

Todos los outputs de este script estan en zzuf-files, y tienen el nombre 'crash-{r}-{s}' o 'hang-{r}-{s}', dependiendo de si ese archivo crashea o deja colgado al parser. r y s, son los valores que se les da a los argumentos -r y -s.

El problema de este script, es que era algo lento, y ninguno de los outputs modificaban el EIP.

## afl

Así que decidi probar la otra tool que está en el practico, [afl](https://github.com/google/AFL), una tool bastante copada de google, que funcionaba más rápido que mi script jajaja

Asi que ejecuté afl por un par de horas, y descubrió 8 archivos que rompian el parser, y 4 que lo dejaban colgando.

Asi que inspeccioné esos archivos con `hexdump`, y los ejecute con `gdb`.

El archivo con id: 0, era medio useless, porque solo hacia terminar el parser con exit(-1), al igual que la mayoria de archivos creados con el sctipt de zzuf.

Los demás si fueron muy útiles. Los de id: 1, 2, 3, 4, 5, 6 y 7, terminaban con segmentation fault core dumped, así que eran importantes.

Revise los registros, con gdb, y resulta que los archivos de id: **1, 3** y **5 rompían** el **EIP**

El archivo de id: 7 me parecio interesante, porque fue el único que rompía la terminal y dumpeaba el binario del input. Así que hice un archivo llamado `modify_crash_file.py`, que modificaba este archivo de id: 7 y cambiaba gran parte del binario por A's, solo para ver si podia printear lo que quería, y asi fue, estaba la terminal llena de A's.

Pero lo importante de todo, es el archivo `crash_01.py`, con el cual, logré modificar el archivo de id: 1, de tal forma que ahora puedo cambiar el registro **EIP** para que apunde a donde yo quiera.

Deje que la address del EIP sea '**ABCD**', o sea, '**\x44\x43\x42\x41**' :D