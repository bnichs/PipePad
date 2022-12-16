#!/usr/bin/env bash


PAD=$1
FIFO=$2
PYPATH=$3


echo $PAD
echo $PYTHONPATH
echo $PYPAT

CURDIR=/home/ben/workplace/pipepad

export PYTHONPATH=$PYPATH:$CURDIR


export PIPEPAD_FIFO=$FIFO
export PIPEPAD_CUR_PATH=$PAD

echo $PIPEPAD_PAD_LANG

if [ "$PIPEPAD_PAD_LANG" = "plaintext" ]; then
  echo

elif [ "$PIPEPAD_PAD_LANG" = "python" ]; then
  python "$PAD"
fi