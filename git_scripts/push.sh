#!/bin/bash

# Git push what is already in the repository
git pull --no-edit; git fetch; 

# Exclude specific files and directories
EXCLUDES=("executable")

# Find all non-hidden files and directories, excluding any hidden files and directories
find . -type f ! -path '*/.*' -print0 | while IFS= read -r -d '' file; do
    # Check if the file is in the exclude list
    should_exclude=false
    for exclude in "${EXCLUDES[@]}"; do
        if [[ "$(basename "$file")" == "$exclude" ]]; then
            should_exclude=true
            break
        fi
    done

    # Add file to staging area if it's not excluded
    if [ "$should_exclude" = false ]; then
        git add -f "$file"
    fi
done
git commit -am "latest pushes"; git push
