#!/bin/bash
while inotifywait -r -e modify,create,delete,move $1; do
        rsync -avz $1 $2
done
