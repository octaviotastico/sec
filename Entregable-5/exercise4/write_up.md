# Ejercicio 4

Extraemos el hash usando la herramienta `office2john.py`

Nos queda
```
fsecret_doc.docx:$office$*2007*20*128*16*ba1ae53b4d016fc3a15124b2a3034779*49a69de2853eac6c62cceeeb549aac18*57e5fd8bfd182b4c70071a3052b91194e048055c
```

Y usando un ataque combinatorio con hashcat
```
hashcat -a 1 -m 9400 --username hash.txt dict1.txt dict2.txt
```

recuperamos la password `jimmyisno.1saop91`