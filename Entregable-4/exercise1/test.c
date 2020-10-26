#include "stdlib.h"
#include "stdio.h"

#define SEMILLA_DESCONOCIDA 0x0 // ??

int main(void) {
  int i = 0; // iStack152 -> Posicion actual
  char c; // cVar1 -> Caracter en posicion actual
  unsigned int r; // uVar4 -> Random number
  char buffer [128]; // acStack148 -> Input nuestro
  srand(SEMILLA_DESCONOCIDA); // Semilla del rand, (main address)
  fgets(buffer, 128, stdin); // Mismo fgets, 128=0x80

  while ((buffer[i] != '\0' && (buffer[i] != '\n'))) {
    c = buffer[i];
    r = rand();
    r = (r & 0xFF) ^ (int)c;
    printf("%02x", r); // Necesito al menos 2 digitos
    i = i + 1;
  }
  putchar(10);

  return 0;
}
