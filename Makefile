CC = cc
CFLAGS = -O2 -Wall

all: rle

rle: rle.c
	$(CC) $(CFLAGS) -o rle rle.c

clean:
	rm -f rle
