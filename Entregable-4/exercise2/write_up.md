# Ejercicio 2

## R1

```
└──╼ $file r1
r1: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.15, BuildID[sha1]=43af309d3735b17cef57f70cb997eebafd17ebf2, not stripped
```

Si abrimos este archivo con `cutter`, podemos analizar el assembler que contiene

Este es el codigo del procedimiento `main`

```
undefined4 main(void)
{
    char cVar1;
    undefined4 uVar2;
    uint32_t uVar3;
    char *pcVar4;
    int32_t in_GS_OFFSET;
    uint8_t uVar5;
    uint32_t uStack48;
    uint8_t auStack40 [20];
    int32_t iStack20;
    int32_t var_8h;
    
    uVar5 = 0;
    iStack20 = *(int32_t *)(in_GS_OFFSET + 0x14);
    printf("Enter password: ");
    __isoc99_scanf(0x8048681, auStack40);
    uStack48 = 0;
    do {
        uVar3 = 0xffffffff;
        pcVar4 = "5tr0vZBrX:xTyR-P!";
        do {
            if (uVar3 == 0) break;
            uVar3 = uVar3 - 1;
            cVar1 = *pcVar4;
            pcVar4 = pcVar4 + (uint32_t)uVar5 * -2 + 1;
        } while (cVar1 != '\0');
        if (~uVar3 - 1 <= uStack48) {
            puts("\nSuccess!! Too easy.");
            uVar2 = 0;
            goto code_r0x0804857a;
        }
        if (auStack40[uStack48] != (uint8_t)((uint8_t)uStack48 ^ "5tr0vZBrX:xTyR-P!"[uStack48])) {
            puts("Wrong!");
            uVar2 = 1;
code_r0x0804857a:
            if (iStack20 != *(int32_t *)(in_GS_OFFSET + 0x14)) {
                uVar2 = __stack_chk_fail();
            }
            return uVar2;
        }
        uStack48 = uStack48 + 1;
    } while( true );
}
```

Analicemolos por partes:

```
uStack48 = 0;
...
uVar3 = 0xffffffff; // -1
pcVar4 = "5tr0vZBrX:xTyR-P!";
do {
if (uVar3 == 0) break;
    uVar3 = uVar3 - 1;
    cVar1 = *pcVar4;
    pcVar4 = pcVar4 + (uint32_t)uVar5 * -2 + 1;
} while (cVar1 != '\0');
if (~uVar3 - 1 <= uStack48) {
    puts("\nSuccess!! Too easy.");
    uVar2 = 0;
    goto code_r0x0804857a;
}
...
```

Esta parte se encarga de recorrer linealmente el string `5tr0vZBrX:xTyR-P!` hasta encontrar el caracter `\0`. Mientras lo va haciendo, le resta uno a la variable `uVar3`

Al finalizar ese `do {...} while()`, `uVar3` valdra exactamente -19. Entonces `~uVar3 - 1` valdra 17. De alguna forma `uStack48` tenemos que hacer que valga 17

```
if (auStack40[uStack48] != (uint8_t)((uint8_t)uStack48 ^ "5tr0vZBrX:xTyR-P!"[uStack48])) {
    puts("Wrong!");
    uVar2 = 1;
code_r0x0804857a:
    if (iStack20 != *(int32_t *)(in_GS_OFFSET + 0x14)) {
        uVar2 = __stack_chk_fail();
    }
    return uVar2;
}
uStack48 = uStack48 + 1;
```

Inmediatamente despues, tenemos este codigo. Lo que hace este codigo es chequear si `auStack40[uStack48] != uStack[48] ^ "5tr0vZBrX:xTyR-P!"[uStack48]`. En palabras mas sencillas `string_del_input[i] != i ^ magic_string[i]`

En caso de que sean iguales, hacemos `uStack48++`, y volvemos a iterar. Es decir, podemos hacer que `uStack48` llege a 17 consiguiendo el string `i ^ magic_string[i]`

Lo hacemos con un sencillo script en python
```
password = "5tr0vZBrX:xTyR-P!"

real = ""

for i in range(len(password)):
    real += chr(ord(password[i]) ^ i)

print(real) # 5up3r_DuP3r_u_#_1
```

y obtenemos
```
└──╼ $./r1
Enter password: 5up3r_DuP3r_u_#_1

Success!! Too easy.
```

## R2

En este caso observamos que el archivo esta `stripped`

```
└──╼ $file r2
r2: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.15, BuildID[sha1]=b3278fe6368cde1f51b1a491b06b16b162c2adc3, stripped
```

Es decir, no tendra datos "extra" que se pueden utilizar para debuggear mas facilmente. Como consecuencia, el decompiler de `cutter` no nos da algo que nos sirve, hora de leer el assembler!

La ejecucion de este archivo es parecida al del `r1`, asi que tiene sentido adivinar que sera algo parecido (para cada letra de un `magic_string`, hacer algo).

```
0x080484e9      push ebp
0x080484ea      mov ebp, esp
0x080484ec      push edi
0x080484ed      push ebx
0x080484ee      and esp, 0xfffffff0
0x080484f1      sub esp, 0x40
0x080484f4      mov eax, dword gs:[0x14]
0x080484fa      mov dword [var_3ch], eax
0x080484fe      xor eax, eax
0x08048500      push eax
0x08048501      xor eax, eax
0x08048503      je 0x8048508
0x08048505      add esp, 4
0x08048508      pop eax
0x08048509      mov dword [func], 0x80484e4 ; void *func
0x08048511      mov dword [esp], 5 ; int sig
0x08048518      call signal        ; sym.imp.signal ; void signal(int sig, void *func)
0x0804851d      mov dword [var_20h], 0
0x08048525      mov eax, str.Enter_password: ; 0x80486f0
0x0804852a      mov dword [esp], eax ; const char *format
0x0804852d      call printf        ; sym.imp.printf ; int printf(const char *format)
0x08048532      int3
0x08048533      mov eax, 0x8048701
0x08048538      lea edx, [esp + 0x28]
0x0804853c      mov dword [esp + 4], edx
0x08048540      mov dword [esp], eax
0x08048543      call __isoc99_scanf ; sym.imp.__isoc99_scanf ; int scanf(const char *format)
0x08048548      mov dword [esp + 0x20], 0
0x08048550      jmp 0x80485b8
```
El programa comienza haciendo un printf (el "Enter password:"), para luego hacer un scanf, hasta aqui vamos igual. Notese que nuestro string queda guardado en [esp + 0x28]

Luego hacemos jmp a la direccion `0x80485b8`

```
0x080485b8      mov ebx, dword [esp + 0x20]
0x080485bc      mov eax, str.kw6PZq3Zd;ekR[_1 ; 0x804a024
0x080485c1      mov dword [esp + 0x1c], 0xffffffff ; -1
0x080485c9      mov edx, eax
0x080485cb      mov eax, 0
0x080485d0      mov ecx, dword [esp + 0x1c]
0x080485d4      mov edi, edx
0x080485d6      repne scasb al, byte es:[edi]
0x080485d8      mov eax, ecx
0x080485da      not eax
0x080485dc      sub eax, 1
0x080485df      cmp ebx, eax
0x080485e1      jb 0x8048552
0x080485e7      int3
0x080485e8      mov dword [esp], str.Success___Too_easy. ; 0x804870b
0x080485ef      call puts          ; sym.imp.puts ; int puts(const char *s)
0x080485f4      mov eax, 0
0x080485f9      mov edx, dword [esp + 0x3c]
0x080485fd      xor edx, dword gs:[0x14]
0x08048604      je 0x804860b
0x08048606      call __stack_chk_fail ; sym.imp.__stack_chk_fail ; void __stack_chk_fail(void)
0x0804860b      lea esp, [ebp - 8]
0x0804860e      pop ebx
0x0804860f      pop edi
0x08048610      pop ebp
0x08048611      ret
```

No lo mostre antes en `r1`, pero este codigo es muy similar. Hay un `magic_string = kw6PZq3Zd;ekR[_1` que queda guardado en `edx`, ponemos `[esp + 0x1c] = 0xffffffff` para despues hacer `ecx = [esp + 0x1c]`, y tambien tenemos un `eax = 0`. Todo esto tiene sentido cuando vemos la instruccion `repne scasb al, byte es:[edi]`, la cual significa:

> Repeat until al != (0x0) or until ecx == 0, reading byte by bytes starting from edi

Es decir, leemos el `magic_string`, el cual tiene 16 caracteres, y nos queda justamente ese 16 en `eax` una vez que hacemos `eax = ~ecx - 1`

De nuevo, nos encontramos el `cmp ebx, eax`, y recordemos que despues del scanf, estaba la instruccion `mov dword [esp + 0x20], 0`, y al principio de este codigo tenemos `mov ebx, dword [esp + 0x20]`. Conclusion, literalmente tenemos el mismo `do { ... } while(cantidad_de_letras <= posicion actual)`. Hay que buscar la forma de mover ese "posicion_actual", que es la direccion de memoria `[esp + 0x20]`.

Bueno, claramente la primera vez que pasamos por esto codigo, saltamos a la direccion `0x8048552`, y lo haremos justamente 16 veces.

```
0x08048552      int3
0x08048553      mov eax, dword [esp + 0x20]
0x08048557      add eax, str.kw6PZq3Zd;ekR[_1 ; 0x804a024
0x0804855c      movzx ebx, byte [eax]
0x0804855f      mov eax, dword [esp + 0x20]
0x08048563      lea ecx, [eax + 1]
0x08048566      mov edx, 0x66666667 ; 'gfff'
0x0804856b      mov eax, ecx
0x0804856d      imul edx
0x0804856f      sar edx, 3
0x08048572      mov eax, ecx
0x08048574      sar eax, 0x1f
0x08048577      sub edx, eax
0x08048579      mov eax, edx
0x0804857b      shl eax, 2
0x0804857e      add eax, edx
0x08048580      shl eax, 2
0x08048583      mov edx, ecx
0x08048585      sub edx, eax
0x08048587      mov eax, edx
0x08048589      xor eax, ebx
0x0804858b      mov byte [esp + 0x27], al
0x0804858f      lea eax, [esp + 0x28]
0x08048593      add eax, dword [esp + 0x20]
0x08048597      movzx eax, byte [eax]
0x0804859a      cmp al, byte [esp + 0x27]
0x0804859e      je 0x80485b3
0x080485a0      mov dword [esp], str.Wrong ; 0x8048704
0x080485a7      call puts          ; sym.imp.puts ; int puts(const char *s)
0x080485ac      mov eax, 1
0x080485b1      jmp 0x80485f9
```

Bien, recordemos `[esp + 0x20]` intuimos que es nuestra posicion en el string, traduzcamos cada linea de este assembler.

Tambien recordemos que 0x804a024 es la direccion de nuestro `magic_string`. Cuando accedamos a tal posicion, supondremos que tenemos un arreglo `A` apuntando a esa direccion

```
mov eax, dword [esp + 0x20]                || eax = posicion
add eax, str.kw6PZq3Zd;ekR[_1 ; 0x804a024  || eax += 0x804a024
movzx ebx, byte [eax]                      || ebx = *(eax) // A[posicion]
mov eax, dword [esp + 0x20]                || eax = posicion
lea ecx, [eax + 1]                         || ecx = eax + 1
mov edx, 0x66666667 ; 'gfff'               || edx = 0x66666667
mov eax, ecx                               || eax = ecx
imul edx                                   || EDX:EAX = eax * edx // split 32-32 bits
sar edx, 3                                 || edx >>= 3
mov eax, ecx                               || eax = ecx
sar eax, 0x1f                              || eax >>= 31
sub edx, eax                               || edx -= eax
mov eax, edx                               || eax = edx
shl eax, 2                                 || eax <<= 2
add eax, edx                               || eax += edx
shl eax, 2                                 || eax <<= 2
mov edx, ecx                               || edx = ecx
sub edx, eax                               || edx -= eax
mov eax, edx                               || eax = edx
xor eax, ebx                               || eax ^= ebx
mov byte [esp + 0x27], al                  || [esp + 0x27] = 8 lower bits of eax
lea eax, [esp + 0x28]                      || eax = address de nuestro string
add eax, dword [esp + 0x20]                || eax += posicion
movzx eax, byte [eax]                      || eax = *(eax) // nuestro_string[posicion]
cmp al, byte [esp + 0x27]                  || 8 lower bits of eax == *(esp + 0x27)
je 0x80485b3
```

Uff, en resumen, agarramos el caracter i-esimo del `magic_string`, hacemos cosas magicas con `posicion + 1` + `0x66666667` + `posicion` + ese caracter i-esimo. Una vez hicimos toda esa magia, guardamos los ultimos 8 bits de eax, cargamos lo que hay en la direccion de memoria `(nuestro_string[0] + posicion)` y lo comparamos con lo que habiamos guardado antes.

Si esta comparacion anda, saltamos a `0x80485b3` y ejecutamos `add dword [esp + 0x20], 1` y posteriormente todo el codigo que hacia `16 <= posicion` se ejecuta. Asi que si, efectivamente `[esp + 0x20]` es nuestra posicion, aunque ya lo suponiamos.

Bueno genial, tenemos el codigo, tenemos el `magic_string`, veamos que le tenemos que mandar!

Sencillo copy paste de lo que escribimos, pero en python

```
A = "kw6PZq3Zd;ekR[_1"

nuestro = []

def imul(edx, eax):
    x = edx * eax
    return x>>32, x&0xffffffff

def doit(i):
    eax = ecx = i + 1
    ebx = ord(A[i])
    edx = 0x66666667

    edx, eax = imul(edx, eax)

    edx >>= 3
    eax = ecx >> 31
    edx -= eax
    eax = (edx << 2) + edx
    eax <<= 2
    edx = ecx - eax
    eax = edx
    eax ^= ebx

    important = eax & 0xff

    nuestro.append(important)

for i in range(len(A)): doit(i)

res = ""
for i in range(len(nuestro)): res += chr(nuestro[i])
print(res) # ju5T_w4Rm1ng_UP!
```

`ju5T_w4Rm1ng_UP!` tiene pinta, y obtenemos

```
└──╼ $./r2
Enter password: ju5T_w4Rm1ng_UP!

Success!! Too easy.
```

## R3

```
└──╼ $file r3 
r3: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.15, BuildID[sha1]=bec53100fab355c947ad9d9a8aa8cb27cbdb4ee9, stripped
```

De nuevo, no nos sera tan facil analizar este archivo

Si lo corremos, nos pide un `Serial`
```
└──╼ $./r3 
Serial:
```

Busquemos donde aparece esto en el assembler. Primero que nada, veamos que hace el `main`

```
100: int main (int argc, char **argv, char **envp);
; var char *var_4h @ esp+0x8
; var char *var_8h @ esp+0xc
0x08048869      push    ebp
0x0804886a      mov     ebp, esp
0x0804886c      and     esp, 0xfffffff0
0x0804886f      sub     esp, 0x10
0x08048872      push    eax
0x08048873      xor     eax, eax
0x08048875      je      0x804887a
0x08048877      add     esp, 4
0x0804887a      pop     eax
0x0804887b      mov     edx, dword [0x804a034]
0x08048881      mov     eax, dword [0x804a038]
0x08048886      cmp     edx, eax
0x08048888      jne     0x80488a9
0x0804888a      mov     eax, str.sSuccess______s ; 0x8048d5b
0x0804888f      mov     dword [var_8h], str.e_0m ; 0x8048d6a
0x08048897      mov     dword [var_4h], str.e_32m ; 0x8048d6f
0x0804889f      mov     dword [esp], eax ; const char *format
0x080488a2      call    printf     ; sym.imp.printf ; int printf(const char *format)
0x080488a7      jmp     0x80488c6
0x080488a9      mov     eax, str.sNope______s ; 0x8048d75
0x080488ae      mov     dword [var_8h], str.e_0m ; 0x8048d6a
0x080488b6      mov     dword [var_4h], str.e_31m ; 0x80489ed
0x080488be      mov     dword [esp], eax ; const char *format
0x080488c1      call    printf     ; sym.imp.printf ; int printf(const char *format)
0x080488c6      mov     eax, 0
0x080488cb      leave
0x080488cc      ret
```

Lo mas rescatable es
```
0x0804887b      mov     edx, dword [0x804a034]
0x08048881      mov     eax, dword [0x804a038]
0x08048886      cmp     edx, eax
0x08048888      jne     0x80488a9
```

Es decir, queremos controlar lo que hay en esas direcciones de memoria. Si hacemos que tengan lo mismo, nos printeara `Success` el programa en vez de `Nope`

Lo loco es que en el main no esta la logica del `scanf`. Esa logica se encuentra en `entry.init1`. Es bastante codigo, asi que adjunto el "mapa del assembler" de esta parte. Obviamente analizare las partes importantes de este.

Notese que hay 2 caminos que nos llevan al `scanf`, uno que nos pide `Serial:`, y el otro nos pide `Enter last name (5 or more letters):`...

Correrlo en `cutter`, nos devuelve:
```
######
#     #  ######  #####   #    #   ####    ####      #    #    #   ####
#     #  #       #    #  #    #  #    #  #    #     #    ##   #  #    #
#     #  #####   #####   #    #  #       #          #    # #  #  #
#     #  #       #    #  #    #  #  ###  #  ###     #    #  # #  #  ###
#     #  #       #    #  #    #  #    #  #    #     #    #   ##  #    #
######   ######  #####    ####    ####    ####      #    #    #   ####


    #     ####
#    #
#     ####
#         #
#    #    #
#     ####


##
#  #
#    #
######
#    #
#    #


  ####   #####   #    #   #####   ####   #    #
#    #  #    #  #    #     #    #    #  #    #
#       #    #  #    #     #    #       ######
#       #####   #    #     #    #       #    #   ###
#    #  #   #   #    #     #    #    #  #    #   ###
####   #    #   ####      #     ####   #    #   ###
```

Ok, supongo que la idea es no debuggear. Ufff, sobre que me cuesta assembler

Bueno, el ultimo cambio en `edx` le asigna `eax`, y `eax = [var_30h]`. Ahi se guardara lo que nosotros ingresemos.

El format del `scanf` se saca de la direccion `0x80489e0`, la cual pareciera contener `and eax, 0x73250064`, bizarro. Pero si le decimos a `cutter` que lo convierta en string, tenemos `"%d"`. Okay okay es un numero, y se guarda en `[var_30h]`. Progress has been made... Ahora se viene la batarola

```
0x08048648      mov ebx, dword [var_34h]
0x0804864b      lea eax, [var_30h]
0x0804864e      mov dword [var_3ch], 0xffffffff ; -1
0x08048655      mov edx, eax
0x08048657      mov eax, 0
0x0804865c      mov ecx, dword [var_3ch]
0x0804865f      mov edi, edx
0x08048661      repne scasb al, byte es:[edi]
0x08048663      mov eax, ecx
0x08048665      not eax
0x08048667      sub eax, 1
0x0804866a      cmp ebx, eax
0x0804866c      jb 0x80485ef
```

Como ya vimos tantos de estos, ya podemos analizarlo mas rapido.

Primero, `ebx = 0`, pues `var_34h` se setea en 0 incluso antes de escanear (mirar foto). Siguiente, cargamos en `eax` la direccion `var_30h`. Entonces vamos a leer la direccion `var_30h` hasta encontrar `\0` de nuevo, `eax` tendra al final cuantos caracteres leimos. Comparamos `ebx = 0` con `eax`.

Probablemente 0 <= "caracteres que metamos", asi que probablemente saltemos y tengamos que correr ese codigo horrible.

Cabe aclarar que se cuentan caracteres, pero nosotros metemos un decimal. Lo unico que hay que tener en cuenta es que tenemos que pasar nuestro decimal a hexa y listo. Esto es interesante, ya que podemos hacer aparecer `\0` en el medio si queremos. Es una observacion que capaz nos sirve, capaz no `\_(ツ)_/`.

Cabe aclarar que el unico "parametro" del codigo de arriba es `var_34h`.

De todas maneras asumamos que el codigo "horrible" se correra "cantidad de caracteres" + 1, veamos que hace...


```
lea eax, [var_30h]
add eax, dword [var_34h]
movzx eax, byte [eax]                   // eax = *(var_30h + var_34h) -> input[i]
movsx edx, al
mov eax, dword [0x804a038]              // una de las direcciones importantes!
lea esi, [edx + eax]                    // esi = eax + (input[i]&0xff)
mov eax, dword [var_34h]                
sub eax, 1
mov ebx, eax                            // ebx = *(var_34h) - 1
lea eax, [var_30h]                     
mov dword [var_3ch], 0xffffffff ; -1    
mov edx, eax 
mov eax, 0                              // eax = 0
mov ecx, dword [var_3ch]                // ecx = -1
mov edi, edx                            // edi = var_30h
repne scasb al, byte es:[edi]           // leer hasta \0 en var_30h (nuestro input)
mov eax, ecx                            
not eax                                 // eax = caracteres posta + 1
lea ecx, [eax - 1]                      // ecx = caracteres posta
mov eax, ebx                            // eax = *(var_34h) - 1
mov edx, 0                              
div ecx                                 // eax = applies EDX:EAX/ecx (thank god EDX = 0)
mov eax, edx                            // eax = eax % ecx
movzx eax, byte [ebp + eax - 0x30]      // eax = *(ebp + eax - 0x30)
movsx eax, al                           // eax = al (pero manteniendo bit 7!)
xor eax, esi                            // eax ^= esi
mov dword [0x804a038], eax              // direccion importante = eax
add dword [var_34h], 1                  // [var_34h]++
```

Termina con un `[var_34h]++`, eso es esperanzador al menos...

Al parecer, `0x804a038` contiene `0x00000000`, una incognita menos

Nos falta saber que hacen la lineas `eax = *(var_34h) - 1`, y `eax = *(ebp + eax - 0x30)`

El resto es todo reproducible por nuestro amigo python (suponiendo que eso es lo que hay que hacer)

Voy a asumir que `*(var_34h)` contiene 0, si me equivoco no funciona y me fijo bien (son direcciones entre 0 y cantidad de caracteres asi que no creo que tengan cosas magicas)

La ultima vez que se toca `ebp`, se le asigna `esp`, el cual es el stack pointer segun internet. Asi que parece que estamos pidiendo algo del stack

A mimir...


