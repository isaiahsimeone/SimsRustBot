#!/bin/bash

# Run on rust game folder (steamapps/common/Rust)
mkdir -p extracted

find . -type f -exec sh -c '
  for file; do
    # Use binwalk to extract embedded files
    mkdir -p "./extracted/${file##*/}_extracted"
    binwalk --dd="png image:png" -C "./extracted/${file##*/}_extracted" "$file"
  done
' sh {} +

# Cleanup

# Directory where the images will be copied to
destination="./images"

# Create the destination directory if it does not exist
mkdir -p "$destination"

# Initialize a counter for file naming
declare -A dirCounter

# Find and copy PNG images, then rename them based on their parent directory with a random string
find . -type f -iname "*.png" | while read -r file; do
    # Get the directory name of the file
    dirName=$(dirname "$file")
    # Simplify the directory name to be used in the filename
    simpleName=$(basename "$dirName")
    
    # Generate a short random string
    randStr=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 4 | head -n 1)
    
    # Check if the directory's file has been encountered before and update counter
    if [[ -z ${dirCounter[$dirName]} ]]; then
        # First time this directory has been encountered
        dirCounter[$dirName]=1
    else
        # Increment counter for the directory
        ((dirCounter[$dirName]++))
    fi
    
    # Construct the new filename based on the directory name, counter, and random string
    newName="${simpleName}_${dirCounter[$dirName]}_${randStr}.png"
    
    # Copy and rename the file to the destination directory
    cp "$file" "$destination/$newName"
done

echo "PNG images have been copied and renamed in $destination."
