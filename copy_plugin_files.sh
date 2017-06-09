#!/bin/bash

#copy plugin files from aiida_fleur into your aiida version

aiida_repo=/home/broeder/aiida/github/aiida_core/aiida
aiida_plotmethods=${PWD}/src
#'.'

#test if aiida_repo exists
if [ ! -d $aiida_repo ]; then
    echo $aiida_repo 'does not exists, write in the script the aiida head directory -> exit'
    exit 1
fi

echo 'copying files from' $aiida_plotmethods 'to' $aiida_repo


#tools
if [ ! -d $aiida_repo/tools/codespecific/fleur ]; then
    mkdir $aiida_repo/tools/codespecific/fleur
    echo 'created dir' $aiida_repo/tools/codespecific/fleur
fi
cp $aiida_plotmethods/*.py $aiida_repo/tools/codespecific/fleur/

