#!/bin/bash

mboxes=$1
outfolder=$2
cwdir=$PWD

for i in $mboxes/*
do
    pushd $i
    echo $i
    for mbox in *.mbox
    do
        mkdir -p $cwdir/$outfolder/$(basename $i)/
        python3 $cwdir/mboxParse.py $mbox $cwdir/$outfolder/$(basename $i)/
    done
    popd
done
