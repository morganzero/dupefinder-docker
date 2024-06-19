#!/bin/bash

# This bash script was created to address the issue with Plex's file deletion process.
# It reads the decisions.log file and deletes the corresponding files after execution.

inputfile="$1"

if [[ ! -f "$inputfile" || ! -r "$inputfile" ]]; then
    echo "Error: $inputfile is not a valid file or lacks read permissions" >&2
    exit 1
fi

while IFS= read -r line
do
    var=$(echo "$line" | grep -oP '(?<=file": ")[^"]+')

    if [[ -f "$var" ]]; then
        if ! rm -f "$var"; then
            echo "Error: Failed to delete file: $var" >&2
        fi
    else
        echo "Error: $var is not a valid file" >&2
    fi
done < "$inputfile"
