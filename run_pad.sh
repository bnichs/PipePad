#!/usr/bin/env bash


PAD=$1
FIFO=$2
PYPATH=$3


echo $PAD
echo $PYTHONPATH
echo $PYPAT

CURDIR=/home/ben/workplace/pipepad

export PYTHONPATH=$PYPATH:$CURDIR

python "$PAD"