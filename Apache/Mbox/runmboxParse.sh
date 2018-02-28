#!/bin/bash

mboxes=$1
outfolder=$2

for i in $mboxes
do
    pushd $i
    for mbox in *.mbox
    do
        python3 mboxParse.py $mbox $outfolder/$(basename $i)/
    done
    popd
done