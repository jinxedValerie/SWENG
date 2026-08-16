CC=gcc
CCFLAGS= -std=c23 -Wall -Wextra -Werror -Wpedantic
EXECUTABLE=main

default:
	clear
	make build
	make run


build:
	$(CC) $(CCFLAGS) main.c -o $(EXECUTABLE)

run:
	./$(EXECUTABLE)

# build:
# 	gcc -std=c23 -Wall -Wextra -Wpedantic     -Wshadow -Wconversion -Wsign-conversion -Wdouble-promotion \
#     -Wformat=2 -Wundef -Wstrict-prototypes -Wold-style-definition \
#     -Wvla -Wcast-qual -Wcast-align -Wnull-dereference -Wimplicit-fallthrough \
#     -Werror main.c -o main