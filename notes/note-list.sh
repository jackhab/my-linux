#!/bin/bash

#generate an array of sorted file names and full paths
IFS=$'\n' Files=($(find $HOME/my/notes -type f -printf '%f\t%p\n' | sort | tr '\t' '\n'))


#show file selector
File=$(zenity   --title 'Notes' --text="" \
                --list --hide-header --column '' --column ''    \
                --hide-column 2 --print-column 2    \
                --width=700 --height=900 \
                "${Files[@]}")

#due to possible bug on Ubuntu 14 zenity prints second column twice separated with "|"
#this removes second column from the file name
File="${File/|*}"

[[ -z $File ]] && exit 0

#show selected file in viewer, if Cancel pressed in editor
zenity  --text-info --filename=$File --text="" \
        --cancel-label="Close" --ok-label="Edit" \
        --font=Monospace --width=700 --height=900 \
        && xdg-open "$File"
