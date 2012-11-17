#!/usr/bin/env bash

# flush.sh

files=`ls src/`
if ! [ -z $files ]; then
  rm src/*
  echo "Files from 'src' directory deleted successfully"
else
  echo "No files found!"
fi

exit 0
