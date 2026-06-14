# MiniCompress

A small file compressor and decompressor using run length encoding (RLE),
implemented in C, with a Python command line wrapper.

RLE replaces runs of repeated bytes with a (count, byte) pair. It works
well on files with long runs of repeated values, such as simple bitmaps,
some logs, or padded binary formats. On typical text or already compressed
files, it usually makes the file larger, since most bytes do not repeat.
This tool reports the result either way so you know what happened.

## Build

```
make
```

This compiles `rle.c` into an `rle` binary in the same folder.

## Usage

Compress one or more files (creates `<file>.rle` alongside the original):

```
python3 compress.py compress notes.txt
python3 compress.py compress file1.bin file2.bin
```

Decompress an `.rle` file (creates `<name>.out`):

```
python3 compress.py decompress notes.txt.rle
```

## How it works

- `rle.c` reads the input byte by byte. For each run of identical bytes
  (up to 255 in a row), it writes one byte for the count and one byte for
  the value. Decompression reverses this by reading each (count, byte)
  pair and writing the byte that many times.
- `compress.py` calls the `rle` binary for the actual work, then reports
  the original size, compressed size, and whether the file actually got
  smaller.

## Notes

- The original file is never modified or deleted, compress and decompress
  always write a new file.
- Compression and decompression are lossless, the original bytes are
  reproduced exactly.
