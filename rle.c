/*
 * rle.c
 *
 * A simple run length encoding (RLE) compressor and decompressor.
 *
 * The compressed format is a sequence of (count, byte) pairs, where count
 * is a single byte from 1 to 255. RLE works well on files with long runs
 * of repeated bytes, such as simple bitmaps, and works poorly on files
 * with little repetition, where it can make the file larger.
 *
 * Usage:
 *   ./rle -c <input> <output>   compress
 *   ./rle -d <input> <output>   decompress
 */

#include <stdio.h>
#include <string.h>

static int compress(const char *in_path, const char *out_path) {
    FILE *in = fopen(in_path, "rb");
    if (!in) {
        perror("fopen input");
        return 1;
    }

    FILE *out = fopen(out_path, "wb");
    if (!out) {
        perror("fopen output");
        fclose(in);
        return 1;
    }

    int c = fgetc(in);
    while (c != EOF) {
        unsigned char byte = (unsigned char)c;
        unsigned char count = 1;

        int next;
        while (count < 255 && (next = fgetc(in)) != EOF) {
            if ((unsigned char)next == byte) {
                count++;
            } else {
                ungetc(next, in);
                break;
            }
        }

        fputc(count, out);
        fputc(byte, out);

        c = fgetc(in);
    }

    fclose(in);
    fclose(out);
    return 0;
}

static int decompress(const char *in_path, const char *out_path) {
    FILE *in = fopen(in_path, "rb");
    if (!in) {
        perror("fopen input");
        return 1;
    }

    FILE *out = fopen(out_path, "wb");
    if (!out) {
        perror("fopen output");
        fclose(in);
        return 1;
    }

    int count;
    while ((count = fgetc(in)) != EOF) {
        int byte = fgetc(in);
        if (byte == EOF) {
            fprintf(stderr, "Unexpected end of file, input may be corrupt\n");
            fclose(in);
            fclose(out);
            return 1;
        }

        for (int i = 0; i < count; i++) {
            fputc(byte, out);
        }
    }

    fclose(in);
    fclose(out);
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Usage: %s -c|-d <input> <output>\n", argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "-c") == 0) {
        return compress(argv[2], argv[3]);
    }

    if (strcmp(argv[1], "-d") == 0) {
        return decompress(argv[2], argv[3]);
    }

    fprintf(stderr, "Usage: %s -c|-d <input> <output>\n", argv[0]);
    return 1;
}
