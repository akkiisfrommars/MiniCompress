#!/usr/bin/env python3
"""
compress.py

A command line wrapper around a run length encoding (RLE) compressor
written in C.

RLE works best on files with long runs of repeated bytes, such as simple
bitmaps or some logs. On typical text or already compressed files it may
make the file larger, this tool will tell you when that happens.

Usage:
    python3 compress.py compress <file> [<file> ...]
    python3 compress.py decompress <file.rle> [<file.rle> ...]
"""

import argparse
import os
import subprocess
import sys

RLE_NAMES = ["rle", "rle.exe"]
EXT = ".rle"


def find_rle():
    here = os.path.dirname(os.path.abspath(__file__))
    for name in RLE_NAMES:
        path = os.path.join(here, name)
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    return None


def format_size(num_bytes):
    size = float(num_bytes)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.0f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def run_rle(rle_path, mode, input_path, output_path):
    result = subprocess.run([rle_path, mode, input_path, output_path], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "rle failed")


def compress_file(rle_path, path):
    output_path = path + EXT
    run_rle(rle_path, "-c", path, output_path)

    original_size = os.path.getsize(path)
    new_size = os.path.getsize(output_path)

    print(f"{path} -> {output_path}")
    print(f"  original:   {format_size(original_size)}")
    print(f"  compressed: {format_size(new_size)}")

    if original_size == 0:
        print("  result:     input file is empty")
    elif new_size >= original_size:
        pct = new_size / original_size * 100
        print(f"  result:     {pct:.0f}% of original, did not shrink")
    else:
        pct = (1 - new_size / original_size) * 100
        print(f"  result:     {pct:.0f}% smaller")


def decompress_file(rle_path, path):
    if path.endswith(EXT):
        output_path = path[: -len(EXT)] + ".out"
    else:
        output_path = path + ".out"

    run_rle(rle_path, "-d", path, output_path)
    print(f"{path} -> {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Compress or decompress files using RLE.")
    sub = parser.add_subparsers(dest="command", required=True)

    compress_parser = sub.add_parser("compress", help="Compress one or more files")
    compress_parser.add_argument("files", nargs="+", help="Files to compress")

    decompress_parser = sub.add_parser("decompress", help="Decompress one or more .rle files")
    decompress_parser.add_argument("files", nargs="+", help="Files to decompress")

    args = parser.parse_args()

    rle_path = find_rle()
    if not rle_path:
        print("Could not find the 'rle' binary. Build it first with 'make'.")
        sys.exit(1)

    for path in args.files:
        if not os.path.isfile(path):
            print(f"Not a file: {path}")
            continue

        try:
            if args.command == "compress":
                compress_file(rle_path, path)
            else:
                decompress_file(rle_path, path)
        except RuntimeError as error:
            print(f"Error processing {path}: {error}")


if __name__ == "__main__":
    main()
