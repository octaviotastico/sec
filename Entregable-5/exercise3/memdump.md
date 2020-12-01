# Memdump analysis en Linux

## **LiME**
[LiME](https://github.com/504ensicsLabs/LiME) (Linux Memory Extractor) es una tool que nos permite realizar una snapshot de la memoria volátil de un dispositivo que corra un sistema operativo basado en Linux, tal como Ubuntu, Debian, Manjaro, o incluso Android...

Esta tool además permite hacer un dumpeo de memoria directamente al filesystem (o sea, al mismo dispositivo), o mandarlo a travez de internet a otro dispositivo, generalmente la estación de trabajo forense.

## **Linux Memory Grabber**
[LMG](https://github.com/halpomeranz/lmg) es una tool que nos permite crear perfiles de memoria desde un pen-drive, usando LiME, sin siquiera instalarlo.

## **fmem**
[fmem](https://github.com/NateBrune/fmem) es un módulo de kernel que crea un dispositivo en /dev/fmem, similar a /dev/mem, pero sin las limitaciónes que tiene normalmente /dev/mem, el cual tien un rango de addresses restringido. Por lo tanto /dev/fmem tiene acceso completo a la memoria física del sistema.

Entonces, usando comandos como dd, podemos copiar toda la memoria del dispositivo a analizar.
