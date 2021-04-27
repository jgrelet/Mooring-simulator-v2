#!/bin/bash

# from: https://stackoverflow.com/questions/1861382/how-to-convert-a-png-image-to-a-svg

File_png="${1?:Usage: $0 file.png}"

if [[ ! -s "$File_png" ]]; then
  echo >&2 "The first argument ($File_png)"
  echo >&2 "must be a file having a size greater than zero"
  ( set -x ; ls -s "$File_png" )
  exit 1
fi

File="${File_png%.*}"

convert "$File_png" "$File.pbm"        # PNG to PBM
potrace "$File.pbm" -s -o "$File.svg"  # PBM to SVG
rm "$File.pbm"                         # Remove PBM
