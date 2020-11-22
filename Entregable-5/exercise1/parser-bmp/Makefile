
all: parse

CC=gcc -O0 -no-pie -fno-pic  -fno-stack-protector -m32 

parse: parse.c paulslib.c 
	${CC} $^ -o $@ -lm

clean:
	rm -f parse
